import kasumi 

#https://www.cosic.esat.kuleuven.be/nessie/testvectors/

key = 0x20000000000000000000000000000000
text = 0x0000000000000000

test = kasumi.Kasumi()
test.KeySchedule(key)

print("Plaintext: ", hex(text))
encrypted = test.enc(text)
print("Cipher Text: ", hex(encrypted))

decrypted = test.dec(encrypted)
print("PlainText: ", hex(decrypted))
