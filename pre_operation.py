import re
#実行コード読み取り
def coderead(start,end,codes,com,opr,count_pc,parflag,command_file):
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
    return (start,end,codes,com,opr,count_pc,parflag)
    

#backward前処理
def backward(ldata,rdata,stack,command_mode):
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
    return (ldata,rdata,stack)

#スタックとinvertedcodeの出力
def forward(ltop,rtop,com,opr,lstack,rstack,value,count_pc,command_mode,command_file,command_file2):
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
