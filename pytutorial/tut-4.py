# # ===================
# # Python Arithmetic Operators

# a = 21
# b = 10

# # Addition
# print ("a + b : ", a + b)

# # Subtraction
# print ("a - b : ", a - b)

# # Multiplication
# print ("a * b : ", a * b)

# # Division
# print ("a / b : ", a / b)

# # Modulus
# print ("a % b : ", a % b)

# # Exponent
# print ("a ** b : ", a ** b)

# # Floor Division
# print ("a // b : ", a // b)

# # ========================
# # Python Comparison Operators


# a = 4
# b = 5

# # Equal
# print ("a == b : ", a == b)

# # Not Equal
# print ("a != b : ", a != b)

# # Greater Than
# print ("a > b : ", a > b)

# # Less Than
# print ("a < b : ", a < b)

# # Greater Than or Equal to
# print ("a >= b : ", a >= b)

# # Less Than or Equal to
# print ("a <= b : ", a <= b)

# ======================
# Python Bitwise Operators
a = 60            # 60 = 0011 1100
b = 13            # 13 = 0000 1101

print("{0:b}".format(a))
print("{0:b}".format(b))
# Binary AND
c = a & b        # 12 = 0000 1100
print ("a & b : ", c)

# Binary OR
c = a | b        # 61 = 0011 1101
print ("a | b : ", c)

# Binary XOR
c = a ^ b        # 49 = 0011 0001
print ("a ^ b : ", c)

# Binary Ones Complement
c = ~a;           # -61 = 1100 0011
print ("~a : ", c)

# Binary Left Shift
c = a << 2;       # 240 = 1111 0000
print ("a << 2 : ", c)

# Binary Right Shift
c = a >> 2;       # 15 = 0000 1111
print ("a >> 2 : ", c)