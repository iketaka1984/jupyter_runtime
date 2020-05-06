import re
import sys
import time
from multiprocessing import Process, Value, Array, Lock
codes=[]
com=[]
opr=[]
stack=[]
rstack=[]
temp=[]
ldata=[]
rdata=[]
top=-1
count_pc=0
parflag=0
command_file='code.txt'
command_file2='inv_code.txt'
command_mode='f'
command_mode2='v'

#push:スタックトップに値を積む
def push(a,stack,top):
    stack.append(a)
    return top+1

#pop1:スタックトップから値をポップする
def pop1(stack,top):
    t=stack[top-1]
    stack.pop()
    return (t,top-1)

#命令，被演算子の組を一つ受け取り実行する
def executedcommand(stack,rstack,lstack,com,opr,pc,pre,top,rtop,ltop,address,value,parpath,tablecount):
    if com==1:#push
        top=push(opr,stack,top)
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==2:#load
        value.acquire()
        c=value[opr]
        value.release()
        top=push(c,stack,top)
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==3:#store
        value.acquire()
        rstack[rtop.value]=(value[opr])
        rstack[rtop.value+1]=(parpath)
        rtop.value=rtop.value+2
        (stack[opr],top)=pop1(stack,top)
        value[opr]=stack[opr]
        value.release()
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==4:#jpc
        (c,top)=pop1(stack,top)
        if c==1:
            pre=pc
            pc=opr-2
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==5:#jmp
        pre=pc
        pc=opr-2
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==6:#op
        if (opr)==0:#'+'
            (c,top)=pop1(stack,top)
            (d,top)=pop1(stack,top)
            top=push(c+d,stack,top)
        elif (opr)==1:#'*'
            (c,top)=pop1(stack,top)
            (d,top)=pop1(stack,top)
            top=push(c*d,stack,top)
        elif opr==2:#'-'
            (c,top)=pop1(stack,top)
            (d,top)=pop1(stack,top)
            top=push(d-c,stack,top)
        elif opr==3:#'>'
            (c,top)=pop1(stack,top)
            (d,top)=pop1(stack,top)
            if d>c:
                top=push(1,stack,top)
            else:
                top=push(0,stack,top)
        elif opr==4:#'=='
            (c,top)=pop1(stack,top)
            (d,top)=pop1(stack,top)
            if d==c:
                top=push(1,stack,top)
            else:
                top=push(0,stack,top)
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==7:#label
        if command_mode=='f':
            lstack[ltop.value]=(pre)
            lstack[ltop.value+1]=parpath
            ltop.value = ltop.value+2
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==8:#rjmp
        pre=pc
        ltop.value=ltop.value-1
        pc=int(lstack[ltop.value])
        pc=pc-2
        ltop.value=ltop.value-1
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==9:#restore
        rtop.value=rtop.value-1
        value[opr]=int(rstack[rtop.value])
        rtop.value=rtop.value-1
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==0:#nop
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==10:#par
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==11:#alloc
        top=push(opr,stack,top)
        tablecount.value=tablecount.value+1
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==12:#free
        (a,top)=pop1(stack,top)
        tablecount.value=tablecount.value-1
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)

