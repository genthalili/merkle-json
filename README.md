# MerkleJson
Generates a unique hash for a json or dict object. In this way you can guarantee the consistency of your json object quickly and easily by storing a unique hash which would act as a certificate signature.

MerkleJson guarantees the unique hash, regardless of the order of the json objects in a list. Also it detects if an merkle hash already exists in the object which avoids re-calculations. Furthermore, you can keep the consistency of the object only partially, by ignoring other irrelevant keys.
## Installation 

````
pip install merkle-json
````

## Usage
````py
from merkle_json import MerkleJson

#init the object
mj = MerkleJson()

#... your code here

````

### Serialize JSON object :
Unlike JSON, MerkleJson serializes objects canonically.

```py
obj = {
    'keyD': 1,
    'keyA': 2,
    'keyC': [4,3],
    'keyB': 4,
}
print(obj) # '{'keyD': 1, 'keyA': 2, 'keyC': [4, 3], 'keyB': 4}'

mj = MerkleJson()
mj.stringify(obj) # '{"keyA":2,"keyB":4,"keyC":3,"keyD":1}'

```

### Generate unique hash of JSON object :
````py
mj = MerkleJson()
mjHash = mj.hash(obj)
print(mjHash) # '7001bd2b415e6a624a23d7bc7c249b21'

# obj_unordered is the same object than obj however it contains different order of the keys
obj_unordered = {
    'keyC': [3,4],
    'keyA': 2,
    'keyB': 4,
    'keyD': 1,
}
mj.hash(obj_unordered) # '7001bd2b415e6a624a23d7bc7c249b21'
````
As you can see they both return the same merkle hash value.
In python when comparing both objects you will get a `False` to `obj == obj_unordered` due to the array which has a different order `[4,3] != [3,4]`.

### If `merkleHash` (default key) is present then the calculation will not be performed (by default `cached = True`) :
````py
new_obj = {
    'key1': 'something',
    'key2': 'otherthing'
}
mj = MerkleJson()
mjHash = mj.hash(new_obj, cached = True) # cached = True by default
print(mjHash) # 'ff55be553d7bcfbf6233891554378ddd'

new_obj = {
    'key1': 'something',
    'key2': 'otherthing',
    'merkleHash': 'my_hash',
    'merkleHash2' : 'my_valid_hash'
}
mj = MerkleJson(ignoreKeys=['merkleHash2'])  #ignore merkleHash2 to be ignored
mjHash = mj.hash(new_obj, cached = False) # cached = True by default
print(mjHash) # 'ff55be553d7bcfbf6233891554378ddd'
mjHash = mj.hash(new_obj) # cached = True by default
print(mjHash) # 'my_hash'

````
### You can get the hash which is stored in a different key by using ``hashTag`` parameter :
````py
mj = MerkleJson(hashTag= 'merkleHash2')
mjHash = mj.hash(new_obj) # cached = True by default but now the value of merkleHash2 will be returned as defined in hashTag parameter
print(mjHash) # 'my_valid_hash'
````

### Ignore specific key in the object with the parameter `ignoreKeys` :
This way you can keep the consistency of the object partially.
````py
#let say you want to ignore 'key2'
new_obj = {
    'key1': 'something',
    'key2': 'otherthing' #ignored
}
obj_without_key2 = {
    'key1': 'something'
}
mj = MerkleJson(ignoreKeys = ['key2'])
mjHash = mj.hash(new_obj) # 
print(mjHash) # '95f6d042c35c1cedc7e3dea0a255c332'
mjHash2 = mj.hash(obj_without_key2) # 
print(mjHash2) # '95f6d042c35c1cedc7e3dea0a255c332'
print(mjHash == mjHash2) # True
````

### Ignore keys with `None` values by setting `ignoreNulls = True` when calling the ``hash()`` function :
````py
k = [{
    'test' : None,
    'test2': 1
}]

l = [{
    'test2': 1
}]
print(mj.hash(k)) # prints 0cf3a78d7746983efea449bf54fa8664
print(mj.hash(k, ignoreNulls=True)) # prints c9153ef54418f96e7937f25be9a8c27f
print(mj.hash(l)) # prints c9153ef54418f96e7937f25be9a8c27f
````

## License

[MIT](LICENSE)

## Credit

The project was inspired by :
- Merkle Tree
- Similar package/project in javascript : [merkle-json](https://github.com/oyamist/merkle-json)

## Merkle Tree
Merkle Trees, also known as hash trees, are a data structure used to efficiently verify the integrity of large datasets. They were named after Ralph Merkle, who first proposed the idea in a 1979 paper.

A Merkle Tree works by recursively hashing pairs of data until a single hash value, known as the root hash or Merkle root, is produced. Each level of the tree represents a different layer of hashes, with the root hash at the top. The leaf nodes of the tree contain the original data or hashed values.

One of the main advantages of Merkle Trees is their ability to efficiently verify the integrity of large datasets without having to hash the entire dataset. Instead, by hashing only the nodes along the path from the data to the root, a Merkle proof can be generated which proves that the data is part of the larger dataset without revealing any other information about the dataset.

Merkle Trees are commonly used in peer-to-peer networks, such as blockchain technology, to ensure the integrity of the data stored in the network. They are also used in other applications such as file sharing and digital signatures.
