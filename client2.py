import threading
from socket import *
from customtkinter import *
import random

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x500')
        self.title("Telegram Chat")

        self.username = 'Artem'
        self.active_chat = 'Olena'

        self.random_users = ['Olena', 'Dmytro', 'Serhii', 'Kateryna', 'Ihor', 'Yuliia']
        self.random_users.remove(self.active_chat)

        # Основний контейнер
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True)

        # Ліва колонка зі списком чатів
        self.sidebar = CTkFrame(self.main_frame, width=200)
        self.sidebar.pack(side='left', fill='y')

        self.chat_list_label = CTkLabel(self.sidebar, text='Чати', font=('Arial', 16, 'bold'))
        self.chat_list_label.pack(pady=10)

        for user in [self.active_chat] + self.random_users:
            button = CTkButton(self.sidebar, text=user, command=lambda u=user: self.switch_chat(u))
            button.pack(fill='x', padx=10, pady=2)

        # Права частина з чатом
        self.chat_area = CTkFrame(self.main_frame)
        self.chat_area.pack(side='right', fill='both', expand=True)

        # Заголовок активного чату
        self.header = CTkLabel(self.chat_area, text=self.active_chat, font=('Arial', 16, 'bold'))
        self.header.pack(pady=5)

        # Поле для повідомлень
        self.chat_field = CTkTextbox(self.chat_area, font=('Arial', 14), state='disabled')
        self.chat_field.pack(padx=10, pady=5, fill='both', expand=True)

        # Поле введення повідомлення
        self.bottom_frame = CTkFrame(self.chat_area)
        self.bottom_frame.pack(padx=10, pady=5, fill='x')

        self.message_entry = CTkEntry(self.bottom_frame, placeholder_text='Введіть повідомлення:')
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))

        self.send_button = CTkButton(self.bottom_frame, text='Надіслати', command=self.send_message)
        self.send_button.pack(side='right')

        self.sock = socket(AF_INET, SOCK_STREAM)


    def add_message(self, text):
        self.chat_field.configure(state='normal')
        self.chat_field.insert(END, text + '\n')
        self.chat_field.configure(state='disabled')
        self.chat_field.see(END)

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.add_message(f"Ти: {message}")
            data = f"TEXT@{self.username}@{message}\n"


    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        parts = line.split("@", 2)
        if len(parts) >= 3 and parts[0] == "TEXT":
            author = parts[1]
            message = parts[2]
            if author != self.username:
                self.add_message(f"{author}: {message}")

    def switch_chat(self, user):
        self.active_chat = user
        self.header.configure(text=self.active_chat)
        self.chat_field.configure(state='normal')
        self.chat_field.delete('1.0', END)
        self.chat_field.configure(state='disabled')
        self.add_message(f"[Система] Ви переписуєтесь з {user}")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
