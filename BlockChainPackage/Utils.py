from .__init__ import *

def calculateHash(data):
	dataEncoded = data.encode()
	return hashlib.sha256(dataEncoded).hexdigest()

def debug_print(*args,**kwargs):
	if DEBUG_ENABLE:
		print(*args,**kwargs)
