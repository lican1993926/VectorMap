a=10
b=20 
if(a and b):
    print('变量a和b都为true')
else:
    print('变量a和b有一个不为true')
if (a or b):
    print('变量a和b都为true,或其中一个变量为true')
else:
    print('变量a和b都不为true')
age=26
if age>=18:
    print('adult')
elif age>=6:
    print('teenager')   
a=-5
while a<10:
   if (a%2==0):
    print('a是一个偶数')
   else:
    print('a是一个奇数')
   a+=1
number = 7
guess = -1
print("数字猜谜游戏!")
while guess != number:
    guess = int(input("请输入你猜的数字："))
    if guess == number:
        print("恭喜，你猜对了！")
    elif guess < number:
        print("猜的数字小了...")
    elif guess > number:
        print("猜的数字大了...")
a = 1
i = 0
while a != 20:
   a = int (input ('请输入你猜的数字：'))
   i += 1    
   if a == 20:
      if i<3:
         print('真厉害，这么快就猜对了！')
      else :
         print('总算猜对了，恭喜恭喜！')
   elif a < 20:
      print('你猜的数字小了，不要灰心，继续努力！')
   else :
      print('你猜的数字大了，不要灰心，继续加油！')
      class Test:
n=1000          
a=0
b=1
    while b<=n:
        a=a+b
        b+=1
print ('从1加到1000的和为'，a)        

      