import stack_operator

#命令，被演算子の組を一つ受け取り実行する
def executedcommand(stack,rstack,lstack,com,opr,pc,pre,top,rtop,ltop,address,value,parpath,tablecount,command_mode):
    if com==1:#push
        top=stack_operator.push(opr,stack,top)
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==2:#load
        value.acquire()
        c=value[opr]
        value.release()
        top=stack_operator.push(c,stack,top)
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==3:#store
        value.acquire()
        rstack[rtop.value]=(value[opr])
        rstack[rtop.value+1]=(parpath)
        rtop.value=rtop.value+2
        (stack[opr],top)=stack_operator.pop1(stack,top)
        value[opr]=stack[opr]
        value.release()
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==4:#jpc
        (c,top)=stack_operator.pop1(stack,top)
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
            (c,top)=stack_operator.pop1(stack,top)
            (d,top)=stack_operator.pop1(stack,top)
            top=stack_operator.push(c+d,stack,top)
        elif (opr)==1:#'*'
            (c,top)=stack_operator.pop1(stack,top)
            (d,top)=stack_operator.pop1(stack,top)
            top=stack_operator.push(c*d,stack,top)
        elif opr==2:#'-'
            (c,top)=stack_operator.pop1(stack,top)
            (d,top)=stack_operator.pop1(stack,top)
            top=stack_operator.push(d-c,stack,top)
        elif opr==3:#'>'
            (c,top)=stack_operator.pop1(stack,top)
            (d,top)=stack_operator.pop1(stack,top)
            if d>c:
                top=stack_operator.push(1,stack,top)
            else:
                top=stack_operator.push(0,stack,top)
        elif opr==4:#'=='
            (c,top)=stack_operator.pop1(stack,top)
            (d,top)=stack_operator.pop1(stack,top)
            if d==c:
                top=stack_operator.push(1,stack,top)
            else:
                top=stack_operator.push(0,stack,top)
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
        top=stack_operator.push(opr,stack,top)
        tablecount.value=tablecount.value+1
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)
    elif com==12:#free
        (a,top)=stack_operator.pop1(stack,top)
        tablecount.value=tablecount.value-1
        pre=pc
        return (pc+1,pre,stack,top,rtop,tablecount)