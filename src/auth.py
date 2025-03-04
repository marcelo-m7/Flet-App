import pymysql
from pymysql import Error
import flet as ft

class AuthManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db_connection = self._create_db_connection()
        self.login_button = ft.ElevatedButton("Login", on_click=self.login_button_click)
        self.logout_button = ft.ElevatedButton("Logout", on_click=self.logout_button_click)
        self.register_button = ft.ElevatedButton("Register", on_click=self.register_button_click)
        self.username_field = ft.TextField(label="Username", expand=True)
        self.password_field = ft.TextField(label="Password", password=True, expand=True)
        self.auth_message = ft.Text("", color=ft.colors.RED)
        self.toggle_login_buttons()

    def _create_db_connection(self):
        """Cria uma conexão com o banco de dados MySQL."""
        try:
            connection = pymysql.connect(
                host='172.18.95.134',
                user='todo_user',
                password='12345',
                database='todoapp'
            )
            return connection
        except Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None

    def login_button_click(self, e):
        """Inicia o processo de login."""
        username = self.username_field.value
        password = self.password_field.value

        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                self.page.session.set("user_id", user[0])  # Armazena o ID do usuário na sessão
                self.auth_message.value = "Login realizado com sucesso!"
                self.auth_message.color = ft.colors.GREEN
                self.toggle_login_buttons()
                self.start_app_func()  # Chama a função para iniciar o app após o login
            else:
                self.auth_message.value = "Usuário ou senha incorretos."
                self.auth_message.color = ft.colors.RED
            self.page.update()

    def register_button_click(self, e):
        """Inicia o processo de registro."""
        username = self.username_field.value
        password = self.password_field.value

        if self.db_connection:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                self.db_connection.commit()
                self.auth_message.value = "Registro realizado com sucesso!"
                self.auth_message.color = ft.colors.GREEN
            except Error as e:
                self.auth_message.value = "Erro ao registrar usuário. Tente outro nome de usuário."
                self.auth_message.color = ft.colors.RED
            self.page.update()

    def logout_button_click(self, e):
        """Inicia o processo de logout."""
        self.page.session.remove("user_id")  # Remove o ID do usuário da sessão
        self.auth_message.value = "Logout realizado com sucesso!"
        self.auth_message.color = ft.colors.GREEN
        self.toggle_login_buttons()
        self.page.update()

    def toggle_login_buttons(self):
        """Alterna a visibilidade dos botões de login, registro e logout."""
        user_id = self.page.session.get("user_id")
        self.login_button.visible = user_id is None
        self.register_button.visible = user_id is None
        self.logout_button.visible = user_id is not None
        self.page.update()

    def start_app_func(self):
        """Função para iniciar o app após o login."""
        if hasattr(self.page, "start_todo_app"):
            self.page.start_todo_app()