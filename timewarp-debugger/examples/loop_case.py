def process_items(n):
    result = []
    for i in range(n):
        result.append(i * 2)
    return result

process_items(3)

# Note: In the debugger, you can see the loop iteration state changing
# i: 0 -> 1 -> 2
# result: [] -> [0] -> [0, 2] -> [0, 2, 4]
