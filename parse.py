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
    paramssql = re.findall(r",(\w+)='([^']+)", elem)
    lparams.append(paramssql)
    elem = re.sub(r",(\w+)='([^']+)", "", elem)
    
    paramssql2 = re.findall(r',(\w+)="([^"]+)', elem)
    lparams.append(paramssql2)
    elem = re.sub(r',(\w+)="([^"]+)', "", elem)

    params = re.findall(r',([A-Za-z0-9А-Яа-я:]+)=([^,]+)', elem)
    ltemp = (*params, *paramssql, *paramssql2)

    if len(ltemp):
        lparams.append(ltemp)
        #print (param)

print(f"Длинна списка параметров: {len(lparams)}")

#GET LIST COLUMS
lcolums = list()
for params in lparams:
    for param in params:
        column = param[0].lower()
        if column in lcolums:
            pass
        else:
            lcolums.append(column)

# print(lcolums)
#lcolums = set(lcolums)
# print(lcolums)
#exit(0)
#SQL
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

if not cursor.tables(table=db_table, tableType='TABLE').fetchone():
    print("doesn't exist")

    sql_create_table = "CREATE TABLE " + db_table + " ("
    for column in lcolums:
        sql_create_table = sql_create_table + '"'+column+'"' + " varchar(MAX), "

    sql_create_table = sql_create_table + ");"

    #print (sql_create_table)
    cursor.execute(sql_create_table)
    cnxn.commit()
    print(cursor)

#INSERT DATA
inserted = 0
for params in lparams:
    colums = ""
    values = ""
    lvalues = list()
    spar = ""
    sql_query = "INSERT INTO " + db_table + " ("
    for param in params:
        col = param[0]
        val = param[1]

        colums= colums + '"'+col+'"' + ","
        values= values + "'"+val+"'" + ","
        spar= spar + "?,"
        lvalues.append(val)

# print(colums)
# print(values)

    colums = colums.rstrip(',')
    values = values.rstrip(',')
    spar = spar.rstrip(',')

    #sql_query = sql_query + colums + ") VALUES ( " + values + ");"
    sql_query = sql_query + colums + ") VALUES ( " + spar + ");"
    print(sql_query)

    #count = cursor.execute(sql_query).rowcount
    count = cursor.execute(sql_query, lvalues).rowcount
    cnxn.commit()
    inserted=+1
    print(f"Вставили запись: {inserted}")

print(f"Количество записей в базе: {inserted}")