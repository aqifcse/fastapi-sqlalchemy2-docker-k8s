import asyncio
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
import aiohttp
from app.models import User
from app.dependencies import get_db

# Set up the OAuth2 scheme with the Authorization Code flow
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    scopes={"https://www.googleapis.com/auth/userinfo.profile": "Read user profile"}
)

app = FastAPI()

# Optional: Secure route that requires the user to be logged in via OAuth2
@app.get("/secure-data/")
async def read_secure_data(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# Custom OpenAPI setup to configure OAuth2 in Swagger UI
@app.get("/openapi.json")
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = app.openapi()
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": "https://accounts.google.com/o/oauth2/auth",
                    "tokenUrl": "https://oauth2.googleapis.com/token",
                    "scopes": {
                        "https://www.googleapis.com/auth/userinfo.profile": "Read user profile"
                    }
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


async def validate_token(token: str):
    # Validate the OAuth2 token against Google's token info API
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={token}") as response:
            token_info = await response.json()
            if response.status != 200 or "error" in token_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return token_info  # Return token info for further processing


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # Validate the token and get user information
    token_info = asyncio.run(validate_token(token))  # Call the token validation function
    email = token_info.get("email")  # Extract user info from token
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not retrieve user email"
        )
    
    # Fetch the user from the database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
