from http.client import HTTPException
from telnetlib import STATUS
from passlib.context import CryptContext
from api.server.validation import validate_object_id

pwd_encrypted = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash:
    def encrypt(password):
        return pwd_encrypted.hash(password)
    
    def verify(password, password_encrypted):
        return pwd_encrypted.verify(password, password_encrypted)

async def _get_field_or_404(id, collection, field)        :
    data = await collection.find_one({'_id': validate_object_id(id) })
    if data:
        return fix_id(data)
    raise HTTPException(status_code=404, detail=f'{field} not found')

    
def fix_id(data):
    if data.get('_id', False):
        data['_id'] = str(data['_id'])
        return data
    raise ValueError(f'_id not found!')
    