import hashlib
import random
import time

# 生成随机私钥
def generate_private_key():
    return random.randint(1, 2**256)

# 生成公钥
def generate_public_key(private_key):
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    sha256_hash = hashlib.sha256(private_key_bytes).digest()
    return int.from_bytes(sha256_hash, byteorder='big')

# 生成签名
def generate_signature(private_key, message_hash):
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    message_bytes = message_hash.to_bytes(32, byteorder='big')
    message_signature = hashlib.sha256(private_key_bytes + message_bytes).digest()
    return int.from_bytes(message_signature, byteorder='big')

# 验证签名
def verify_signature(public_key, message_hash, signature):
    public_key_bytes = public_key.to_bytes(32, byteorder='big')
    message_bytes = message_hash.to_bytes(32, byteorder='big')
    signature_bytes = signature.to_bytes(32, byteorder='big')
    message_signature = hashlib.sha256(public_key_bytes + message_bytes).digest()
    return message_signature == signature_bytes

# 批量验证签名
def batch_verify_signature(public_keys, message_hashes, signatures):
    if len(public_keys) != len(message_hashes) or len(public_keys) != len(signatures):
        return False
    
    aggregated_public_key = sum(public_keys) % (2**256)
    aggregated_message_hash = sum(message_hashes) % (2**256)
    aggregated_signature = sum(signatures) % (2**256)
    
    return verify_signature(aggregated_public_key, aggregated_message_hash, aggregated_signature)

# 示例用法
def main():
    # 生成3个随机私钥
    s=time.time()
    private_key_1 = generate_private_key()
    private_key_2 = generate_private_key()
    private_key_3 = generate_private_key()
    
    # 生成对应的公钥
    public_key_1 = generate_public_key(private_key_1)
    public_key_2 = generate_public_key(private_key_2)
    public_key_3 = generate_public_key(private_key_3)
    
    # 生成3个随机消息哈希
    message_hash_1 = random.randint(1, 2**256)
    message_hash_2 = random.randint(1, 2**256)
    message_hash_3 = random.randint(1, 2**256)
    
    # 分别生成3个签名
    signature_1 = generate_signature(private_key_1, message_hash_1)
    signature_2 = generate_signature(private_key_2, message_hash_2)
    signature_3 = generate_signature(private_key_3, message_hash_3)
    
    # 构建公钥、消息哈希和签名的列表
    public_keys = [public_key_1, public_key_2, public_key_3]
    message_hashes = [message_hash_1, message_hash_2, message_hash_3]
    signatures = [signature_1, signature_2, signature_3]
    
    # 批量验证签名
    result = batch_verify_signature(public_keys, message_hashes, signatures)
    e=time.time()
    print("批量验证签名结果：", result)
    print("the time used:",e-s)

if __name__ == "__main__":
    main()
