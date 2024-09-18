from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas import User, UserCreate, Group, GroupCreate, Post, PostCreate
from app.models import (
    User as UserModel, Group as GroupModel, Post as PostModel
)
from app.dependencies import get_db
from app.security import get_current_user
from config import Config
import aiohttp

# Define the router here
router = APIRouter()


# Endpoint to start the OAuth2 flow
@router.get("/login")
async def login():
    auth_url = (
        f"{Config.OAUTH2_AUTHORIZATION_URL}"
        f"?response_type=code"
        f"&client_id={Config.CLIENT_ID}"
        f"&redirect_uri={Config.REDIRECT_URI}"
        f"&scope=https://www.googleapis.com/auth/userinfo.profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return {"authorization_url": auth_url}


@router.get("/auth/callback")
async def auth_callback(code: str):
    async with aiohttp.ClientSession() as session:
        token_url = Config.OAUTH2_TOKEN_URL
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Config.REDIRECT_URI,
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
        }
        async with session.post(token_url, data=data) as response:
            token_response = await response.json()
            access_token = token_response.get("access_token")
            if not access_token:
                raise HTTPException(
                    status_code=400, detail="Failed to get access token"
                )
            return {"access_token": access_token}


# Endpoint to get the current user (requires authentication)
@router.get("/users/me")
async def get_current_user(token: str = Depends(get_current_user)):
    return {"token": token}


# CRUD operations for users
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = UserModel(
        name=user.name, email=user.email, password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).filter(
        UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# CRUD operations for groups
@router.post("/groups/", response_model=Group)
async def create_group(group: GroupCreate, db: AsyncSession = Depends(get_db)):
    db_group = GroupModel(name=group.name)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group


# CRUD operations for posts
@router.post("/posts/", response_model=Post)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_post = PostModel(
        title=post.title, content=post.content, owner=current_user
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post
