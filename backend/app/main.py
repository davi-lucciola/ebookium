from app import create_app
from app.config import settings

app = create_app(title=settings.title)
