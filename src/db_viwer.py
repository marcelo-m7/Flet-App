import flet as ft
import pymysql
from pymysql import Error
from config import DB_CONFIG

def fetch_data(table_name):
    """Busca todos os dados de uma tabela."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Nomes das colunas
        return columns, rows
    except Error as e:
        print(f"Erro ao buscar dados da tabela {table_name}: {e}")
        return [], []
    finally:
        if connection:
            connection.close()

def display_table(page, table_name):
    """Exibe os dados de uma tabela em uma interface Flet."""
    columns, rows = fetch_data(table_name)
    
    if not columns:
        page.add(ft.Text(f"Nenhum dado encontrado na tabela {table_name}."))
        return

    # Cria uma tabela para exibir os dados
    data_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in columns],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(value))) for value in row]
            ) for row in rows
        ],
    )

    page.add(ft.Text(f"Conteúdo da tabela {table_name}:", size=20, weight="bold"))
    page.add(data_table)

def main(page: ft.Page):
    page.title = "Visualizador do Banco de Dados"
    page.scroll = ft.ScrollMode.AUTO

    # Botões para carregar as tabelas
    btn_users = ft.ElevatedButton(
        "Carregar Usuários",
        on_click=lambda e: display_table(page, "users")
    )
    btn_tasks = ft.ElevatedButton(
        "Carregar Tarefas",
        on_click=lambda e: display_table(page, "tasks")
    )

    page.add(ft.Row([btn_users, btn_tasks]))

# Inicia o aplicativo Flet
ft.app(main, port=3001, view=ft.AppView.WEB_BROWSER)
