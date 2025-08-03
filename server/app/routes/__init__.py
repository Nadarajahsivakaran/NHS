from .auth import auth_bp
from .media_upload import upload_bp
from .appointments import appointments_bp
from .admin import admin_bp

# These will be used in app/__init__.py
__all__ = ["auth_bp", "upload_bp", "appointments_bp", "admin_bp"]
