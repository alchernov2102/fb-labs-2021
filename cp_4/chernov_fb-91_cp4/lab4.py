import random
from telnetlib import ENCRYPT

key_length = 256

#розширений алгоритм Евкліда g-НСД
def calculate_GCD(a, b):

    if (a == 0):
        return b, 0, 1
    else:
        g,x,y = calculate_GCD(b%a, a)
        return g, y - (b//a) * x, x


#пошук оберненого елемента за модулем
def reverse_element(a, n):

    g, x, _ = calculate_GCD(a,n)

    if g == 1:
        return x % n
    else: 
        print("No reverse element, GCD != 1", '\n')

#функція розкладу p-1 = d * 2^S
def roz_func(number):

    s = 0
    temp = number - 1 

    while temp % 2 == 0:

        temp = temp // 2
        s = s + 1

    return(temp, s)




#тест Міллера-Рабіна
def primality_test(number, count):

    temp = 0
    
    x = random.randint(2, number-1)
    var_d, var_s = roz_func(number)

    if number % 2 == 0 or number % 3 == 0 or number % 5 == 0 or number % 7 == 0 or number % 9 == 0:
        #print("Number is not prime \n")
        return False
    
    else: 

        for i in range(0, count):
            #перевіряємо НСД x та p
            if calculate_GCD(x, number)[0] > 1:

                #print("Number is not prime \n")
                return False
    
            #повертаємо x^d mod p
            elif pow(x, var_d, number) == 1 or pow(x, var_d, number) == number-1:

                continue
            
            else:

                additional_counter = 0

                while (additional_counter < var_s - 1):

                    temp = (temp ** 2) % number
                
                    if temp == 1:
                        return False
                        
                    elif temp == number - 1:
                        break

                    else:

                        additional_counter += 1

                    if additional_counter == var_s - 1:

                        return False    
        return True
                    
def generate_random_key(key_length):

    while True:
        my_key = random.randrange(2**(key_length - 1), 2 ** (key_length))
        if primality_test(my_key, 4):

            #print("YOUR KEY IS: ", my_key)
            return my_key
            

var_q = 91020714455297308973390619582600842997726535405579825765201226774219635852939
var_p = 104576276447658008256557839449428297010151568638787218098866322818644888285903
var_q1 = 110902468790912915858012174720853363541948126252774950997945903895992984067579
var_p1 = 62373675425845803064655323226345885192810191935839861456488214046498405857339




def generate_random_pairs(var_p, var_q):

    #var_q = generate_random_key(256)
    #var_p = generate_random_key(256)

    
    #print("Generated p and q values: ", var_p, var_q, "\n")


    var_n = var_p * var_q
    #print("N:", var_n, '\n')
    var_euler = (var_p - 1)*(var_q - 1)
    #print("Euler:", var_euler, '\n')


    while True:

        var_e = random.randrange(2**(key_length - 1), 2 ** (key_length))
        if calculate_GCD(var_e, var_euler)[0] == 1:
            break
    
    #print("E: ", var_e)
    var_d = reverse_element(var_e, var_euler)
    #print("D:", var_d, '\n')

    pub_key = (var_n, var_e)
    sec_key =  var_d

    print("PUBLIC KEY:", pub_key, "\n")
    print("PRIVATE KEY:", sec_key, "\n")
    

def rsa_encrypt(message, var_e, var_n):

    encrypted = pow(message, var_e, var_n)

    return encrypted

def rsa_decrypt(encrypted, var_d, var_n):

    message = pow(encrypted, var_d, var_n)
    return message

def rsa_sign(message, var_d, var_n):
    signed = pow(message, var_d, var_n)
    return signed

def rsa_verify(message, signed, var_e, var_n):
    if message == pow(signed, var_e, var_n):
        return True





 


    
   

    



