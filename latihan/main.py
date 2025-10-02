# # # n = int(input("Masukkan n: ")) 
# # # for i in range(n):
# # #   print(9, end ='')

# # #--------------------------------------#

# # # animals = {"cat", "dog", "bird", "dog" ,"cow"}
# # # print(animals)

# # #--------------------------------------#

# # # c = {'1', '2', '3', '4'}
# # # b = {'5', '1', '2', '6', '7', '8',}
# # # d = c.difference(b)
# # # print(d)

# # #--------------------------------------#

# # # years = [2002, 3004, 199]
# # # years[1] = 2007
# # # for year in years :
# # #     print(year)

# # #--------------------------------------#

# # # contact={
# # #     "name": "ubed",
# # #     "company": "smk"
# # # }

# # # info_kesy = contact.keys()
# # # info_value = contact.values()
# # # info = contact.items()

# # # print(info_kesy)
# # # print(info_value)
# # # print(info)

# # #--------------------------------------#

# # # nama = ["samsul", "samsudin", "bintang", "brando"]
# # # group = [x for x in nama if x[0] == "s"]

# # # print(group)

# # #--------------------------------------#

# # # import helloworld 

# # # helloworld.say_hello()      # This should print "Hello, World!"

# # # helloworld.add(2, 3)        # This should print a + b

# # # helloworld.subtract(4, 2)   # This should print a - b

# # # helloworld.multiply(2, 5)   # This should print a * b

# # # helloworld.devide(20, 2)    # This should print a / b

# # #--------------------------------------#

# # # def ordeer():
# # #     def prepare():
# # #         return "your meal is being prepared!"
# # #     status = prepare()
# # #     return status

# # # ordeer()

# # #--------------------------------------#

# # # nums = (55,44, 33, 22)
# # # print(nums[:2] [-1])

# # #--------------------------------------#

# # # def test(func, arg) :
# # #     return func(func(arg))

# # # def mult(x) :
# # #     return x * x 

# # # print(test(mult, 2))

# # #--------------------------------------#
# # genertaor

# # def numbers(x) :
# #     for i in range (x) :
# #         if i % 2 == 0 :
# #             yield i
            
# # print(list(numbers(11)))

# # #--------------------------------------#
# # genertaor  -----#

# # def make_word():
# #     word = ""
# #     for ch in "spam":
# #         word += ch
# #         yield word

# # print(list(make_word()))

# #--------------------------------------#
# # decorators -----#

# def decor(func):
#     def wrap():
#         print("==============")
#         func()
#         print("==============")
#     return wrap


# @decor
# def print_text():
#     print("Hello World")
    
# # print_text = decor(print_text)
# print_text()

# #--------------------------------------#
# # recursion -----#

# def factorial(x):
#     if x == 1:
#         return 1
#     else:
#         return x * factorial(x-1)
    
# permutasi ------------- #
# n = factorial(6)       # n!
# r  = factorial(4)    # (n-r)!

# print(n / r)
# ----------------------- #

# permutasi siklis ------ #
# p = factorial(7) # P (siklis) = (n-1)!

# print(p)
# ----------------------- #

# translasi ------------- #
# def translation(x, y, a, b):
#     x_aksen = x + a
#     y_aksen = y + b
#     return (x_aksen, y_aksen)

# print(translation(-5, 1, 2, -3))
# ----------------------- #

# operasi factorial ----- #
# c = factorial(5)
# d = factorial(2)
# e = factorial(4)

# print(c / d)
# print(e)









