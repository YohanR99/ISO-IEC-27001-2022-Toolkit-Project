import random
import math
import time
import psutil
import hashlib

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

# Function to calculate signing and verification time and CPU usage
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

# Generate two distinct prime numbers, p and q (large enough for SHA-256)
p, q = generate_prime(10000, 50000), generate_prime(10000, 50000)
while p == q:
    q = generate_prime(10000, 50000)

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

# Function to read a file in binary mode
def read_file_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        exit()

# Prompt user for the file path to sign
file_path = input("Enter the path to the file to sign (e.g., .txt, .pdf): ")

# Read the file content in binary mode
file_content = read_file_binary(file_path)

# Hash the file content using SHA-256
hashed_content = int.from_bytes(hashlib.sha256(file_content).digest(), byteorder='big') % n  # Mod n to avoid large hash

# Sign the file hash using the private key (d, n)
signature, signing_time, signing_cpu = measure_performance(
    lambda hashed_content, d, n: pow(hashed_content, d, n), hashed_content, d, n
)

# Print the signature
print(f"Signature: {signature}")

# Ask if the user wants to verify the signature using the public key
verify_choice = input("Do you want to verify the signature with the public key [y/n]? ").strip().lower()

if verify_choice == 'y':
    # Verify the signature using the public key (e, n)
    def verify_signature(signature, e, n, original_hash):
        verified_hash = pow(signature, e, n)
        return verified_hash == original_hash

    is_verified, verification_time, verification_cpu = measure_performance(
        verify_signature, signature, e, n, hashed_content
    )

    # Print whether the signature is valid or not
    print(f"Signature Verified: {is_verified}")

    # Write signing and verification performance results to a text file
    with open("rsa2performance.txt", "w") as log_file:
        log_file.write(f"Signing Time: {signing_time:.5f} seconds\n")
        log_file.write(f"Signing CPU Usage: {signing_cpu:.2f}%\n")
        log_file.write(f"Verification Time: {verification_time:.5f} seconds\n")
        log_file.write(f"Verification CPU Usage: {verification_cpu:.2f}%\n")
else:
    # Write only signing performance results to a text file
    with open("rsa2performance.txt", "w") as log_file:
        log_file.write(f"Signing Time: {signing_time:.5f} seconds\n")
        log_file.write(f"Signing CPU Usage: {signing_cpu:.2f}%\n")
