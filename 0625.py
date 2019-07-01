list1 = ['Google', 'Runoob', 1997, 2000];
list2 = [1, 2, 3, 4, 5, 6, 7 ];
print ("list1[0]: ", list1[0])
print ("list2[1:5]: ", list2[1:5])
message=17%4
print (message)
message1=16/2
print (message1)
message2=13.0//2
print (message2)
result=abs(-799)
print("result:",result)
import math
message3=math.fabs(-789)
message4=int (message3)
print (message4)
message5=pow(3,4)+math.sqrt(16)
message6=int(message5)
print ('pow(3,4)+math.sqrt(16)=',message6)
message7=60 & 13
print (message7)
prime_count = 0
n = 2
while (prime_count <= 1000):
  #if even, check for 2, the only even prime
  if (n % 2 == 0):
    if n == 2:
      prime_count += 1
    n += 1
  else:
    # number is odd, possible prime
    for div in range(3, n, 2):
      if (n % div == 0):
        # not a prime
        n += 1
        break
    else:
      # prime!
      prime_count += 1
      if prime_count == 1000:
        print ("The 1000 prime is", n)
      else:
        n += 1