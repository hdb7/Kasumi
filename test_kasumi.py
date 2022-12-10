import kasumi 

key = 0x9900aabbccddeeff1122334455667788
# text = 0xfedcba0987654321
text = 0x68656c6c6f20
# text = 114784820031264
print("Plaintext: ", text)
# print(text)
# print(type(text))
test = kasumi.Kasumi()
test.KeySchedule(key)

print("Plaintext: ", hex(text))
encrypted = test.enc(text)
print("Cipher Text: ", hex(encrypted))

decrypted = test.dec(encrypted)
print("PlainText: ", hex(decrypted))
