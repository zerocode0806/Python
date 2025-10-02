import itertools
import string
import time

# Function for numeric password brute force attack
def numeric_password_guesser(real_password):
    characters = string.digits  # Only focus on digits (0-9) since it's a numeric password.
    attempts = 0
    
    start_time = time.time()

    # Generate all possible numeric combinations (00000000 to 99999999)
    for guess in itertools.product(characters, repeat=8):
        attempts += 1
        guess_password = ''.join(guess)
        
        # Check if the guessed password matches the real password
        if guess_password == real_password:
            end_time = time.time()
            print(f"\nYour Password '{real_password}' ")
            print(f"Time taken: {end_time - start_time:.2f}")
            print(f"Guessed correctly in {attempts} attempts!")
            return
    
    print("\nYour Password not found.")

# Main logic to check if input is numeric-only
real_password = input("Enter your numeric password: ")

if len(real_password) == 8 and real_password.isdigit():
    print("Using numeric brute-force approach...")
    numeric_password_guesser(real_password)
else:
    print("Please enter a valid 8-digit numeric password.")
