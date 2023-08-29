import tkinter as tk
from tkinter import font
from utils import consts
from utils.tools import Tools
from beds24.beds_api_handler import BedsHandler


class Window(object):
    def __init__(self, root) -> None:
        self.root = root
        self.tools = Tools()
        self.beds_api = BedsHandler()
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
        header = "Margaritas House - Statement Maker"
        font_size = font.Font(size=20)
        header_label = tk.Label(self.root, text=header, font=font_size)
        header_label.pack(padx=20, pady=20)

    def create_window(self) -> None:
        self.set_window_name()
        self.set_window_size()
        self.set_header_title()        

    def setup_buton(self) -> None:
        setup_btn = tk.Button(self.root, text="Set Up", command=self.mostrar_ventana_setup)
        setup_btn.pack(pady=20)

    def mostrar_ventana_setup(self) -> None:
        ventana_pop = tk.Toplevel(self.root)
        ventana_pop.title("Authentication SetUp")
        self.set_secundary_window_size(ventana_pop)
        msg = "Para obtener un nuevo invite code, primero tienes que hacer log in en beds, despues haz click en el boton de generar invite code"
        get_invite_text = tk.Label(ventana_pop, text=msg)
        get_invite_text.pack(padx=20, pady=20)
        btn_get_invite = tk.Button(ventana_pop, text="Get Invite Code", command=self.tools.invite_code_link, cursor="hand2")
        btn_get_invite.pack(pady=10)

        instruction = tk.Label(ventana_pop, text="Introduce el invite code")
        instruction.pack(padx=20, pady=20)

        self.invite_code = tk.Entry(ventana_pop)
        self.invite_code.pack(pady=20)

        self.setup_msg = tk.Label(ventana_pop, text="")
        self.setup_msg.pack()

        btn_send = tk.Button(ventana_pop, text="Send", command=self.call_setup_beds_api)
        btn_send.pack(pady=10)
        btn_exit = tk.Button(ventana_pop, text="Close", command=ventana_pop.destroy)
        btn_exit.pack(side="bottom", pady=10, padx=10, anchor="se")

    def call_setup_beds_api(self) -> None:
        api_response = self.beds_api.setup(self.invite_code.get())
        msg = "All right, code valid"
        if not api_response:
            msg = "Error, code invalid. Try with another invite code"

        self.setup_msg.config(text=msg)
