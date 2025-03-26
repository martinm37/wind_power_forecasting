#!usr/bin/python3.11

import os
import datetime

from src.utils.paths import get_log_files_path

a = 1.0
a += 2.333

print(f"current time: {datetime.datetime.now()}")

# logging the output
with open(os.path.join(get_log_files_path(),"test_logs.txt"), "a") as text_file:
    print(f"{a},successful execution at {datetime.datetime.now()}", file = text_file)




