import tkinter as tk
from tkinter import font, ttk
from tkcalendar import Calendar
from collections import namedtuple
from oauthlib.oauth2.rfc6749.errors import InvalidClientError
from app_api_handlers.beds_api_handler import BedsHandler
from app_api_handlers.xero_api_handler import XeroHandler
from statement_maker.statement_maker import StatementMaker
from statement_maker.property_rules import PropertyRules
from utils import consts as CS
from utils.exceptions import NoBookings, NoProperyData, NoRequestResponse, NonSuccessfulRequest
from utils.logger import Logger
from utils.tools import Tools, StringVar


class Window(object):
    def __init__(self, root) -> None:
        self.root = root
        self.tools = Tools()
        self.logger = Logger()
        self.beds_api = BedsHandler()
        self.xero_api = XeroHandler()
        self.statement_maker = StatementMaker()
        self.invite_code = None
        self.setup_msg = None
        self.token = None
        self.refresh_token = None

    def set_window_name(self) -> None:
        self.root.title(CS.TOOL_NAME)

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

        build_statement_btn = tk.Button(options_frame, text="Make Statement", command=self.build_single_statement)
        build_statement_btn.pack(padx=25, pady=20, side="left")

        xero_btn = tk.Button(options_frame, text="Xero", command=self.start_xero_process)
        xero_btn.pack(padx=25, pady=20, side="left")

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
        msg = "Error, code invalid. Try with another invite code"

        if api_response:
            self.beds_api.get_all_properties()
            msg = "All right, code valid"

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

    def make_all_statements(self, label):
        try:
            self.statement_maker.make_all_statements()
            label.config(text="All statements were created!!", fg="#27A243")
        except:
            label.config(text="Something is wrong, cannot build all staments. An error occurs.", fg="red")        

    def build_all_statements(self) -> None:
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Create statements")
        self.set_secundary_window_size(window_pop)

        options_frame = tk.Frame(window_pop)
        options_frame.pack()

        result_label = tk.Label(options_frame, text="")
        build_all_reports_btn = tk.Button(options_frame, text="Build all reports", command=lambda: self.make_all_statements(result_label))
        build_all_reports_btn.pack(pady=20)
        result_label.pack(side="bottom", pady=(70, 10), anchor="center")

        close_btn = tk.Button(window_pop, text="Close", command=window_pop.destroy)
        close_btn.pack(side="bottom", pady=20, anchor="center")

    def make_single_statement(self, label, prop_data):
        try:
            data = prop_data.get()
            self.statement_maker.make_single_statement(data.id_)
            label.config(text=f"{data.name} was created", fg=CS.PASS_COLOR)
        except NoBookings as e:
            label.config(text=f"{data.name} was not created: {e.message}", fg="orange")
        except NoProperyData as e:
            label.config(text=f"{data.name} was not created: {e.message}", fg="red")
        except IndexError:
            label.config(text="Please select one property before hit the button.", fg="red")
        except:
            label.config(text="Something went wrong.. An error occurs", fg="red")

    def build_single_statement(self) -> None:
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Create single statement")
        self.set_secundary_window_size(window_pop)

        main_win_frame = tk.Frame(window_pop)
        main_win_frame.pack()

        sorted_list = self.tools.get_sorted_property_items()

        menu_button = ttk.Menubutton(main_win_frame, text="Pick one property")
        name_selected = StringVar()

        drop_down_menu = tk.Menu(main_win_frame, tearoff=0)
        property_rules = PropertyRules()

        for item in sorted_list:
            listing_duplicated = any(item.id_ == duplicate_listing[1] for duplicate_listing in property_rules.duplicate_listing)
            if listing_duplicated:
                continue
            drop_down_menu.add_radiobutton(label=item.name, value=item, variable=name_selected)

        name_selected.trace("w", lambda *args: menu_button.config(text=name_selected.get().name))
        menu_button["menu"] = drop_down_menu
        menu_button.pack(pady=(10, 0), expand=True)

        result_label = tk.Label(main_win_frame, text="")
        build_statement_btn = tk.Button(main_win_frame, text="Create report", command=lambda: self.make_single_statement(result_label, name_selected))
        build_statement_btn.pack(pady=20)
        result_label.pack(side="bottom", pady=(70, 10), anchor="center")

        close_btn = tk.Button(window_pop, text="Close", command=window_pop.destroy)
        close_btn.pack(side="bottom", pady=20, anchor="center")


##########################################################################################################################################################################
# XERO
##########################################################################################################################################################################

    def save_client_data(self, window, client_id, client_secret, result_msg):
        xero_client_tuple = namedtuple("xero_client", ["client_id", "client_secret"])
        id_ = client_id.get()
        secret = client_secret.get()

        if not id_ or not secret:
            result_msg.config(text="Please provide Cliend ID and Client secret.", fg="orange")
            return

        try:
            xero_client = xero_client_tuple(id_, secret)
            self.xero_api.xero_oauth2(xero_client)
            self.logger.printer("window_maker.save_client_data()", "Client credentials saved.")

            window.destroy()
            self.xero_main_view()
        except InvalidClientError as e:
            result_msg.config(text=f"Invalid credentials: {e}", fg="red")
        except NonSuccessfulRequest as e:
            result_msg.config(text=e.message, fg="red")
        except NoRequestResponse as e:
            result_msg.config(text=e.message, fg="red")

    def xero_authenticate(self):
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Xero authentication")
        self.set_secundary_window_size(window_pop)

        main_win_frame = tk.Frame(window_pop)
        main_win_frame.pack()

        result_label = tk.Label(main_win_frame, text="")

        client_id_label = tk.Label(main_win_frame, text="Client ID")
        client_id_label.pack(pady=20)

        client_id_entry = tk.Entry(main_win_frame)
        client_id_entry.pack()

        client_secret_label = tk.Label(main_win_frame, text="Client Secret")
        client_secret_label.pack(pady=20)

        client_secret_entry = tk.Entry(main_win_frame)
        client_secret_entry.pack()

        save_data_btn = tk.Button(main_win_frame, text="Save", command=lambda: self.save_client_data(window_pop, client_id_entry, client_secret_entry, result_label))
        save_data_btn.pack(pady=20)

        result_label.pack(side="bottom", pady=(40, 10), anchor="center")

        close_btn = tk.Button(window_pop, text="Close", command=window_pop.destroy)
        close_btn.pack(side="bottom", pady=20, anchor="center")

    def xero_main_view(self):
        window_pop = tk.Toplevel(self.root)
        window_pop.title("Xero")
        self.set_secundary_window_size(window_pop)

        main_win_frame = tk.Frame(window_pop)
        main_win_frame.pack()

        load_file_btn = tk.Button(main_win_frame, text="Load file", command="TBD")
        load_file_btn.pack(padx=25, pady=20, side="left")

        upload_charges_btn = tk.Button(main_win_frame, text="Upload charges", command="TBD")
        upload_charges_btn.pack(padx=25, pady=20, side="left")

        configure_btn = tk.Button(main_win_frame, text="Set Up", command=self.xero_api.xero_oauth2)
        configure_btn.pack(padx=25, pady=20, side="left")

        close_btn = tk.Button(window_pop, text="Close", command=window_pop.destroy)
        close_btn.pack(side="bottom", pady=20, anchor="center")

    def start_xero_process(self):
        xero_client = self.tools.get_xero_client()
        if xero_client.client_id is None or xero_client.client_secret is None:
            self.xero_authenticate()
        else:
            self.xero_main_view()
        

