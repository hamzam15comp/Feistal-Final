import sys


def startEncryption(message, key):
    times, words = seperateMessage(checkLength(message))
    enc = ""
    for i in range(times):
        enc += encrypt(words[i], key)
    #print "Encrypted message:",enc
    return enc
    #startDecryption(enc, key)


def startDecryption(message, key):
    times, words = seperateMessage(message)
    dec = ""
    for i in range(times):
        dec += decrypt(words[i], key)
    #print "Decrypted message:",dec
    return dec


#input from user: key of 16 bits.
def getKey():
    key = ""
    while True:
        key = raw_input("Enter your 16 character key: ")
        if len(key) == 16:
            break
        print "Please enter 16 characters only"
    return key


#If not a multiple of 8 will pad the message with with spaces
def checkLength(message):
    length = len(message) % 8
    if length % 8 == 0:
        pass
    else:
        add = 8 - length
        for i in range(add):
            message += " "
    return message


#counts number of blocks of 8 and also returns a list of 8 byte chunks
def seperateMessage(message):
    n = 8
    times = len(message) / 8
    words = [message[i:i + 8] for i in range(0, len(message), n)]
    return times, words
    

#For key generation, alternate characters are getting incremented and the rest are getting decremented.
def encrypt(message, key):
    left = message[:4]
    right = message[4:]
    for i in range(16):
	#print("Round {0}".format(i))
	tmp = ""
	for j in range(16):
		if j % 2 == 0:
			tmp += chr(ord(key[j]) + 1)
		else:
			tmp += chr(ord(key[j]) - 1)
	key = tmp
	RKbin = ' '.join(format(ord(x), 'b') for x in key[:4])
	Rightbin = ' '.join(format(ord(x), 'b') for x in right)
	Leftbin = ' '.join(format(ord(x), 'b') for x in left)
	#print("RKey{0:1d} = {1} {2}".format(i, key[:4], RKbin))
	#print("Right = {0} {1}".format(right, Rightbin))
	#print("Left  = {0} {1}".format(left, Leftbin))
        afterF = roundFunction(right, key)
        result = performXOR(left, afterF)
        left = right
        right = result
    return right + left


def decrypt(message, key):
    right = message[:4]
    left = message[4:]
    tmp = ""
    for j in range(16):
	if j % 2 == 0:
		tmp += chr(ord(key[j]) + 17)
	else:
		tmp += chr(ord(key[j]) - 17)
    key = tmp
    for i in range(15, -1, -1):
	tmp = ""
	for j in range(16):
                if j % 2 == 0:
                        tmp += chr(ord(key[j]) - 1)
                else:
                        tmp += chr(ord(key[j]) + 1)
	key = tmp
        afterF = roundFunction(left, key)
        result = performXOR(right, afterF)
        right = left
        left = result
    return left + right


#In XOR function, negation of the right string is being done.
def performXOR(left, right):
    result = ""
    for i in range(4):
        num = (ord(left[i]) ^ ord(right[i]))
	convert = chr(num)
        result += convert
    return result


#In round function, key is being rotated by 8 steps.
def roundFunction(message, key):
    keyL = list(key)
    keyL = keyL[8:] + keyL[:8]
    key = "".join(keyL)
    return performXOR(message[2:] + message[:2], key)


def main():
	if len (sys.argv) != 4 :
		print "Usage:python FeistalCode.py <e/d> <inputfile.txt> <outputfile.txt>"
		sys.exit (1)
	arguments = sys.argv[1:]
	try:
		f = open(arguments[1], 'r')
	except Exception:
		print "Usage:python FeistalCode.py <e/d> <inputfile.txt> "
		sys.exit (1)
	message = f.read().rstrip('\n')
	f.close()
	CipherText = ""
	PlainText = ""
	key = "ABCDEFGHIJKLMNOP"#getKey() Hardcoding key for now
	try:	
		f = open(arguments[2], 'w')
	except Exception :
		print "Unable to generate Output file"
		sys.exit (1)

	if arguments[0] == "e":
		CipherText = startEncryption(message, key)
		f.write(CipherText)
		print ("\n\nCipherText : {0}\n\n".format(CipherText))
	elif arguments[0] == "d":
		if len(message) % 8 == 1:
			print "Message wrong length, please check again"
		else:
			PlainText = startDecryption(message, key)
			print PlainText
			f.write(PlainText)

	f.close()

if __name__ == '__main__':
    main()

#Extraaa

#To encrypt of decrypt input from user.
#def getMode(mode):
#        #mode = raw_input("Enter the mode (e/d): ")
#	if mode == 'e' or mode == 'd':
#		return mode
#        else :
#		print "Usage:python FeistalCode.py <e/d> <inputfile.txt> "
#		sys.exit (1)
	
#	message = raw_input("Enter Message: ")
#	mode = getMode(arguments[0])
#	if mode.lower() == "e":
#		startEncryption(message, key)
#	elif mode.lower() == "d":
#		if len(message) % 8 == 1:
#			print "Message wrong length, please check again"
#		else:
#			startDecryption(message, key)
        

