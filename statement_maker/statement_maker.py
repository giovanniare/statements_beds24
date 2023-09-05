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
from statement_maker.property_rules import PropertyRules


class StatementMaker(object):
    def __init__(self) -> None:
        self.beds_handler = BedsHandler()
        self.tools = Tools()
        self.logger = Logger()
        self.rules = PropertyRules()

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
            colWidths=[60, 60, 380],
            style=[
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ],
        )

        contenido.append(fecha)

        espacio = Spacer(1, 30)
        contenido.append(espacio)

        return statement

    def calculate_total_and_line_total(self, invoice_items, price, property_id, property_info) -> tuple:
        booking_from_beds = False
        income = None
        charges = {}

        for item in invoice_items:
            if item["type"] == "payment":
                booking_from_beds = True
                income = item["amount"]
                continue

            concept = item["description"]
            if concept == "VAT on Accommodation (Mexico)":
                continue

            charges[concept] = item["amount"]

        income_choice = price if booking_from_beds else income
        total = self.rules.get_total(charges, income_choice, property_id, booking_from_beds)
        line_total = self.rules.commission_collection(total, property_id, property_info)

        return total, line_total

    def fill_booking_data(self, bookings, prop_id, property_info, booking_table_data) -> None:
        for booking in bookings:
            if booking["status"] == "cancelled":
                continue

            total, line_total = self.calculate_total_and_line_total(booking["invoiceItems"], booking["price"], prop_id, property_info)

            booking_data = [
                f"{booking['firstName']} {booking['lastName']}",
                booking["arrival"],
                booking["departure"],
                total,
                line_total
            ]

            booking_table_data.append(booking_data)

    def booking_table(self, contenido, booking_table_data) -> None:
        booking_table = Table(
            booking_table_data,
            colWidths=[200, 75, 75, 55, 55],
        )

        contenido.append(booking_table)
        espacio = Spacer(1, 30)
        contenido.append(espacio)

    def build_booking_table(self, contenido, property_info, prop_id) -> None:
        bookings = self.beds_handler.get_property_bookings(prop_id)
        if not bookings:
            return

        booking_table_data = [
            ["Description", "From", "To", "Total", "Line Total"]
        ]

        listing_not_duplicated = all(prop_id not in duplicate_listing for duplicate_listing in self.rules.duplicate_listing)
        if listing_not_duplicated:
            self.fill_booking_data(bookings, prop_id, property_info, booking_table_data)
            return

        for duplicate_listing in self.rules.duplicate_listing:
            for listing in duplicate_listing:
                self.fill_booking_data(bookings, listing, property_info, booking_table_data)

        self.booking_table(contenido, booking_table_data)

    def make_all_statements(self) -> None:
        self.create_statements_folder()
        properties = self.tools.get_full_properties_data()

        project_dir = os.getcwd()
        date_folder_dir = project_dir.join(["", f"\\statements\\{self.tools.get_current_month()}-{self.tools.get_current_year()}"])

        for prop_id, info in properties.items():
            file_name = date_folder_dir.join(["", f"\\{info['property_name']}.pdf"])
            contenido = []
            statement = self.build_file(file_name, info, contenido)

            listing_duplicated = all(prop_id == duplicate_listing[1] for duplicate_listing in self.rules.duplicate_listing)
            if listing_duplicated:
                continue

            self.build_booking_table(contenido, info, prop_id)
            statement.build(contenido)

    def create_statements_folder(self) -> None:
        current_dir = os.getcwd()
        statements_dir = current_dir.join(["", "\\statements"])
        
        try:
            os.mkdir(statements_dir)
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{statements_dir}' successfully created.")
        except FileExistsError:
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{statements_dir}' found.")

        date_folder_dir = statements_dir.join(["", f"\\{self.tools.get_current_month()}-{self.tools.get_current_year()}"])

        try:
            os.mkdir(date_folder_dir)
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{date_folder_dir}' successfully created.")
        except FileExistsError:
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{date_folder_dir}' found.")
