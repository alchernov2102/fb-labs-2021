import random


key_length = 256

#розширений алгоритм Евкліда 
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
            

var_q = 178658293926135350700920903979336738587095191539795651452453458168024038066993
var_p = 278254034557349701170736144331736945666227895345976837499171901170822344402849
var_q1 = 76372103711763912577011713974872193706501899482824593053130169929661142963293
var_p1 = 203383915170499312103832799543620348968177648113589717632697842086025763303371




def generate_random_pairs(var_p, var_q):

    #var_q = generate_random_key(256)
    #var_p = generate_random_key(256)

    
    #print("Generated p and q values: ", var_p, var_q, "\n")


    var_n = var_p * var_q
    #print("N:", var_n, '\n')
    var_euler = (var_p - 1)*(var_q - 1)
    #print("Euler:", var_euler, '\n')


    while True:

        var_e = random.randint(2, var_euler - 1)
        if calculate_GCD(var_e, var_euler)[0] == 1:
            break
    
    #print("E: ", var_e)
    var_d = reverse_element(var_e, var_euler)
    #print("D:", var_d, '\n')

    pub_key = (var_n, var_e)
    sec_key =  var_d

    #print("PUBLIC KEY:", pub_key, "\n")
    #print("PRIVATE KEY:", sec_key, "\n")

    return sec_key, pub_key 
    

def rsa_encrypt(message, public_key):

    var_n = public_key[0]
    var_e = public_key[1]

    encrypted = pow(message, var_e, var_n)

    return encrypted

def rsa_decrypt(encrypted, public_key, private_key):

    message = pow(encrypted, private_key, public_key[0])
    return message

def rsa_sign(message, private_key, public_key):
    signed = pow(message, private_key, public_key[0])
    return signed

def rsa_verify(message, signed, public_key):
    if message == pow(signed, public_key[1], public_key[0]):
        return True

#TODO receive key
def rsa_receive_key(encrypted, encrypt_signed, private_key, public_key1, public_key2):

    message = rsa_decrypt(encrypted, public_key1, private_key)
    decrypt_signed = rsa_decrypt(encrypt_signed, public_key1, private_key)
    exchange_ver = rsa_verify(message, decrypt_signed, public_key2)
    print("Received!")

    return message, exchange_ver


#TODO send key
def rsa_send_key(message, secret_k, public_key1, public_key2 ):
    encrypted = rsa_encrypt(message, public_key1)
    signed = rsa_sign(message, secret_k, public_key2)
    encypt_signed = rsa_encrypt(signed, public_key1)
    print("Was sent!")
    return encrypted, encypt_signed



#driver code

#згенеруємо дві пари ключів 
private_key1 = generate_random_pairs(var_p, var_q)[0]
public_key1 = generate_random_pairs(var_p, var_q)[1]
private_key2 = generate_random_pairs(var_p1, var_q1)[0]
public_key2 = generate_random_pairs(var_p1, var_q1)[1]

print(f'Private key 1: {private_key1} \n Public key 1  {public_key1} \n Private key 2: {private_key2} \n Public key 2: {public_key2} \n')


#реалізуємо обмін ключів

my_message = random.randint(1, 2 ** 255)
print('MY MESSAGE: ', my_message)

encrypted_msg, encrypted_sgn = rsa_send_key(my_message, private_key1, public_key2, public_key1)

print(encrypted_msg, encrypted_sgn)

message, verified = rsa_receive_key(encrypted_msg, encrypted_sgn, private_key2, public_key2, public_key1 )
print('Decrypted message: ', message)

 

    
   

    



