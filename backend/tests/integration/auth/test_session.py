from fastapi import status
from fastapi.testclient import TestClient

from app.core.users.models import User
from app.core.users.schemas import UserIn
from app.infra.auth.cookies import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME


def test_signup_success(client: TestClient) -> None:
    user_in = UserIn(name='test', email='new@email.com', password='secret')

    response = client.post('/api/auth/user', json=user_in.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body['message'] == 'User created successfully.'
    assert body['data']['email'] == 'new@email.com'
    assert body['data']['name'] == 'test'
    assert 'password' not in body['data']


def test_signup_duplicate_email_returns_409(
    client: TestClient, test_user: User
) -> None:
    response = client.post(
        '/api/auth/user',
        json={'name': 'other', 'email': test_user.email, 'password': 'secret'},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'message': 'A user with this email already exists.'}


def test_signup_invalid_email_returns_422_detail(client: TestClient) -> None:
    response = client.post(
        '/api/auth/user',
        json={'name': 'test', 'email': 'not-an-email', 'password': 'secret'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    body = response.json()
    assert body.get('message') is None
    assert body['detail'][0]['loc'] == ['body', 'email']


def test_session_sets_http_only_cookies_and_no_tokens_in_body(
    client: TestClient, test_user: User
) -> None:
    response = client.post(
        '/api/auth/session',
        json={'email': test_user.email, 'password': 'test'},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body['email'] == test_user.email
    assert 'access_token' not in body
    assert 'refresh_token' not in body
    assert 'token' not in body

    set_cookie = ''.join(response.headers.get_list('set-cookie'))
    assert ACCESS_COOKIE_NAME in set_cookie
    assert REFRESH_COOKIE_NAME in set_cookie
    assert 'HttpOnly' in set_cookie
    assert client.cookies.get(ACCESS_COOKIE_NAME) is not None
    assert client.cookies.get(REFRESH_COOKIE_NAME) is not None


def test_session_invalid_credentials(client: TestClient, test_user: User) -> None:
    response = client.post(
        '/api/auth/session',
        json={'email': test_user.email, 'password': 'wrong'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'message': 'Invalid credentials.'}


def test_session_refresh_rotates_cookies(client: TestClient, test_user: User) -> None:
    login = client.post(
        '/api/auth/session',
        json={'email': test_user.email, 'password': 'test'},
    )
    old_access = login.cookies.get(ACCESS_COOKIE_NAME)
    old_refresh = login.cookies.get(REFRESH_COOKIE_NAME)

    response = client.post('/api/auth/session/refresh')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == test_user.email
    assert 'access_token' not in response.json()
    set_cookie = ''.join(response.headers.get_list('set-cookie'))
    assert ACCESS_COOKIE_NAME in set_cookie
    assert REFRESH_COOKIE_NAME in set_cookie
    assert client.cookies.get(REFRESH_COOKIE_NAME) != old_refresh
    assert old_access is not None


def test_me_returns_401_without_access_cookie(client: TestClient) -> None:
    response = client.get('/api/auth/user/me')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'message': 'Authentication required.'}


def test_me_returns_200_with_access_cookie(client: TestClient, test_user: User) -> None:
    client.post(
        '/api/auth/session',
        json={'email': test_user.email, 'password': 'test'},
    )

    response = client.get('/api/auth/user/me')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == test_user.email
    assert response.json()['id'] == test_user.id


def test_logout_clears_cookies_and_blocks_further_refresh(
    client: TestClient, test_user: User
) -> None:
    client.post(
        '/api/auth/session',
        json={'email': test_user.email, 'password': 'test'},
    )

    response = client.delete('/api/auth/session')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    me = client.get('/api/auth/user/me')
    assert me.status_code == status.HTTP_401_UNAUTHORIZED

    refresh = client.post('/api/auth/session/refresh')
    assert refresh.status_code == status.HTTP_401_UNAUTHORIZED
