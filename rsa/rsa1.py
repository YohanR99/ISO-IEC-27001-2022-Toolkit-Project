import random
import math
import time
import psutil  # For CPU usage monitoring

# Function to check if a number is prime
def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
    return True

# Function to generate a prime number within a given range
def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

# Function to calculate modular inverse using Extended Euclidean Algorithm
def mod_inverse(e, phi):
    return pow(e, -1, phi)

# Function to calculate encryption time and CPU usage
def measure_performance(func, *args):
    # Start measuring time and CPU usage
    start_time = time.time()
    psutil.cpu_percent(interval=None)  # Discard the first reading

    result = func(*args)

    # End measuring time and CPU usage
    end_time = time.time()
    # Measure CPU usage over a small interval to avoid negative values
    cpu_usage = psutil.cpu_percent(interval=0.1)

    execution_time = end_time - start_time

    return result, execution_time, cpu_usage

# Generate two distinct prime numbers, p and q
p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)
while p == q:
    q = generate_prime(1000, 5000)

# Calculate n and φ(n)
n = p * q
phi_n = (p - 1) * (q - 1)

# Select e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
e = random.randint(3, phi_n - 1)
while math.gcd(e, phi_n) != 1:
    e = random.randint(3, phi_n - 1)

# Calculate d (private key) such that e*d ≡ 1 (mod φ(n))
d = mod_inverse(e, phi_n)

# Display public and private keys and modulus
print(f"Public Key: {e}")
print(f"Private Key: {d}")
print(f"n: {n}")
print(f"p: {p}, q: {q}")

# Prompt user for input message to encrypt
message = input("Enter the plaintext message to encrypt with public key: ")

# Encrypt the message using public key (e, n)
message_encoded = [ord(char) for char in message]  # Convert message to integer list (Unicode values)

# Measure encryption time and CPU usage
ciphertext, encryption_time, encryption_cpu = measure_performance(
    lambda message_encoded, e, n: [pow(char, e, n) for char in message_encoded], message_encoded, e, n
)

# Print the ciphertext
print(f"Ciphertext: {ciphertext}")

# Ask if user wants to decrypt the message with private key
decrypt_choice = input("Do you want to decrypt the message with private key [y/n]? ").strip().lower()

if decrypt_choice == 'y':
    # Decrypt the message using private key (d, n)
    # Measure decryption time and CPU usage
    decrypted_message, decryption_time, decryption_cpu = measure_performance(
        lambda ciphertext, d, n: [pow(char, d, n) for char in ciphertext], ciphertext, d, n
    )

    decrypted_text = "".join(chr(char) for char in decrypted_message)  # Convert decrypted integers back to text

    # Print the decrypted message
    print(f"Decrypted message: {decrypted_text}")

    # Write performance results to a text file
    with open("rsa1performance.txt", "w") as log_file:
        log_file.write(f"Encryption Time: {encryption_time:.5f} seconds\n")
        log_file.write(f"Encryption CPU Usage: {encryption_cpu:.2f}%\n")
        log_file.write(f"Decryption Time: {decryption_time:.5f} seconds\n")
        log_file.write(f"Decryption CPU Usage: {decryption_cpu:.2f}%\n")
else:
    # Write encryption performance results to a text file only
    with open("rsa1performance.txt", "w") as log_file:
        log_file.write(f"Encryption Time: {encryption_time:.5f} seconds\n")
        log_file.write(f"Encryption CPU Usage: {encryption_cpu:.2f}%\n")
