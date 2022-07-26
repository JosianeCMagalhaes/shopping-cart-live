from fastapi import APIRouter, status, BackgroundTasks, Depends
from starlette.responses import JSONResponse
from api.schemas.user import UserSchema, EmailActivate
from api.cruds.authentication import get_current_user
from api.cruds.user import create_user, get_user_by_email, update_user
from api.utils import delete_token_redis, get_from_redis, send_register

router = APIRouter(tags=['Accounts'], prefix='/accounts')

@router.get('/user/me', response_model=UserSchema)
async def user(user: UserSchema = Depends(get_current_user)):
    return user

@router.post('/register', response_model=UserSchema)
async def register(background_tasks: BackgroundTasks, user: UserSchema):
    user_db = await get_user_by_email(email=user.email)
    if user_db:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={'message': 'Email already registered'})

    user = await create_user(user)
    
    user['token'] = send_register(
        id=user['_id'],
        email=user['email'],
        background_tasks=background_tasks
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@router.post('/activate')
async def activate_account_user(active: EmailActivate):
    user = await get_user_by_email(email=active.email)
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'data': {'message':'Expired token'}})

    token_from_redis = get_from_redis(id=user['_id'], mode='register')
    if not token_from_redis:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'data': {'message':'Expired token'}})

    if active.token != token_from_redis.decode('UTF-8'):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'data': {'message': 'Expired token'}})

    user['is_active'] = True
    status_user = await update_user(user['_id'], user)
    
    if status_user == status.HTTP_304_NOT_MODIFIED:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content={'data': {'message': 'Account not modified'}})
    
    delete_token_redis(user['_id'], 'register')

    return JSONResponse(status_code=status.HTTP_200_OK, content={'data': {'message': 'Active account'}})