#コードの実行
def execution(mode,lock,mlock,command,opr,start,end,stack,address,value,tablecount,rstack,lstack,rtop,ltop,endflag,parpath):
    pc=start
    pre=pc
    top=len(stack)
    if command_mode=='f':
        while pc<end:
            #現在のプロセスに鍵がかかっているか確認
            if parpath!=0:
               lock.acquire()
            if command_mode2!='q':
                if command[pc]==1:
                    command1='ipush'
                elif command[pc]==2:
                    command1=' load'
                elif command[pc]==3:
                    command1='store'
                elif command[pc]==4:
                    command1='  jpc'
                elif command[pc]==5:
                    command1='  jmp'
                elif command[pc]==6:
                    command1='   op'
                elif command[pc]==7:
                    command1='label'
                elif command[pc]==10:
                    command1='  par'
                elif command[pc]==11:
                    command1='alloc'
                elif command[pc]==12:
                    command1=' free'
                print("~~~~~~~~Process"+str(parpath)+" execute~~~~~~~~")
                print("pc = "+str(pc+1)+"   command = "+command1+"   operand = "+str(opr[pc])+"")
            #コマンドを実行する関数に処理を渡す
            (pc,pre,stack,top,rtop,tablecount)=executedcommand(stack,rstack,lstack,command[pc],opr[pc],pc,pre,top,rtop,ltop,address,value,parpath,tablecount)
            if command_mode2!='q':
                print("executing stack:       "+str(stack[:])+"")
                print("shared variable stack: "+str(value[0:tablecount.value])+"")
            #表示モードによってプロセスの鍵の管理の仕方が違う
            if parpath!=0:
                if mode=='2':
                    lock.acquire(False)
                    mlock.release()
                elif mode=='1':
                    lock.release()
        endflag.value=1
    #backward mode
    elif command_mode=='b':
        while pc<end:
            if parpath!=0:
                lock.acquire()
            if command_mode2!='q':
                if command[pc]==0:
                    command1='    nop'
                elif command[pc]==7:
                    command1='  label'
                elif command[pc]==8:
                    command1='   rjmp'
                elif command[pc]==9:
                    command1='restore'
                elif command[pc]==10:
                    command1='    par'
                elif command[pc]==11:
                    command1='  alloc'
                elif command[pc]==12:
                    command1='   free'
                print("~~~~~~~~Process"+str(parpath)+" execute~~~~~~~~")
                print("pc = "+str(pc+1)+"   command = "+command1+"   operand = "+str(opr[pc])+"")
            (pc,pre,stack,top,rtop,tablecount)=executedcommand(stack,rstack,lstack,command[pc],opr[pc],pc,pre,top,rtop,ltop,address,value,parpath,tablecount)
            if command_mode2!='q':
                print("shared variable stack: "+str(value[0:tablecount.value])+"")
            if parpath!=0:
                lock.acquire(False)
                mlock.release()
        endflag.value=1
    return stack        

#実行コード読み取り
def coderead(start,end):
    global codes
    global com
    global opr
    global count_pc
    global parflag
    f=open(command_file,mode='r')
    codes=f.read()
    f.close()
    for i in range(0,len(codes),9):
        t1=codes[i:i+2]
        s1=re.search(r'\d+',t1)
        t2=codes[i+2:i+8]
        s2=re.search(r'\d+',t2)
        #comに命令oprに被演算子を格納
        com.append((int)(s1.group()))
        opr.append((int)(s2.group()))
        if ((int)(s1.group())==10 and (int)(s2.group())==0):
            start.append(count_pc)
        elif ((int)(s1.group())==10 and (int)(s2.group())==1):
            end.append(count_pc)
            parflag=parflag+1
        count_pc=count_pc+1
    return (start,end)
    

#backward前処理
def backward():
    global ldata
    global rdata
    global stack
    if command_mode=='b':
        path4='lstack.txt'
        path5='rstack.txt'
        path7='stack.txt'
        f4=open(path4,mode='r')
        f5=open(path5,mode='r')
        f7=open(path7,mode='r')
        temp=f4.read()
        ldata=re.findall(r'[-]?\d+',temp)
        temp=f5.read()
        rdata=re.findall(r'[-]?\d+',temp)
        temp=f7.read()
        stack=re.findall(r'[-]?\d+',temp)
        f4.close()
        f5.close()
        f7.close()

#スタックとinvertedcodeの出力
def forward(ltop,rtop):
    if command_mode!='f' and command_mode!='b':
        path2=command_file2
        f2=open(path2,mode='w')
        for i in range(0,count_pc,1):
            if com[count_pc-i-1]==7:
                f2.write(" 8     0\n")
            elif com[count_pc-i-1]==3:
                f2.write(" 9 "+str(opr[count_pc-i-1]).rjust(5)+"\n")
            elif com[count_pc-i-1]==4:
                f2.write(" 7     0\n")
            elif com[count_pc-i-1]==5:
                f2.write(" 7     0\n")
            elif com[count_pc-i-1]==10:
                f2.write("10 "+str(opr[count_pc-i-1]).rjust(5)+"\n")
            elif com[count_pc-i-1]==11:
                f2.write("12 "+str(opr[count_pc-i-1]).rjust(5)+"\n")
            elif com[count_pc-i-1]==12:
                f2.write("11 "+str(opr[count_pc-i-1]).rjust(5)+"\n")
            else:
                f2.write(" 0     0\n")
        f2.close()
        #print("forward code is converted into inverting code.")
    elif command_mode=='f':
        path=command_file2
        f=open(path,'w')
        for i in range(0,ltop,2):
            f.write(""+str(count_pc-lstack[i])+" "+str(lstack[i+1])+" ")
        f.close()

        path3='rstack.txt'
        f3=open(path3,'w')
        for i in range(0,rtop,1):
            f3.write(""+str(rstack[i])+" ")
        f3.close()

        path6='stack.txt'
        f6=open(path6,'w')
        for i in range(0,len(value),1):
            f6.write(""+str(value[i])+" ")
        f6.close()