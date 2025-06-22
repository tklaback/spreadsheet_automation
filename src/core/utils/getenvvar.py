import os

def get_required_os_var(env_var_name: str) -> str:
    value = os.environ.get(env_var_name)

    assert value, f"{value} is a required environment variable"

    return value