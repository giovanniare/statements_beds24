import tkinter as tk
from tkinter import font
from tkcalendar import Calendar
from collections import namedtuple
from utils import consts
from utils.logger import Logger
from utils.tools import Tools
from beds24.beds_api_handler import BedsHandler
from statement_maker.statement_maker import StatementMaker


class Window(object):
    def __init__(self, root) -> None:
        self.root = root
        self.tools = Tools()
        self.logger = Logger()
        self.beds_api = BedsHandler()
        self.statement_maker = StatementMaker()
        self.invite_code = None
        self.setup_msg = None
        self.token = None
        self.refresh_token = None

    def set_window_name(self) -> None:
        self.root.title(consts.TOOL_NAME)

    def get_window_size(self) -> tuple:
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        return (screen_height, screen_width)

    def set_window_size(self) -> None:
        screen_height, screen_width = self.get_window_size()
        screen_size = f"{int(screen_width/2)}x{int(screen_height/2)}"

        self.root.geometry(screen_size)

    def set_secundary_window_size(self, secundary_window) -> None:
        screen_height, screen_width = self.get_window_size()
        xside = int(screen_width/2)
        yside = int(screen_height/3)
        screen_size = f"{xside}x{yside}"

        secundary_window.geometry(screen_size)

    def set_header_title(self) -> None:
        header_frame = tk.Frame(self.root)
        header_frame.pack()
        header = "Margaritas House - Statement Maker"
        font_size = font.Font(size=20)
        header_label = tk.Label(header_frame, text=header, font=font_size)
        header_label.pack(padx=20, pady=20)

    def create_window(self) -> None:
        self.set_window_name()
        self.set_window_size()
        self.set_header_title()

        options_frame = tk.Frame(self.root)
        options_frame.pack()

        set_report_dates_btn = tk.Button(options_frame, text="Set Dates", command=self.get_dates_from_calendar)
        set_report_dates_btn.pack(padx=25, pady=20, side="left")

        build_all_statements_btn = tk.Button(options_frame, text="Make all Statements", command=self.build_all_statements)
        build_all_statements_btn.pack(padx=25, pady=20, side="left")

        build_statement_btn = tk.Button(options_frame, text="Make Statement", command=self.build_all_statements)
        build_statement_btn.pack(padx=25, pady=20, side="left")

        close_btn = tk.Button(self.root, text="Close", command=self.root.destroy)
        close_btn.pack(side="bottom", pady=20, anchor="center")

    def setup_buton(self) -> None:
        setup_btn = tk.Button(self.root, text="Set Up", command=self.mostrar_ventana_setup)
        setup_btn.pack(pady=20)

    def mostrar_ventana_setup(self) -> None:
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Authentication SetUp")
        self.set_secundary_window_size(window_pop)
        msg = "Para obtener un nuevo invite code, primero tienes que hacer log in en beds, despues haz click en el boton de generar invite code"
        get_invite_text = tk.Label(window_pop, text=msg)
        get_invite_text.pack(padx=20, pady=20)
        btn_get_invite = tk.Button(window_pop, text="Get Invite Code", command=self.tools.invite_code_link, cursor="hand2")
        btn_get_invite.pack(pady=10)

        instruction = tk.Label(window_pop, text="Introduce el invite code")
        instruction.pack(padx=20, pady=20)

        self.invite_code = tk.Entry(window_pop)
        self.invite_code.pack(pady=20)

        self.setup_msg = tk.Label(window_pop, text="")
        self.setup_msg.pack()

        btn_send = tk.Button(window_pop, text="Send", command=self.call_setup_beds_api)
        btn_send.pack(pady=10)
        btn_exit = tk.Button(window_pop, text="Close", command=window_pop.destroy)
        btn_exit.pack(side="bottom", pady=10, padx=10, anchor="se")

    def call_setup_beds_api(self) -> None:
        api_response = self.beds_api.setup(self.invite_code.get())
        msg = "All right, code valid"
        if not api_response:
            msg = "Error, code invalid. Try with another invite code"

        self.setup_msg.config(text=msg)

    def set_report_dates_and_close(self, calendar_from, calendar_to, window_pop):
        dates = namedtuple("report_dates", ["From", "To"])
        report_dates = dates(calendar_from.selection_get(), calendar_to.selection_get())

        self.logger.printer("window_maker.get_dates_from_calendar()", f"From: {calendar_from.selection_get()} - To: {calendar_to.selection_get()}")

        self.statement_maker.set_report_dates(report_dates)
        window_pop.destroy()

    def get_dates_from_calendar(self):
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Set Report Dates")
        self.set_secundary_window_size(window_pop)

        calendar_from = Calendar(window_pop)
        calendar_from.pack(padx=20, pady=20, side="left")

        calendar_to = Calendar(window_pop)
        calendar_to.pack(padx=20, pady=20, side="left")

        set_dates_btn = tk.Button(window_pop, text="Set report dates", command=lambda: self.set_report_dates_and_close(calendar_from, calendar_to, window_pop))
        set_dates_btn.pack(pady=(100, 10))

        close_btn = tk.Button(window_pop, text="Close", command=window_pop.destroy)
        close_btn.pack()

    def build_all_statements(self) -> None:
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Create statements")
        self.set_secundary_window_size(window_pop)

        build_all_reports_btn = tk.Button(window_pop, text="Build all reports", command=self.statement_maker.make_all_statements)
        build_all_reports_btn.pack(pady=20)

        close_btn = tk.Button(window_pop, text="Close", command=self.root.destroy)
        close_btn.pack(side="bottom", pady=20, anchor="center")
