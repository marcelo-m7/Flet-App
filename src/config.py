import os
from dotenv import load_dotenv

def load_env_file(env_file_path="src/.env"):
    """
    Carrega variáveis de ambiente de um arquivo .env.

    Args:
        env_file_path (str): Caminho para o arquivo .env.
    """
    load_dotenv(env_file_path)

def get_env_variable(key, default=None):
    """
    Obtém uma variável de ambiente ou retorna um valor padrão.

    Args:
        key (str): Nome da variável de ambiente.
        default: Valor padrão caso a variável não exista.

    Returns:
        Valor da variável de ambiente ou o valor padrão.
    """
    return os.getenv(key, default)
