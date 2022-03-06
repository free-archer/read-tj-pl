import re
import datetime
import pyodbc


filename = '22022411.log'
#filename = '211003111.log'

#SQL Connect
server = 'localhost'
database = 'tempdb'
username = 'sa'
password = 'cnhtkjr'
db_table = "tjpy2"
#SQL Connect

def append_to_dict(D_params, lparams):
    for params in lparams:
        D_params[params[0].lower()] = params[1]
    

str_log = ""
arr = list()

#1. Создаем массив строк склеивая их по регулярному выражению
with open(filename, "r", encoding="utf-8-sig") as f:
    for str in f.readlines():
        str = str.strip()

        if (re.match(r'([0-9]{2}):([0-9]{2})\.([0-9]+)\-([0-9]+)\,(\w+)\,(\d+)', str)):
            if (len(str_log)): arr.append(str_log)

            str_log = str

        else:
            str_log = "-#-".join((str_log, str))

print (f"Длинна массива: {len(arr)}")

#Запишем для теста
# with open("_"+filename, "w", encoding="utf-8-sig") as fw:
#     fw.writelines("\n".join(arr))


#2. Получаем список параметров
fileparams = re.findall(r'(\d{2})(\d{2})(\d{2})(\d{2})', filename)
(year, month, day, hour) = fileparams[0]
lparams = list()
for elem in arr:
    timeparams = re.findall(r'(\d{2}):(\d{2}).(\d{6})', elem)
    (minute, second, msec) = timeparams[0]
    date_time_str = f'20{year}-{month}-{day} {hour}:{minute}:{second}.{msec}'
    time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    #SQL ,([A-Za-z0-9_А-Яа-я:]+)='([^']+)
    #SQL2 ,(\w+)='([\w|\d|\s|\-|#|\.|,|(|)|:|=|/|\?|;]+)',
    #,(\w+)="([\w|\d|\s|\-|#|\.|,|(|)|:|=|/|\?|;]+)",
    #(Sql|planSQLText|Context) ',(\w+)='([^']+)' or ',(\w+)="([^"]+)'
    #papam ,([A-Za-z0-9_А-Яа-я:]+)=([^,]+)

    Dict_params = {}

    params = re.findall(r",(\w+)='([^']+)", elem)
    append_to_dict(Dict_params, params)
    elem = re.sub(r",(\w+)='([^']+)", "", elem)
    
    params = re.findall(r',(\w+)="([^"]+)', elem)
    append_to_dict(Dict_params, params)
    elem = re.sub(r',(\w+)="([^"]+)', "", elem)

    params = re.findall(r',([A-Za-z0-9А-Яа-я:]+)=([^,]+)', elem)
    append_to_dict(Dict_params, params)

    if len(Dict_params):
        lparams.append(Dict_params)

print(f"Длинна списка параметров: {len(lparams)}")

#exit(0)
#SQL
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

if not cursor.tables(table=db_table, tableType='TABLE').fetchone():
    print("doesn't exist")

    #GET LIST UNIQUE COLUMS
    lcolumns = list()
    for params in lparams:
        for column, value in params.items():
            if column not in lcolumns:
                lcolumns.append(column)

    #CREATE TABLE
    sql_create_table = "CREATE TABLE " + db_table + " ("
    for column in lcolumns:
        sql_create_table = sql_create_table + '"'+column+'"' + " varchar(MAX), "

    sql_create_table = sql_create_table + ");"

    #print (sql_create_table)
    cursor.execute(sql_create_table)
    cnxn.commit()
    print(cursor)

#INSERT DATA
inserted = 0
for params in lparams:
    columns = ""

    for column, value in params.items():
        columns= columns + '"'+column+'"' + ","

    columns = columns.rstrip(',')

    val = ('?,' * len(params)).rstrip(',')

    sql_query = "INSERT INTO " + db_table + " ("
    sql_query = sql_query + columns + ") VALUES ( " + val + ");"
    #print(sql_query)

    lvalues= list(params.values())

    count = cursor.execute(sql_query, lvalues).rowcount
    cnxn.commit()
    inserted += 1
    print(f"Вставили запись: {inserted}")

print(f"Количество записей в базе: {inserted}")


