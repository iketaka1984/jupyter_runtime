import execute
#コードの実行
def execution(mode,lock,mlock,command,opr,start,end,stack,address,value,tablecount,rstack,lstack,rtop,ltop,endflag,parpath,command_mode,command_mode2):
    pc=start
    pre=pc
    top=len(stack)
    #result=open("result.txt",mode='a')
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
                print("~~~~~~~~Process"+str(parpath)+" execute~~~~~~~~\n")
                print("pc = "+str(pc+1)+"   command = "+command1+"   operand = "+str(opr[pc])+"\n")
                #print("process"+str(parpath)+"")
                #result.write("~~~~~~~~Process"+str(parpath)+" execute~~~~~~~~\n")
                #result.write("pc = "+str(pc+1)+"   command = "+command1+"   operand = "+str(opr[pc])+"\n")
            #コマンドを実行する関数に処理を渡す
            (pc,pre,stack,top,rtop,tablecount)=execute.executedcommand(stack,rstack,lstack,command[pc],opr[pc],pc,pre,top,rtop,ltop,address,value,parpath,tablecount,command_mode)
            if command_mode2!='q':
                #print("a")
                print("executing stack:       "+str(stack[:])+"\n")
                print("shared variable stack: "+str(value[0:tablecount.value])+"\n")
                #result.write("executing stack:       "+str(stack[:])+"\n")
                #result.write("shared variable stack: "+str(value[0:tablecount.value])+"\n")
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
                print("~~~~~~~~Process"+str(parpath)+" execute~~~~~~~~\n")
                print("pc = "+str(pc+1)+"   command = "+command1+"   operand = "+str(opr[pc])+"\n")
                #result.write("~~~~~~~~Process"+str(parpath)+" execute~~~~~~~~\n")
                #result.write("pc = "+str(pc+1)+"   command = "+command1+"   operand = "+str(opr[pc])+"\n")
            (pc,pre,stack,top,rtop,tablecount)=execute.executedcommand(stack,rstack,lstack,command[pc],opr[pc],pc,pre,top,rtop,ltop,address,value,parpath,tablecount,command_mode)
            if command_mode2!='q':
                print("shared variable stack: "+str(value[0:tablecount.value])+"\n")
                #result.write("shared variable stack: "+str(value[0:tablecount.value])+"\n")
            if parpath!=0:
                lock.acquire(False)
                mlock.release()
        endflag.value=1
    #result.close()
    return stack        
