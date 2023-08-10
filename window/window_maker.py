import tkinter as tk
from utils import consts
from beds24.beds_api_handler import BedsHandler


class Window(object):
    def __init__(self, root) -> None:
        self.root = root
        self.beds_api = BedsHandler()
        self.invite_code = None
        self.setup_msg = None

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

    def set_secundary_window_size(self, secundary_window):
        screen_height, screen_width = self.get_window_size()
        xside = int(screen_width/4)
        yside = int(screen_height/4)
        screen_size = f"{xside}x{yside}"

        secundary_window.geometry(screen_size)

    def create_window(self) -> None:
        self.set_window_name()
        self.set_window_size()

    def setup_buton(self):
        setup_btn = tk.Button(self.root, text="Set Up", command=self.mostrar_ventana_setup)
        setup_btn.pack(pady=20)

    def mostrar_ventana_setup(self):
        ventana_pop = tk.Toplevel(self.root)
        ventana_pop.title("Authentication SetUp")
        self.set_secundary_window_size(ventana_pop)

        instruction = tk.Label(ventana_pop, text="Introduce el invite code")
        instruction.pack(padx=20, pady=20)

        self.invite_code = tk.Entry(ventana_pop)
        self.invite_code.pack(pady=20)

        self.setup_msg = tk.Label(ventana_pop, text="")
        self.setup_msg.pack()

        btn_send = tk.Button(ventana_pop, text="Send", command=self.call_setup_beds_api)
        btn_send.pack(pady=10)
        btn_exit = tk.Button(ventana_pop, text="Close", command=ventana_pop.destroy)
        btn_exit.pack(pady=10)

    def call_setup_beds_api(self):
        api_response = self.beds_api.setup(self.invite_code.get())
        msg = "All right, code valid"
        if not api_response:
            msg = "Error, code invalid. Try with another invite code"

        self.setup_msg.config(text=msg)