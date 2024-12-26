from pydantic import BaseModel
from typing import Optional

class TicketOrigin(BaseModel):
    id: int = None
    date_creation: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None
    users_id_recipient: Optional[int] = None
    _users_id_requester: Optional[int] = None
    users_id: Optional[int] = None
    solvedate: Optional[str] = None
    closedate: Optional[str] = None
    status: Optional[int] = None
    priority: int = None
    slas_id_ttr: Optional[int] = None
    slas_id_tto: Optional[int] = None
    waiting_duration: Optional[int] = None
    sla_waiting_duration: Optional[int] = None
    close_delay_stat: Optional[int] = None
    solve_delay_stat: Optional[int] = None
    takeintoaccount_delay_stat: Optional[int] = None
    itilcategories_id: Optional[int] = None

    def set_author_id(self, author_id: int):
        self._users_id_requester = author_id
        self.users_id_recipient = author_id
        self.users_id = author_id