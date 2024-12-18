from pydantic import BaseModel
from typing import Optional

EMAIL_SUFFIX_PHOENIXIT = "@phoenixit.ru"
EMAIL_SUFFIX_ATCONSULTING = "@at-consulting.ru"

class UserOrigin(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    realname: Optional[str] = None
    firstname: Optional[str] = None
    is_active: Optional[int] = None

    def get_email_phoenixit(self):
        return self.name + EMAIL_SUFFIX_PHOENIXIT
    
    def get_email_atconsulting(self):
        return self.name + EMAIL_SUFFIX_ATCONSULTING
    
class UserStorage(UserOrigin):
    telegram_id: Optional[int] = None