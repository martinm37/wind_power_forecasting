

import pandas as pd
import os.path

def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def get_data_path():
    return os.path.join(get_root_path(), "data")

def get_log_files_path():
    return os.path.join(get_root_path(), "log_files")

def get_pickles_path():
    return os.path.join(get_root_path(), "pickle_files")

def get_figures_path():
    return os.path.join(get_root_path(), "figures")


def get_data_file(file_name:str):
    data = pd.read_csv(os.path.join(get_data_path(),file_name))
    return data




