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
        self.report_from = None
        self.report_to = None

    def set_report_dates(self, report_dates):
        self.report_from = report_dates.From
        self.report_to = report_dates.To

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
                ("FONTSIZE", (0, 0), (-1, -1), 17),
            ],
        )
        contenido.append(franja_azul)

        espacio = Spacer(1, 30)
        contenido.append(espacio)

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

        contenido.append(fecha)

        espacio = Spacer(1, 50)
        contenido.append(espacio)

        return statement

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

    def booking_table(self, contenido, booking_table_data) -> None:
        booking_table = Table(
            booking_table_data,
            colWidths=[180, 60, 60, 75, 85],
            style=[
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),  # Color de fondo para el encabezado
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto para el encabezado
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alineación al centro
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espacio inferior para el encabezado
                ('GRID', (0, 0), (-1, -1), 1, colors.gray),  # Agregar bordes a la tabla
                ('GRID', (0, 0), (-1, 0), 1, colors.gray),  # Agregar bordes al encabezado
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación a la izquierda
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente para el texto en las celdas
                ('LEADING', (0, 0), (-1, -1), 14),  # Espaciado entre líneas (interlineado)
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ],
        )

        contenido.append(booking_table)
        espacio = Spacer(1, 30)
        contenido.append(espacio)

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

        project_dir = os.getcwd()
        date_folder_dir = project_dir.join(["", date_path])

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
