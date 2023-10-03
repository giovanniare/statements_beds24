import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
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
        self.report_from = None
        self.report_to = None

    def set_report_dates(self, report_dates):
        self.report_from = report_dates.From
        self.report_to = report_dates.To

    def add_item_to_document(self, item, statement, x, y):
        width, height = letter
        item.wrap(width, height)
        item.drawOn(statement, x=x, y=y)

    def build_file(self, info, statement):
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
                ("FONTSIZE", (0, 0), (-1, -1), 17),
            ],
        )

        self.add_item_to_document(franja_azul, statement, CS.BLUE_LABEL_X, CS.BLUE_LABEL_Y)

        month_range = self.tools.get_month_range()
        month = self.tools.get_current_month()
        year = self.tools.get_current_year()
        report_from = self.report_from
        report_to = self.report_to

        if report_from is None or report_to is None:
            date_data = [
                ["Incomes from:", f"{month}/01/{year}", ""],
                ["Incomes to:", f"{month}/{month_range[1]}/{year}", ""],
                ["Date:", f"{month}/{month_range[1] - 1}/{year}", ""]
            ]
        else:
            date_data = [
                ["Incomes from:", f"{report_from.month}/{report_from.day}/{report_from.year}"],
                ["Incomes to:", f"{report_to.month}/{report_to.day}/{report_to.year}"],
                ["Date:", f"{month}/{month_range[1] - 1}/{year}"]
            ]

        fecha = Table(
            date_data,
            colWidths=[100, 75, 285],
            rowHeights=[15, 15, 15],
            style=[
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ],
        )   
        fecha_table_style = TableStyle(
            [
                ('ALIGN', (0, 0), (-1, -1), 'LEFT')
            ]
        )
        fecha.setStyle(fecha_table_style)

        fecha_y = (CS.BLUE_LABEL_Y - sum(fecha._rowHeights)) - CS.GENERIC_SPACE_Y
        self.add_item_to_document(fecha, statement, CS.BLUE_LABEL_X, fecha_y)

        logo_path = self.tools.get_logo_path()
        logo = Image(logo_path, width=CS.IMAGE_WIDTH, height=CS.IMAGE_HEIGHT)

        logo_y = (CS.BLUE_LABEL_Y - CS.IMAGE_HEIGHT) - 10
        logo_x = ((612 - CS.ITEM_X) - CS.IMAGE_WIDTH) - 20
        self.add_item_to_document(logo, statement, logo_x, logo_y)

    def calculate_total_and_line_total(self, invoice_items, price, property_id, property_info) -> tuple:
        booking_from_beds = True
        income = None
        charges = {}

        for item in invoice_items:
            if item["type"] == "payment":
                booking_from_beds = False
                income = item["amount"]
                continue

            concept = item["description"]
            if concept in CS.IGNORE_CONCEPT_LIST:
                continue

            charges[concept] = item["amount"]

        income_choice = price if booking_from_beds else income
        total = self.rules.get_total(charges, income_choice, property_id, booking_from_beds)
        line_total = self.rules.commission_collection(total, property_id, property_info)

        return total, line_total

    def sort_booking_table(self, booking_table, temporary_table, total_bookings):
        ordered_booking_table = sorted(temporary_table,
                                       key=lambda booking: self.tools.convert_str_date_to_datetime(booking[1]))

        for booking in ordered_booking_table:
            booking_table.append(booking)

        total_rentas_line = ["", "", "", "TOTAL RENTAS", f"$ {total_bookings}"]
        booking_table.append(total_rentas_line)

    def fill_booking_data(self, bookings, prop_id, property_info, booking_table_data) -> None:
        temporary_booking_table = []
        total_bookings = 0
        for booking in bookings:
            if booking["status"] == "cancelled":
                continue

            total, line_total = self.calculate_total_and_line_total(booking["invoiceItems"], booking["price"], prop_id, property_info)

            booking_data = [
                f"{booking['firstName']} {booking['lastName']}",
                booking["arrival"],
                booking["departure"],
                f"$ {total}",
                f"$ {line_total}"
            ]

            temporary_booking_table.append(booking_data)
            total_bookings += line_total

        self.sort_booking_table(booking_table_data, temporary_booking_table, total_bookings)

    def booking_table(self, statement, booking_table_data) -> None:
        row_heights = [20 for _ in booking_table_data]
        booking_table = Table(
            booking_table_data,
            colWidths=[180, 60, 60, 75, 85],
            rowHeights=row_heights,
            style=[
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),  # Color de fondo para el encabezado
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto para el encabezado
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alineación al centro
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
                ('GRID', (0, 0), (-1, -1), 1, colors.gray),  # Agregar bordes a la tabla
                ('GRID', (0, 0), (-1, 0), 1, colors.gray),  # Agregar bordes al encabezado
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación a la izquierda
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente para el texto en las celdas
                ('LEADING', (0, 0), (-1, -1), 14),  # Espaciado entre líneas (interlineado)
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ],
        )

        logo_y = (CS.BLUE_LABEL_Y - CS.IMAGE_HEIGHT) - 10
        table_y = (logo_y - sum(booking_table._rowHeights)) - 10
        self.add_item_to_document(booking_table, statement, CS.BLUE_LABEL_X, table_y)

    def build_booking_table(self, contenido, property_info, prop_id) -> None:
        if self.report_from is None or self.report_to is None:
            bookings = self.beds_handler.get_property_bookings(prop_id)
        else:
            bookings = self.beds_handler.get_property_bookings(prop_id, arrival_from=self.report_from, arrival_to=self.report_to)
        if not bookings:
            return

        booking_table_data = [
            CS.BOOKING_TABLE_HEADER
        ]

        listing_not_duplicated = all(prop_id not in duplicate_listing for duplicate_listing in self.rules.duplicate_listing)
        if listing_not_duplicated:
            self.fill_booking_data(bookings, prop_id, property_info, booking_table_data)
            self.booking_table(contenido, booking_table_data)
            return

        for duplicate_listing in self.rules.duplicate_listing:
            for listing in duplicate_listing:
                self.fill_booking_data(bookings, listing, property_info, booking_table_data)

        self.booking_table(contenido, booking_table_data)

    def make_all_statements(self) -> None:
        self.create_statements_folder()
        properties = self.tools.get_full_properties_data()

        if self.report_from is None or self.report_to is None:
            month = self.tools.get_current_month()
            year = self.tools.get_current_year()
            date_path = f"\\statements\\{month}-{year}"
        else:
            month = self.report_from.month
            year = self.report_from.year
            date_path = f"\\statements\\{self.report_from.month}-{self.report_from.year}_to_{self.report_to.month}-{self.report_to.year}"

        project_dir = self.tools.get_project_path()
        date_folder_dir = project_dir.join(["", date_path])

        for prop_id, info in properties.items():
            file_name = date_folder_dir.join(["", f"\\{info['property_name']}.pdf"])
            statement = canvas.Canvas(file_name, pagesize=letter)
            self.build_file(info, statement)

            listing_duplicated = all(prop_id == duplicate_listing[1] for duplicate_listing in self.rules.duplicate_listing)
            if listing_duplicated:
                continue

            self.build_booking_table(statement, info, prop_id)
            statement.save()

    def create_statements_folder(self) -> None:
        current_dir = self.tools.get_project_path()
        statements_dir = current_dir.join(["", "\\statements"])
        
        try:
            os.mkdir(statements_dir)
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{statements_dir}' successfully created.")
        except FileExistsError:
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{statements_dir}' found.")

        if self.report_from is None or self.report_to is None:
            month = self.tools.get_current_month()
            year = self.tools.get_current_year()
            date_path = f"\\{month}-{year}"
        else:
            date_path = f"\\{self.report_from.month}-{self.report_from.year}_to_{self.report_to.month}-{self.report_to.year}"

        date_folder_dir = statements_dir.join(["", date_path])

        try:
            os.mkdir(date_folder_dir)
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{date_folder_dir}' successfully created.")
        except FileExistsError:
            self.logger.printer("statement_maker/create_statements_folder", f"Reports dir: '{date_folder_dir}' found.")
