def fibonacci():
    a = 0
    b = 1

    while True:
        yield a
        a, b = b, a + b


# prueba corta
fib = fibonacci()

for _ in range(10):
    print(next(fib))
