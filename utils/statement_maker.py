import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from beds24.beds_api_handler import BedsHandler
from utils import consts as CS
from utils.tools import Tools
from utils.logger import Logger


class StatementMaker(object):
    def __init__(self) -> None:
        self.beds_handler = BedsHandler()
        self.tools = Tools()
        self.logger = Logger()

    def build_file(self, property_file_dir, info, contenido):
        statement = SimpleDocTemplate(property_file_dir, pagesize=letter)

        # Franja azul
        franja_azul = Table(
            [[info["property_name"]]],
            colWidths=[500],
            rowHeights=[40],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(0x5B9BD5)),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 18),
            ],
        )
        contenido.append(franja_azul)

        espacio = Spacer(1, 12)
        contenido.append(espacio)

        month_range = self.tools.get_month_range()
        month = self.tools.get_current_month()
        year = self.tools.get_current_year()

        date_data = [
            ["Incomes from:", f"{month}/{month_range[0]}/{year}"],
            ["Incomes to:", f"{month}/{month_range[1]}/{year}"],
            ["Date:", f"{month}/{month_range[1] - 1}/{year}"]
        ]

        fecha = Table(
            date_data,
            colWidths=[200, 100],
            style=[
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ],
        )

        contenido.append(fecha)

        espacio = Spacer(1, 30)
        contenido.append(fecha)

        return statement

    def calculate_total_and_line_total(self, invoice_items, price) -> tuple:
        booking_from_beds = False
        income = None
        charges = {}

        for item in invoice_items:
            if item["type"] == "payment":
                booking_from_beds = True
                income = item["amount"]

            concept = item["description"]
            charges[concept] = item["amount"]

        if booking_from_beds:
            pass
            

    def parse_bookings(self, property_id, statement) -> None:
        bookings = self.beds_handler.get_property_bookings(property_id)
        if not booking:
            return

        booking_table_data = [
            ["Description", "From", "To", "Total", "Line Total"]
        ]
        
        for booking in bookings:
            if booking["status"] == "cancelled":
                continue

            total, line_total = self.calculate_total_and_line_total(booking["invoiceItems"], booking["price"])

            booking_data = [
                f"{booking['firstName']} {booking['lastName']}",
                booking["arrival"],
                booking["departure"],
                total,
                line_total
            ]

            booking_table_data.append(booking_data)
            

    def make_all_statements(self) -> None:
        properties = self.tools.get_full_properties_data()

        project_dir = os.getcwd()
        date_folder_dir = project_dir.join["", f"\\statements\\{self.tools.get_current_month()}-{self.tools.get_current_year()}"]

        for prop_id, info in properties.items():
            file_name = date_folder_dir.join(["", info["property_name"]])
            contenido = []
            statement = self.build_file(file_name, info, contenido)

            self.parse_bookings(properties[prop_id], statement)

    def create_statements_folder(self) -> None:
        current_dir = os.getcwd()
        statements_dir = current_dir.join(["", "\\statements"])
        
        try:
            os.mkdir(statements_dir)
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{statements_dir}' successfully created.")
        except FileExistsError:
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{statements_dir}' found.")

        date_folder_dir = statements_dir.join["", f"\\{self.tools.get_current_month()}-{self.tools.get_current_year()}"]

        try:
            os.mkdir(date_folder_dir)
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{date_folder_dir}' successfully created.")
        except FileExistsError:
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{date_folder_dir}' found.")
