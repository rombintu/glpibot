import glpi_api
from lib.logger import logging as log
from lib.helper import item_types, SlaOrigin, CategoryOrigin
from lib.models.ticket import TicketOrigin
from lib.models.user import UserOrigin
from lib.helper import seconds2time
from lib.helper import status2str

class API:
    version = None

    def __init__(self, url, app_token, user_token):
        self.url = url
        self.app_token = app_token
        self.user_token = user_token

    def get_items(self, item_type, **kw):
        try:
            with glpi_api.connect(self.url, self.app_token, self.user_token, verify_certs=False) as glpi:
                return glpi.get_all_items(item_type, **kw)
        except glpi_api.GLPIError as err:
            log.error(str(err))
            return []
    
    def get_item(self, item_type, item_id, **kw):
        try:
            with glpi_api.connect(self.url, self.app_token, self.user_token, verify_certs=False) as glpi:
                return glpi.get_item(item_type, item_id, **kw)
        except glpi_api.GLPIError as err:
            log.error(str(err))
            return []

    def get_slas(self):
        slas_json = self.get_items(item_types.sla)
        slas = {}
        for s in slas_json:
            slas[s["id"]] = SlaOrigin(**s)
        return slas

    def get_tickets(self):
        tickets_json = self.get_items(item_types.ticket, range="1-9999")
        tickets: list[TicketOrigin] = []
        for t in tickets_json:
            if not t.get("solvedate"):
                continue
            tickets.append(TicketOrigin(**t))
        return tickets

    def get_user(self, user_id: int):
        user_json = self.get_item(item_types.user, user_id)
        if user_json:
            return UserOrigin(**user_json)

    def get_categories(self):
        categories_json = self.get_items(item_types.category)
        categories = {}
        for c in categories_json:
            categories[c["id"]] = CategoryOrigin(**c)
        return categories
    
    def prepare_report(self, 
                       tickets: list[TicketOrigin], 
                       slas: dict[int: SlaOrigin], 
                       categories: dict[int, CategoryOrigin],
                       ):
        report = []
        for ticket in tickets:
            ticket_report = {}
            sla_reaction: SlaOrigin = slas.get(ticket.slas_id_ttr)
            sla_solved: SlaOrigin = slas.get(ticket.slas_id_tto)

            # Общая информация
            ticket_report["Номер заявки"] = ticket.id
            ticket_report["Категория"] = categories.get(ticket.itilcategories_id).name if ticket.itilcategories_id else "Без категории"
            ticket_report["Тема"] = ticket.name
            # ticket_report["Сообщение"] = extract_text_from_html(ticket.content)
            ticket_report["Дата создания"] = ticket.date_creation
            ticket_report["Дата решения"] = ticket.solvedate
            ticket_report["Дата закрытия"] = ticket.closedate if ticket.closedate else "-"
            ticket_report["Приоритет"] = ticket.priority
            ticket_report["Статус"] = status2str(ticket.status)
            # Временные метки
            ticket_report["Время реакции"] = seconds2time(ticket.takeintoaccount_delay_stat)
            ticket_report["Время решения"] = seconds2time(ticket.solve_delay_stat)
            ticket_report["Время закрытия"] = seconds2time(ticket.close_delay_stat)
            ticket_report["Время ожидания"] = seconds2time(ticket.waiting_duration)

            # Нарушение
            ticket_report["SLA Время ожидания"] = seconds2time(ticket.sla_waiting_duration)
            if sla_reaction:
                ticket_report["SLA Время реакции нарушено"] = "Да" if ticket.takeintoaccount_delay_stat > sla_reaction.toSecond() else "Нет"
            else:
                ticket_report["SLA Время реакции нарушено"] = "-"
            if sla_solved:
                ticket_report["SLA Решения нарушено"] = "Да" if ticket.solve_delay_stat > sla_solved.toSecond() else "Нет"
            else:
                ticket_report["SLA Решения нарушено"] = "-"
            report.append(ticket_report)

        return report
    
    def add_items(self, item_type: str, *items: any):
        try:
            with glpi_api.connect(self.url, self.app_token, self.user_token, verify_certs=False) as glpi:
                return glpi.add(item_type, *items)
        except glpi_api.GLPIError as err:
            log.error(str(err))
            return []
        
    def create_ticket(self, ticket: dict):
        return self.add_items(item_types.ticket, (ticket))