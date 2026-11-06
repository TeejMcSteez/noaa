import os
import pandas

def get_data(path: str | None) -> pandas.DataFrame | FileNotFoundError:
    cwd = os.getcwd()
    current_path = ""
    if path:
        current_path = f"{cwd}/{path}"
    else:
        raise FileNotFoundError
    return pandas.read_csv(current_path)
