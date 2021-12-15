import re
from datetime import datetime
import time

#filename = '../21103114.log'
filename = '../21121413.log'#big

start_time = datetime.now()

str_log = ""
arr = list()

with open(filename, "r", encoding="utf-8") as f:
    for str in f.readlines():
        str.strip()

        if (re.match(r'([0-9]{2}):([0-9]{2})\.([0-9]+)\-([0-9]+)\,(\w+)\,(\d+)', str)):
            if (len(str_log)):
                arr.append(str_log)

            str_log = str

        else:
            str_log = str_log + str

print("len array: ")
print(len(arr))

for elem in arr:
    param = re.findall(',([A-Za-z0-9_А-Яа-я:]+)=([^,]+)', elem)
    len(param)

stop_time = datetime.now()
print("start: ")
print(start_time)

print("stop: ")
print(stop_time)
print("diff: ")
print(stop_time - start_time)