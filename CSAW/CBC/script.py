from pwn import *
from tqdm import tqdm

# Connect to the server
conn = remote('cbc.ctf.csaw.io', 9996)

# Function to test if a given ciphertext is valid
def is_valid_padding(ciphertext):
    conn.sendline(ciphertext)
    response = conn.recvline().decode().strip()
    return "Looks fine" in response

# Function to perform the padding oracle attack
def padding_oracle_attack(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)  # Convert hex string to bytes
    block_size = 16
    num_blocks = len(ciphertext) // block_size

    plaintext = bytearray(len(ciphertext))

    # Iterate over each block (excluding IV, assuming first block is IV)
    for i in range(num_blocks - 1, 0, -1):
        current_block = ciphertext[i * block_size:(i + 1) * block_size]
        previous_block = ciphertext[(i - 1) * block_size:i * block_size]

        intermediate = bytearray(block_size)

        for byte_index in tqdm(range(1, block_size + 1), desc=f"Cracking block {i}"):
            padding_value = byte_index
            # Create modified block with guessed padding
            modified_block = bytearray(block_size)
            for j in range(1, byte_index):
                modified_block[-j] = intermediate[-j] ^ padding_value
            # Brute-force the current byte
            for guess in range(256):
                # print(f"{num_blocks - i - 1}/{num_blocks} {guess}/256")
                modified_block[-byte_index] = guess
                test_block = bytes(modified_block) + current_block

                if is_valid_padding(test_block.hex()):
                    intermediate[-byte_index] = guess ^ padding_value
                    plaintext[(i - 1) * block_size + (-byte_index)] = intermediate[-byte_index] ^ previous_block[-byte_index]

        asdf = plaintext.decode(errors='ignore')

        if "csawctf{" in asdf and "}" in asdf:
            return asdf.strip("\x00")
        else:
            print(asdf.strip("\x00"))

    # Return the reconstructed plaintext
    return plaintext.decode(errors='ignore')


with open('out.txt', 'r') as f:
    ciphertext = f.read().strip()
    
# Run the attack and print the result
decrypted_plaintext = padding_oracle_attack(ciphertext)
with open('decrypted_output.txt', 'w') as f:
    f.write(f"Decrypted plaintext: {decrypted_plaintext}\n")
    print(f"Decrypted plaintext: {decrypted_plaintext}")

# Close the connection
conn.close()
