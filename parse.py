import re
import pyodbc

filename = '21103114.log'

#SQL Connect
server = 'localhost'
database = 'tempdb'
username = 'sa'
password = 'cnhtkjr'
db_table = "tjpy"
#SQL Connect

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

print (len(arr))
lparams = list()
for elem in arr:
    params = re.findall(',([A-Za-z0-9_А-Яа-я:]+)=([^,]+)', elem)
    lparams.append(params)
    #print (param)

print(len(lparams))

#GET LIST COLUMS
lcolums = list()
for elem_params in lparams:
    for param in params:
        column = param[0]
        lcolums.append(column)

# print(lcolums)
lcolums = set(lcolums)
# print(lcolums)
exit
#SQL
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

if not cursor.tables(table=db_table, tableType='TABLE').fetchone():
    print("doesn't exist")

    sql_create_table = "CREATE TABLE " + db_table + " ("
    for column in lcolums:
        sql_create_table = sql_create_table + '"'+column+'"' + " varchar(255), "

    sql_create_table = sql_create_table + ");"

    print (sql_create_table)
    cursor.execute(sql_create_table)
    cnxn.commit()
    print(cursor)

#INSERT DATA
colums = ""
values = ""
sql_query = "INSERT INTO " + db_table + " ("
for param in params:
    col = param[0]
    val = param[1]

    colums= colums + '"'+col+'"' + ","
    values= values + '"'+val+'"' + ","

# print(colums)
# print(values)

colums = colums.rstrip(',')
values = values.rstrip(',')

sql_query = sql_query + colums + ") VALUES ( " + values + ");"
print(sql_query)

count = cursor.execute(sql_query).rowcount
cnxn.commit()
print(count)