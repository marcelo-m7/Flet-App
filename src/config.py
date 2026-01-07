import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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


# Database Configuration
DB_CONFIG = {
    'host': get_env_variable('DB_HOST', '172.18.95.134'),
    'user': get_env_variable('DB_USER', 'todo_user'),
    'password': get_env_variable('DB_PASSWORD', '12345'),
    'database': get_env_variable('DB_NAME', 'todoapp')
}

# Application Configuration
FLET_PORT = get_env_variable('FLET_PORT', '8000')
FLET_HOST = get_env_variable('FLET_HOST', '0.0.0.0')
FERNET_KEY = get_env_variable('FERNET_KEY', None)
