# coding = utf-8

from socket import *
import sys 
import getpass

#创建网络连接
def main():
    ADDR = ('127.0.0.1',8000)
    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return 

    # 一级界面
    while True:
        print('''
        ============Welconm=============
        --  1.注册   2.登录   3.退出  --
        ================================        
        ''')
        try:
            cmd = int(input('输入选项：'))
        except KeyboardInterrupt:
            sys.exit('谢谢使用')
        except Exception as e:
            print('命令错误')
            continue

        if cmd not in [1,2,3]:
            print('没有该选项')
            continue
        elif cmd == 1:# 注册
            do_register(s) 
        elif cmd == 2:# 登录
            do_login(s)
        elif cmd == 3:# 退出
            s.send(b'E')
            sys.exit('谢谢使用')

#注册
def do_register(s):
    while True:
        name = input('User:')
        passwd = getpass.getpass()# 隐式输入密码
        passwd1 = getpass.getpass('Again:')
        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print('两次密码不一致')
            continue
        msg = 'R %s %s'%(name,passwd)
        # 发送请求
        s.send(msg.encode())
        # 等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print('注册成功')
        elif data == 'EXISTS':
            print('该用户已存在')
        else:
            print('注册失败')
        return 

# 登录
def do_login(s):
    name = input('User:')
    passwd = getpass.getpass()# 隐式输入密码
    msg = 'L %s %s'%(name,passwd)
    # 发送请求
    s.send(msg.encode())
    # 等待回复
    data = s.recv(128).decode()
    if data == 'OK':
        print('登录成功')
        login(s,name) # 登录成功后，调用二级界面函数
    else:
        print('登录失败')

# 二级界面
def login(s,name):
    while True:
        print('''
        ==============查询界面===========
        - 1.查词    2.历史记录  3.注销 -
        ================================
        ''')
        try:
            cmd = int(input('输入选项：'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1,2,3]:
            print('没有该选项')
            continue
        elif cmd == 1: # 查单词
            do_query(s,name)  
        elif cmd == 2: # 查历史记录
            do_hist(s,name) 
        elif cmd == 3: # 退出二级界面
            return 

# 查单词       
def do_query(s,name):
    while True:
        word = input('(输入3结束查词)单词：')
        if word == '3':
            break 
        msg = 'Q %s %s'%(name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'FALL':
            print('没有找到该单词')
        else:
            print(data)

# 查历史记录
def do_hist(s,name):
    msg = 'H %s'%name 
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break 
            print(data) 
    else:
        print('没有历史记录')    


if __name__ == '__main__':
    main()




