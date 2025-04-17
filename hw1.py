"""
* Name: Yolanda Meng
* Date: 2024.1.15
* CSE 160, Winter 2024
* Homework 1
* Description:
"""

# Uncomment the line below to make the math.sqrt function available
import math
# Problem 1
# Coefficients of the quadratic equation
print("Problem 1 solution follows:")
a = 3
b = -5.86
c = 2.5408
d = b ** 2 - 4 * a * c
root1 = (-b - math.sqrt(d)) / (2 * a)
root2 = (-b + math.sqrt(d)) / (2 * a)
print("Root 1:", root1)
print("Root 2:", root2)

print()

# Problem 2
# This problem prints the decimal values of reciprocals from 1/2 to 1/10
print("Problem 2 solution follows:")
for i in range(2, 11):
    decimal = 1 / i
    print("1/" + str(i) + ": " + str(decimal))
print()

# Problem 3
print("Problem 3 solution follows:")

# Provided partially-working solution to problem 3
# `...` are placeholders and should be replaced
n = 10
triangular = 0
for i in range(1, n+1):
    triangular = triangular + i
print("Triangular number", n, "via loop:", triangular)
print("Triangular number", n, "via formula:", n * (n + 1) / 2)
print()

# Problem 4
# This problem calculates and prints the factorial of 10
print("Problem 4 solution follows:")
n = 10
factorial = 1
for i in range(1, n+1):
    factorial = factorial * i
print(str(n) + "!:" + " " + str(factorial))
print()

# Problem 5
# This problem calculates and prints the factorials of numbers from 10 to 1
print("Problem 5 solution follows:")
num_lines = 10
for n in range(num_lines, 0, -1):
    factorial = 1
    for i in range(1, n+1):
        factorial = factorial * i
    print(str(n) + "!: " + str(factorial))
print()

# Problem 6
print("Problem 6 solution follows:")
n = 10
# Start with the 1 outside the loop
e = 1
for i in range(1, n+1):
    factorial = 1
    for j in range(1, i+1):
        factorial = factorial * j
    e = e + 1 / factorial
print("e:", e)
