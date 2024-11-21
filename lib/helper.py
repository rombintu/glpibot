import json
from pydantic import BaseModel
from typing import Optional
# from dataclasses import dataclass
class item_types:
    ticket = "Ticket"

class TicketTimeModel(BaseModel):
    open: Optional[str] = None
    close: Optional[str] = None

class TicketModel(BaseModel):
    title: Optional[str] = None
    time: TicketTimeModel
    url: Optional[str] = None
    urlapprove: Optional[str] = None
    status: Optional[str] = None
    urgency: Optional[str] = None
    impact: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    authors: Optional[str] = None
    content: Optional[str] = None

class TriggerDataModel(BaseModel):
    ticket: TicketModel

    def __str__(self) -> str:
        return f"""Новая заявка {self.ticket.title}
Категория: {self.ticket.category}
От кого: {self.ticket.authors}
Статус: {self.ticket.status}
Время открытия: {self.ticket.time.open}
Приоритет: {self.ticket.priority}
Сообщение: {self.ticket.content}
Подробнее: {self.ticket.url}"""

def json2pretty(data):
    s = json.dumps(data, ensure_ascii=False, indent=4)
    return f"""Новая заявка
```json
{data}
```
"""