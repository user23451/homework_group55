import hashlib
import math
import time

class IMPLMerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.tree = []

    def build_tree(self):
        if len(self.leaves) == 0:
            return None
        
        self.tree = [None] * (2 * len(self.leaves) - 1)
        self._build_tree_recursive(self.leaves, 0, len(self.leaves) - 1, 0)

    def _build_tree_recursive(self, leaves, start, end, index):
        if start == end:
            leaf_hash = self._hash_leaf(leaves[start])
            self.tree[index] = leaf_hash
            return leaf_hash
        
        mid = (start + end) // 2
        left_child_hash = self._build_tree_recursive(leaves, start, mid, 2 * index + 1)
        right_child_hash = self._build_tree_recursive(leaves, mid + 1, end, 2 * index + 2)
        
        node_hash = self._hash_children(left_child_hash, right_child_hash)
        self.tree[index] = node_hash

        return node_hash

    def _hash_leaf(self, leaf):
        return hashlib.sha256(leaf.encode()).hexdigest()

    def _hash_children(self, left_child_hash, right_child_hash):
        combined_hash = bytes.fromhex(left_child_hash) + bytes.fromhex(right_child_hash)
        return hashlib.sha256(combined_hash).hexdigest()

    def get_root_hash(self):
        if len(self.tree) == 0:
            return None
        
        return self.tree[0]

    def create_proof(self, leaf_index):
        if not 0 <= leaf_index < len(self.leaves):
            return None
        
        proof = []
        self._create_proof_recursive(leaf_index, 0, len(self.leaves) - 1, 0, proof)
        
        return proof

    def _create_proof_recursive(self, leaf_index, start, end, index, proof):
        if start == end:
            return
        
        mid = (start + end) // 2
        
        if leaf_index <= mid:
            proof.append((self.tree[2 * index + 2], 'L'))
            self._create_proof_recursive(leaf_index, start, mid, 2 * index + 1, proof)
        else:
            proof.append((self.tree[2 * index + 1], 'R'))
            self._create_proof_recursive(leaf_index, mid + 1, end, 2 * index + 2, proof)

    def verify_proof(self, leaf_hash, leaf_index, proof):
        if not 0 <= leaf_index < len(self.leaves):
            return False
        
        current_hash = leaf_hash
        for i in range(len(proof)):
            node_hash, position = proof[i]
            if position == 'L':
                combined_hash = bytes.fromhex(current_hash) + bytes.fromhex(node_hash)
            else:
                combined_hash = bytes.fromhex(node_hash) + bytes.fromhex(current_hash)
            
            current_hash = hashlib.sha256(combined_hash).hexdigest()
        
        return current_hash == self.tree[0]

s=time.time()
# 创建叶子节点列表
leaves = ['Leaf1', 'Leaf2', 'Leaf3', 'Leaf4']

# 创建IMPL Merkle Tree对象
tree = IMPLMerkleTree(leaves)

# 建立树
tree.build_tree()

# 获取根哈希
root_hash = tree.get_root_hash()
print("根哈希:", root_hash)

# 创建证明
leaf_index = 2
proof = tree.create_proof(leaf_index)
print("叶子节点", leaves[leaf_index], "的证明:", proof)

# 验证证明
leaf_hash = tree._hash_leaf(leaves[leaf_index])  # 或者使用外部生成的叶子节点哈希
is_valid = tree.verify_proof(leaf_hash, leaf_index, proof)
print("验证结果:", is_valid)
e=time.time()
print("the time used:",e-s)


#通信
import socket

# 创建客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 服务器地址和端口号
server_address = ('127.0.0.1', 8888)

try:
    # 连接到服务器
    client_socket.connect(server_address)
    print('成功连接到服务器')
    
    # 构造协议数据（根据RFC 6962）
    protocol_data = "your_protocol_data"  # 根据具体协议定义，构造相应的数据
    
    # 发送协议数据给服务器
    client_socket.sendall(protocol_data.encode())
    print('已发送协议数据给服务器')
    
    # 接收来自服务器的响应
    response = client_socket.recv(1024)
    print(f'服务器响应： {response.decode()}')
    
except ConnectionError as e:
    print(f'连接错误：{e}')
    
finally:
    # 关闭客户端连接
    client_socket.close()
    print('客户端连接已关闭')
