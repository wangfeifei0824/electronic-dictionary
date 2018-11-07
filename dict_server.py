'''
name:Tedu
modules: pymysql
This is a dict project for AID
'''

from socket import *
import pymysql
import os 
import sys 
import time 
from threading import *

# 定义全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#创建子进程创建僵尸进程
def zombie():
        os.wait()

# 网络搭建
def main():
    # 创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict2')

    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(10)
    print('Listen...')
    while True:
        try:
            c,addr = s.accept()
            print('Connect from ...')
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        
        # 创建子进程
        pid = os.fork()
        if pid ==0:
            s.close()
            do_child(c,db) # 子进程函数
        else:
            c.close()
            t = Thread(target = zombie)
            t.setDaemon(True)
            t.start()            
            continue

# 子进程函数
def do_child(c,db):
    while True:
        # 接收客户端请求
        data = c.recv(128).decode()
        # print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            c.close()
            break
        elif data[0] == 'R':# 注册
            do_register(c,db,data)
        elif data[0] == 'L':# 登录
            do_login(c,db,data)
        elif data[0] == 'Q':# 查单词
            do_query(c,db,data)
        elif data[0] == 'H':# 历史记录
            do_hist(c,db,data)

    sys.exit('客户端退出')

# 注册
def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    # 查询用户是否存在
    sql = 'select * from user where name="%s";'%name
    try:
        cursor.execute(sql)
        r = cursor.fetchone()
    except Exception as e:
        print(e)
        return
    if r != None:
        c.send(b'EXISTS')
        return
    #插入用户
    sql = 'insert into user(name,pass) values("%s","%s");'%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception as e:
        print(e)
        db.rollback()
        c.send(b'FALL')

# 登录
def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor() 
    # 查询用户名、密码是否正确
    sql = 'select * from user where name="%s" and pass="%s";'%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == 'None':
        c.send(b'FALL')
    else:
        c.send(b'OK')

# 查单词    
def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor() 
    #插入历史记录
    def insert_history():
        tm = time.ctime()
        sql = 'insert into hist(name,word,time) values("%s","%s","%s");'%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()       
    #查找单词
    try:
        f = open(DICT_TEXT)
    except:
        s.send(b'FALL')
        return 
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'FALL')
            f.close()
            return 
        elif tmp == word:
            c.send(line.encode())
            f.close()
            insert_history()# 调用插入历史记录函数
            return 
    f.close()
    c.send(b'FALL')

# 查询历史记录
def do_hist(c,db,data):
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor() 
    sql = 'select * from hist where name="%s";'%name 
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:# 如果没有历史记录，则返回FALL
        c.send(b'FALL')
        return 
    else:
        c.send(b'OK')
        time.sleep(0.1)
    for i in r:
        msg = "%s  %s  %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
        time.sleep(0.1)
    c.send(b'##')# 发送结束标志

if __name__ == '__main__':
    main()
