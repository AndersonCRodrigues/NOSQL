from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..core.dependencies import get_user_service
from ..schemas.users import UserCreate, UsersResponse, UsersUpdate
from ..services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UsersResponse])
async def list_users(service: UsersService = Depends(get_user_service)):
    return await service.get_all()


@router.get("/{user_id}", response_model=UsersResponse)
async def get_user(user_id: str, service: UsersService = Depends(get_user_service)):
    user = await service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrada")
    return user


@router.post("/", response_model=UsersResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UsersService = Depends(get_user_service)):
    try: 
        return await service.create(data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email já cadastrado",
        )


@router.put("/{user_id}", response_model=UsersResponse)
async def update_user(user_id: str, data: UsersUpdate, service: UsersService = Depends(get_user_service)):
    user = await service.update(user_id, data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrada")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, service: UsersService = Depends(get_user_service)):
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrada")
