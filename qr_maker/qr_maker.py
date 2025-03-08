import os
import re
import qrcode
from app_api_handlers.beds_api_handler import BedsHandler
from datetime import datetime
from utils.consts import DASH, SIRENIS_ID, WHATSAPP_NUMBER, EXTRA_QR_PROPERTIES
from utils.exceptions import UnexpectedError
from utils.tools import Tools
from utils.logger import Logger


class QrMaker(object):
    def __init__(self) -> None:
        self.beds_handler = BedsHandler()
        self.tools = Tools()
        self.logger = Logger()
        self.date_from = None
        self.date_to = None

    def set_date_from_and_date_to(self, report_dates):
        self.date_from = report_dates.From
        self.date_to = report_dates.To

    def generate_qrs(self, room_id, room_name):
        if room_id in EXTRA_QR_PROPERTIES:
            bookings_dict = self.beds_handler.get_property_bookings(room_id, arrival_from=self.date_from, arrival_to=self.date_to)
            name = room_id
        else:
            bookings_dict = self.beds_handler.get_room_bookings(SIRENIS_ID, arrival_from=self.date_from, arrival_to=self.date_to, room=room_id)
            name = room_name

        folder_obj = FolderObj(self.date_from, self.date_to, name)
        folder_obj.build()

        bookings_list = list()
        for booking in bookings_dict:
            booking_obj = BookingDetails()
            booking_obj.build(booking)
            bookings_list.append(booking_obj)

        try:
            for booking in bookings_list:
                qr_obj = QRCreator()
                qr_obj.populate(booking, folder_obj.room_path, name)
                qr_obj.build()
        except Exception as e:
            msg = f"An Error Occours over {room_id} - {room_name}: \n{e}"
            self.logger.printer("qr_maker.generate_qrs()", msg)
            error_data = (room_id, room_name)
            raise UnexpectedError(error_data)


class BookingDetails(object):
    def __init__(self):
        self.id = None
        self.propertyId = None
        self.roomId = None
        self.status = None
        self.arrival = None
        self.departure = None
        self.numAdult = None
        self.numChild = None
        self.firstName = None
        self.lastName = None

    def build(self, dictionary):
        self.id = dictionary["id"]
        self.propertyId = dictionary["propertyId"]
        self.roomId = dictionary["roomId"]
        self.status = dictionary["status"]
        self.arrival = dictionary["arrival"]
        self.departure = dictionary["departure"]
        self.numAdult = dictionary["numAdult"]
        self.numChild = dictionary["numChild"]
        self.firstName = dictionary["firstName"]
        self.lastName = dictionary["lastName"]


class QRCreator(object):
    def __init__(self):
        self.file_name = None
        self.room = None
        self.breakfast_qty = None
        self.firstName = None
        self.lastName = None
        self.guest_qty = None
        self.checkIn = None
        self.checkOut = None
        self.phone_number = None
        self.message = None

    def populate(self, book_obj: BookingDetails, room_path, room_name):
        self.room = get_room_number(room_name)
        self.firstName = book_obj.firstName
        self.lastName = book_obj.lastName
        self.checkIn = book_obj.arrival
        self.checkOut = book_obj.departure
        days_qty = calculate_days_qty(self.checkIn, self.checkOut)
        self.guest_qty = book_obj.numAdult + book_obj.numChild
        self.breakfast_qty = self.guest_qty * days_qty
        self.phone_number = WHATSAPP_NUMBER
        file_name = f"{DASH}{self.checkIn}_{self.firstName}_{self.lastName}_room{self.room}_qty{self.breakfast_qty}.png"
        self.file_name = room_path.join(["", file_name])

    def build_whatsapp_message(self):
        base_msg = "Name: {name} {last_name}, Room number: {room}, Check In date: {checkIn}, number of guests {guest_qty}, total breakfast for stay: {breakfast_qty}"
        base_msg_populated = base_msg.format(name=self.firstName,
                                             last_name=self.lastName,
                                             room=self.room,
                                             checkIn=self.checkIn,
                                             guest_qty=self.guest_qty,
                                             breakfast_qty=self.breakfast_qty)

        # Convertir el mensaje en un formato adecuado para un enlace de WhatsApp
        self.message = f"https://wa.me/{self.phone_number}?text={base_msg_populated.replace(' ', '%20')}"

    def generate_qr_object(self):
        # Generar el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.message)
        qr.make(fit=True)
        return qr

    def save_qr_image(self, qr):
        # Crear la imagen del QR
        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar la imagen del código QR
        img.save(self.file_name)

    def build(self):
        self.build_whatsapp_message()
        qr = self.generate_qr_object()
        self.save_qr_image(qr)


class FolderObj(object):
    def __init__(self, report_from, report_to, room_name):
        self.tools = Tools()
        self.logger = Logger()
        self.project_path = None
        self.qr_base_path = None
        self.date_path = None
        self.report_from = report_from
        self.report_to = report_to
        self.room_path = None
        self.room = get_room_number(room_name)

    def set_project_path_attribute(self):
        self.project_path = self.tools.get_project_path()

    def create_qr_base_folder(self):
        self.qr_base_path = self.project_path.join(["", f"{DASH}qr"])
        self.create_folder(self.qr_base_path)

    def create_date_folder(self):
        if self.report_from is None or self.report_to is None:
            month = self.tools.get_current_month()
            year = self.tools.get_current_year()
            date_folder_name = f"{DASH}{month}-{year}"
        else:
            date_folder_name = f"{DASH}{self.report_from.month}-{self.report_from.year}_to_{self.report_to.month}-{self.report_to.year}"

        self.date_path = self.qr_base_path.join(["", date_folder_name])
        self.create_folder(self.date_path)

    def create_room_folder(self):
        self.room_path = self.date_path.join(["", f"{DASH}room{self.room}"])
        self.create_folder(self.room_path)

    def create_folder(self, path):
        try:
            os.mkdir(path)
            self.logger.printer("qr_maker/create_folder: ",
                                f"Path '{path}' successfully created.")
        except FileExistsError:
            self.logger.printer("qr_maker/create_folder: ", f"Path '{path}' already exists.")

    def build(self):
        self.set_project_path_attribute()
        self.create_qr_base_folder()
        self.create_date_folder()
        self.create_room_folder()


def calculate_days_qty(fecha_inicio_str, fecha_fin_str):
    # Convertir las cadenas de fecha en objetos datetime
    formato_fecha = "%Y-%m-%d"
    fecha_inicio = datetime.strptime(fecha_inicio_str, formato_fecha)
    fecha_fin = datetime.strptime(fecha_fin_str, formato_fecha)

    # Calcular la diferencia en días
    diferencia_dias = (fecha_fin - fecha_inicio).days

    # El número de desayunos es igual a la diferencia en días
    breakfast_qty = diferencia_dias

    return breakfast_qty


def get_room_number(string):
    pattern = r'\d+'

    result = re.search(pattern, string)

    if result:
        return result.group()
    return 0
