from .config import config

def log_exception(func):
    conf = config()
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            conf.write_log(str(e.args),species="ERROR")
    return wrapper
