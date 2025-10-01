import hashlib

from fastapi_users.jwt import decode_jwt
from app import auth_settings

class UserInfoBackend:
    async def get_user_info(self, auth_header=None):
        if not auth_header or auth_header.split(" ")[0] == "Basic":
            return {
                "authentication": False,
                "email": "Unauthenticated User",
                "roles": [None],
                "provider": "JWT",
                "realm": "Bearer",
            }

        cache_key = (
            hashlib.blake2b(auth_header.split(" ")[1].encode()).hexdigest().encode()
        )
        
        data = decode_jwt(
            auth_settings.jwt_secret,
            ["fastapi-users:auth"],
            algorithms="HS256",
        )

        return {
            "authenticated": True,
            "email": data.get("email"),
            "roles": [data.get("role")],
            "provider": "JWT",
            "realm": "Bearer",
        }