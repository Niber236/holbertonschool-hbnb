from flask_jwt_extended import JWTManager
from app.api.vi.auth import api as auth_ns

jwt = JWTManager(app)