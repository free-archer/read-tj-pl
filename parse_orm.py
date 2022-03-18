import re
import datetime
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy import Table, Column, String
from sqlalchemy import insert

start_time = datetime.datetime.now()
print(f"Start: {start_time}")

#filename = '21103114.log'#test
#filename = '22022411.log'#small
filename = '22031506.log'# 1GB

#SQL Connect
server = 'localhost'
database = 'tempdb'
username = 'sa'
password = 'cnhtkjr'
db_table = "tjpy7"
#SQL Connect

def append_to_dict(D_params, lparams):
    for params in lparams:
        D_params[params[0].lower()] = params[1].replace("-#-", '\n')
    
print(f"Время чтения файла: {datetime.datetime.now() - start_time}")

str_log = ""
mainArray = list()

#1. Создаем массив строк склеивая их по регулярному выражению
with open(filename, "r", encoding="utf-8-sig") as f:
    for str in f.readlines():
        str = str.strip()
        if (re.match(r'\d{2}:\d{2}.\d{6}-\d', str)):
            if (len(str_log)): mainArray.append(str_log)

            str_log = str

        else:
            str_log = "-#-".join((str_log, str))

print (f"Длинна массива: {len(mainArray)}")
print(f"Время подготовки массива строк: {datetime.datetime.now() - start_time}")

#2. Получаем список параметров
fileparams = re.findall(r'(\d{2})(\d{2})(\d{2})(\d{2})', filename)
(year, month, day, hour) = fileparams[0]
lparams = list()
for elem in mainArray:
    timeparams = re.findall(r'(\d{2}):(\d{2}).(\d{6})', elem)
    (minute, second, msec) = timeparams[0]
    date_time_str = f'20{year}-{month}-{day} {hour}:{minute}:{second}.{msec}'
    time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    Dict_params = {'time':date_time_str}

    re_patterns = (",(\w+)='([^']+)", ',(\w+)="([^"]+)', ',([A-Za-z0-9А-Яа-я:]+)=([^,]+)')
    for pattern in re_patterns:
        params = re.findall(pattern, elem)
        append_to_dict(Dict_params, params)
        if re_patterns.index(pattern) != len(pattern)-1:
            elem = re.sub(pattern, "", elem)

    if len(Dict_params):
        lparams.append(Dict_params)

print(f"Длинна списка параметров: {len(lparams)}")
print(f"Разбор параметров: {datetime.datetime.now() - start_time}")

#exit(0)
#SQL CONNECT
engine = create_engine(f"mssql+pymssql://{username}:{password}@{server}/{database}", echo=False, future=False)
#engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}')
#engine = create_engine('sqlite:///foo2.db')
metadata = MetaData(engine)

#CHECK TABLE
inspect = inspect(engine)
tables_in_base = inspect.get_table_names()

if db_table in tables_in_base:
    dbTable = Table(db_table, metadata, autoload_with=engine)
else:
    print("The table doesn't exist")
    #GET LIST UNIQUE COLUMS
    lcolumns = list()
    for params in lparams:
        for column, value in params.items():
            if column not in lcolumns:
                lcolumns.append(column)
                
    l_Column = list()
    for column in lcolumns:
        l_Column.append(Column(column, String))

    #CREATE TABLE
    dbTable = Table(db_table, metadata, *l_Column)
    metadata.create_all()

print(f"Определение таблицы БД: {datetime.datetime.now() - start_time}")

#INSERT DATA
inserted = 0
conn = engine.connect()
for params in lparams:
    ins = dbTable.insert().values(**params)
    result = conn.execute(ins)

    inserted += 1
    print(f"Вставили запись: {inserted}")

print(f"Количество записей в базе: {inserted}")

end_time = datetime.datetime.now()
print(f"Время выполнения: {end_time - start_time}")
