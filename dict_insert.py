import pymysql 
import re 

db = pymysql.connect('localhost','root','123456','dict2')
cursor = db.cursor()

f =  open('./dict.txt') 
for line in f:
    try:
        obj = re.match(r"([-a-zA-Z]+)\s+(.+)",line)
        word = obj.group(1)
        interpret = obj.group(2)
    except:
        continue
    # print(word, '-->', interpret)
    sql = 'insert into words(word,interpret) values("%s","%s");'%(word,interpret)
    try:
        cursor.execute(sql)
        db.commit()
        print('0k')
    except Exception as e:
        print(e)
        db.rollback()

cursor.close()
db.close()  
f.close()


