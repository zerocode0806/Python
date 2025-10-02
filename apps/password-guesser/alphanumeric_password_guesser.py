import itertools
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of common passwords for dictionary attack
common_passwords = ["password", "123456", "123456789", "qwerty", "abc123", "password1", "111111", "letmein"]

# Function to perform dictionary attack
def dictionary_attack(real_password):
    # Try guessing from a dictionary of common passwords
    for common_password in common_passwords:
        if common_password == real_password:
            return common_password
    return None

# Optimized brute force function that works with threads
def brute_force_guess_threaded(real_password, charset, length_range):
    attempts = 0
    for length in range(length_range[0], length_range[1] + 1):  # Attempt password lengths within the given range
        for guess in itertools.product(charset, repeat=length):
            guess_password = ''.join(guess)
            attempts += 1
            if guess_password == real_password:
                return guess_password, attempts
    return None, attempts

# Optimized password guessing using multi-threading
def password_guesser(real_password, max_length=8):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits  # Optimized charset

    # First, try a dictionary attack
    print("\nStarting dictionary attack...")
    start_time = time.time()
    dictionary_result = dictionary_attack(real_password)

    if dictionary_result:
        end_time = time.time()
        print(f"\nPassword '{real_password}' guessed using dictionary attack!")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return

    # If dictionary attack fails, use brute force with threads
    print("\nDictionary attack failed. Starting brute force attack...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust `max_workers` for more parallel threads
        futures = []
        # Split the work among threads by dividing password length ranges
        for i in range(1, max_length + 1, 2):  # Attempt lengths in ranges (e.g., length 1-2, 3-4, etc.)
            futures.append(executor.submit(brute_force_guess_threaded, real_password, characters, (i, i+1)))

        # Collect the results as they complete
        for future in as_completed(futures):
            result, attempts = future.result()
            if result:
                end_time = time.time()
                print(f"\nPassword '{real_password}' guessed correctly in {attempts} attempts!")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                return

    print("\nPassword not found.")

# Main logic for alphanumeric password guessing
real_password = input("Enter your alphanumeric password: ")

print("Using optimized brute-force approach...")
password_guesser(real_password, max_length=len(real_password))
