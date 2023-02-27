import os
import re
import datetime
import logging
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy import Table, Column, String

logging.basicConfig(
    # filename='result_log.txt',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

start_time = datetime.datetime.now()
logging.info(f"Start: {start_time}")

#VARS
filename= os.environ.get('filename')
#SQL Connect
sql_type = os.environ.get('sql_type')
#MSSQL/Postgres
server = os.environ.get('server')
database = os.environ.get('database')
username = os.environ.get('username')
password = os.environ.get('password')
db_table = os.environ.get('table')
#SQLight
db_file = os.environ.get('db_file')
#SQL Connect
#VARS

def append_to_dict(D_params, lparams):
    for params in lparams:
        D_params[params[0].lower()] = params[1].replace("'","").replace("''","").replace("-#-", '\n')
    
logging.info(f"Время чтения файла: {datetime.datetime.now() - start_time}")

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

if (len(str_log)): mainArray.append(str_log)

logging.info (f"Длинна массива: {len(mainArray)}")
logging.info(f"Время подготовки массива строк: {datetime.datetime.now() - start_time}")

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

logging.info(f"Длинна списка параметров: {len(lparams)}")
logging.info(f"Разбор параметров: {datetime.datetime.now() - start_time}")

#exit(0)
#SQL CONNECT
match sql_type:
    case "mssql":
        connect_string = f"mssql+pymssql://{username}:{password}@{server}/{database}"
    case "postgres":
        connect_string = f"postgresql+psycopg2://{username}:{password}@{server}/{database}"
    case "sqlight":
        connect_string = f"sqlite:///{db_file}"
    case _:
        logging.error('Не определен тип базы данных')
        exit(0)

engine = create_engine(connect_string, echo=False, future=False)
metadata = MetaData(engine)

#CHECK TABLE
inspect = inspect(engine)
tables_in_base = inspect.get_table_names()

if db_table in tables_in_base:
    dbTable = Table(db_table, metadata, autoload_with=engine)
else:
    logging.error("The table doesn't exist")
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

logging.info(f"Определение таблицы БД: {datetime.datetime.now() - start_time}")

#INSERT DATA
inserted = 0
conn = engine.connect()
for params in lparams:
    ins = dbTable.insert().values(**params)
    result = conn.execute(ins)

    inserted += 1
    logging.debug(f"Вставили запись: {inserted}")

logging.info(f"Количество записей в базе: {inserted}")

end_time = datetime.datetime.now()
logging.info(f"Время выполнения: {end_time - start_time}")
