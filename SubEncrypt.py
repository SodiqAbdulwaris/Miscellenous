import random, string

chars = list(string.punctuation + string.digits + string.ascii_letters + " ")
key = chars.copy()
random.shuffle(key)


# print(chars)
# print(key)

# user_input = str(input("Type something here: "))
# cipher_text = ""

# for letter in user_input:
#     ind = chars.index(letter)

#     cipher_text += key[ind]
# print(f"your cipher is {cipher_text}")

cipher_text = input("Enter a message to encrypt: ")
plain_text = ""

for letter in cipher_text:
    inde = key.index(letter)
    plain_text += chars[inde]

print(f"encrypted message: {cipher_text}")
print(f"original message : {plain_text}")
