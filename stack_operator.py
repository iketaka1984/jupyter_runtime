#push:スタックトップに値を積む
def push(a,stack,top):
    stack.append(a)
    return top+1

#pop1:スタックトップから値をポップする
def pop1(stack,top):
    t=stack[top-1]
    stack.pop()
    return (t,top-1)