import json
from pydantic import BaseModel
from typing import Optional

class item_types:
    ticket = "Ticket"
    slm = "Slm"
    sla = "SLA"
    category = "ITILCategory"
    user = "User"

class TicketTimeModel(BaseModel):
    open: Optional[str] = None
    close: Optional[str] = None

class TicketModel(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    time: TicketTimeModel
    url: Optional[str] = None
    urlapprove: Optional[str] = None
    author: Optional[str] = None
    status: Optional[str] = None
    urgency: Optional[str] = None
    impact: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    authors: Optional[str] = None
    assigntouser: Optional[str] = None
    duedate: Optional[str] = None
    content: Optional[str] = None


def pretty_status(status: str):
    match status:
        case "Новая":
            return f"🟢"
        case "В работе (назначена)":
            return f"🔵"
    return f"⚪️"

def if_not_empty(content, value, default=""):
    return content if value else default

class TriggerDataModel(BaseModel):
    ticket: TicketModel

    def __str__(self) -> str:
        return f"""Тикет {self.ticket.id} {pretty_status(self.ticket.status)}
👨‍💻 {self.ticket.author}
{if_not_empty(f"🔬 {self.ticket.category}", self.ticket.category, f"🔬 Без категории")}
🚀 {self.ticket.priority} приоритет
🗓 {self.ticket.time.open}
{if_not_empty(f"♻️ {self.ticket.duedate} [SLA]", self.ticket.duedate, "♻️ - [SLA]")}
{if_not_empty(f"🛠 {self.ticket.assigntouser}", self.ticket.assigntouser, f"🛠 Не назначена")}

{self.ticket.title}
"""

class CategoryOrigin(BaseModel):
    id: int
    name: Optional[str] = None

def json2str(jsdata):
    return json.dumps(jsdata, indent=4, ensure_ascii=False)


class SlaOrigin(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None 
    entities_id: Optional[int] = None
    is_recursive: Optional[int] = None
    type: Optional[int] = None
    comment: Optional[str] = None
    number_time: Optional[int] = None
    use_ticket_calendar: Optional[int] = None
    calendars_id: Optional[int] = None
    date_mod: Optional[str] = None
    definition_time: Optional[str] = None
    end_of_working_day: Optional[int] = None
    date_creation: Optional[str] = None
    slms_id: Optional[int] = None

    def toSecond(self):
        match self.definition_time:
            case "minute":
                return self.number_time * 60
            case "hour":
                return self.number_time * 60 * 60
            case "day":
                return self.number_time * 24 * 60 * 60
            case "month":
                return self.number_time * 30 * 24 * 60 * 60    
                
def new_report_file(data: dict, pathfile="report.csv"):
    if not len(data):
        return
    import csv
    with open(pathfile, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def seconds2time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def status2str(status: int):
    s = "-"
    match status:
        case 1: s = "Открыта"
        case 2: s = "В работе" 
        case 3: s = "Запланирована"
        case 4: s = "В ожидании"
        case 5: s = "Решена"
        case 6: s = "Закрыта"
    return s

# def extract_text_from_html(html_content):
#     # Создаем объект BeautifulSoup с парсером lxml
#     soup = bs(html_content, 'lxml')
    
#     # Извлекаем текст без тегов
#     text = soup.get_text(separator='\n')
    
#     return text 