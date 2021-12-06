
import re

filename = 'read.txt'

str_log = ""
arr = list()

with open(filename, "r", encoding="utf-8") as f:
    for str in f.readlines():
        str.strip()
        print (str)
