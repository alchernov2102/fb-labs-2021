'''
Расширенный алгоритм Евклида: функция calculate_GCD (a, b) принимает два числа и возвращает g, x, y,
такие что ax + by = d, где d=НОД(a,b)
'''



#пошук НСД чисел a і b
def calculate_GCD(a, b):

    if (a == 0):
        return b, 0, 1
    else:
        g,x,y = calculate_GCD(b%a, a)
        return g, y - (b//a) * x, x

#пошук оберненого елемента
def reverse_element(a, n):

    g, x, _ = calculate_GCD(a,n)

    if g == 1:
        return x % n
    else: 
        print("No reverse element, GCD != 1", '\n')
       
#розв'язування лінійних порівнянь
def linear_comparsion(a, b, n):

    #масив усіх розв'язків
    all_solutions = []  
    
    #знаходимо НСД чисел
    gcd = calculate_GCD(a, n)[0]

    if gcd == 1:
        return reverse_element(a,n)

    elif gcd > 1:

        if b % gcd == 0:

          a_temp = a / gcd
          b_temp = b / gcd
          n_temp = n / gcd

          
          
          
          for sol in range(0, gcd):
              all_solutions.append((reverse_element(a_temp, n_temp) * b_temp + sol * n_temp) % n)
          
          return all_solutions        


