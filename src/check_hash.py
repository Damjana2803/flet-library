import hashlib

password = "dacika123"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(f"Password: {password}")
print(f"Hash: {hash_value}")

# Compare with stored hash
stored_hash = "164eafefe423186584f48d142dc2d8ed1a33bd937dbb60ba3f82eed1424670a3"
print(f"Stored hash: {stored_hash}")
print(f"Match: {hash_value == stored_hash}")
