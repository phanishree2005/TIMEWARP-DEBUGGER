def multiply(x, y):
    return x * y

def do_math(a, b):
    temp = a + b
    res = multiply(temp, 2)
    return res

print(do_math(3, 4))

# Note: In the debugger, you can see the call stack depth change
# as do_math calls multiply, and you can inspect the locals
# 'temp', 'a', 'b' in do_math, and 'x', 'y' in multiply.
