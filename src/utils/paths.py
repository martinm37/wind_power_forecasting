
import os.path

def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_data_path():
    return os.path.join(get_root_path(), "data")



