from auth import AuthManager
import flet as ft
from todo import TodoApp

def main(page: ft.Page):
    # Configurações da página
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Inicializa o gerenciador de autenticação
    auth_manager = AuthManager(page)

    # Função para iniciar o aplicativo ToDo após o login
    def start_todo_app():
        page.clean()
        todo_app = TodoApp(page)  # Passa a página para o TodoApp
        page.add(todo_app)
        page.update()
        todo_app.new_task.focus()

    auth_manager.start_app_func = start_todo_app

    page.add(
        auth_manager.username_field,
        auth_manager.password_field,
        auth_manager.login_button,
        auth_manager.register_button,
        auth_manager.logout_button,
        auth_manager.auth_message
    )

# Inicia o aplicativo Flet
ft.app(main, port=3000, view=ft.AppView.WEB_BROWSER, assets_dir="assets")