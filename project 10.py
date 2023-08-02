import ecdsa
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import NIST256p
import hashlib
import time

s=time.time()
# 生成私钥
private_key = SigningKey.generate(curve=NIST256p)
private_key_hex = private_key.to_string().hex()

# 生成公钥
public_key = private_key.get_verifying_key()
public_key_hex = public_key.to_string().hex()

# 生成地址
address = hashlib.sha3_256(public_key.to_string().hex().encode('utf-8')).hexdigest()[24:]

# 消息签名
message = "Hello, Ethereum!"
signature = private_key.sign(message.encode('utf-8'))

# 验证签名
is_valid = public_key.verify(signature, message.encode('utf-8'))
e=time.time()

print("Private Key:", private_key_hex)
print("Public Key:", public_key_hex)
print("Address:", address)
print("Signature:", signature.hex())
print("Is Valid:", is_valid)
print("the time used:",e-s)
