from starlette.requests import Request


def get_db(request: Request):
    """
    use when using db_session_middleware in main.py
    otherwise use get_db in settings.database
    """
    return request.state.db

