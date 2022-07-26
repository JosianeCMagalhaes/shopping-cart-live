from typing import List
from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from api.cruds.authentication import get_current_user_admin
from api.cruds.user import  get_users, delete_user
from api.schemas.user import UserList

router = APIRouter(tags=['Admin Accounts'], prefix='/admin/accounts')

@router.get('', response_model=List[UserList], dependencies=[Depends(get_current_user_admin)])
async def list_user(skip=0, limit=100):
    users = await get_users(skip, limit)
    return JSONResponse(content=users, status_code=status.HTTP_200_OK)

@router.delete('/{user_id}', dependencies=[Depends(get_current_user_admin)])
async def delete_user_by_id(user_id):
    await delete_user(user_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')

    