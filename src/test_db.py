import pymysql
from pymysql import Error

def create_connection():
    """Cria uma conexão com o banco de dados MySQL."""
    try:
        connection = pymysql.connect(
            host='172.18.95.134',  # Substitua pelo IP do servidor do banco de dados
            user='todo_user',       # Substitua pelo usuário do banco de dados
            password='12345',      # Substitua pela senha do banco de dados
            database='todoapp'     # Substitua pelo nome do banco de dados
        )
        print("Conexão ao banco de dados estabelecida com sucesso!")
        return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def test_create_table(connection):
    """Testa a criação de uma tabela no banco de dados."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabela 'test_table' criada com sucesso!")
    except Error as e:
        print(f"Erro ao criar tabela: {e}")

def test_insert_data(connection):
    """Testa a inserção de dados na tabela."""
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO test_table (name) VALUES (%s)", ("Teste 1",))
        connection.commit()
        print("Dados inseridos com sucesso!")
    except Error as e:
        print(f"Erro ao inserir dados: {e}")

def test_read_data(connection):
    """Testa a leitura de dados da tabela."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        print("Dados lidos com sucesso:")
        for row in rows:
            print(row)
    except Error as e:
        print(f"Erro ao ler dados: {e}")

def test_update_data(connection):
    """Testa a atualização de dados na tabela."""
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE test_table SET name = %s WHERE id = %s", ("Teste Atualizado", 1))
        connection.commit()
        print("Dados atualizados com sucesso!")
    except Error as e:
        print(f"Erro ao atualizar dados: {e}")

def test_delete_data(connection):
    """Testa a exclusão de dados da tabela."""
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM test_table WHERE id = %s", (1,))
        connection.commit()
        print("Dados excluídos com sucesso!")
    except Error as e:
        print(f"Erro ao excluir dados: {e}")

def main():
    """Função principal para testar o banco de dados."""
    connection = create_connection()
    if connection:
        try:
            # Testar operações CRUD
            test_create_table(connection)
            test_insert_data(connection)
            test_read_data(connection)
            test_update_data(connection)
            test_read_data(connection)
            test_delete_data(connection)
            test_read_data(connection)
        finally:
            # Fechar a conexão com o banco de dados
            connection.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()