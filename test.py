from merkle_json import MerkleJson

mj = MerkleJson()

obj = {
    'keyD': 1,
    'keyA': 2,
    'keyC': [4, 3],
    'keyB': 4,
}
print(obj)  # '{'keyD': 1, 'keyA': 2, 'keyC': [4, 3], 'keyB': 4}'

mj = MerkleJson()
s_obj = mj.stringify(obj)
print(s_obj)  # '{"keyA":2,"keyB":4,"keyC":3,"keyD":1}'

# they should not be null as s_obj has been sorted
assert not obj == s_obj


mjHash = mj.hash(obj)
print(mjHash)  # '7001bd2b415e6a624a23d7bc7c249b21'

# obj_unordered is the same object than obj however it contains different order of the keys
obj_unordered = {
    'keyC': [3, 4],
    'keyA': 2,
    'keyB': 4,
    'keyD': 1,
}
mjUnsHash = mj.hash(obj_unordered)
print(mjUnsHash)  # '7001bd2b415e6a624a23d7bc7c249b21'

# should be the same even if the key order is different, or the objects in lists are not ordered
assert mjUnsHash == mjHash


new_obj = {
    'key1': 'something',
    'key2': 'otherthing'
}
mj = MerkleJson()
mjHash = mj.hash(new_obj, cached=True)  # cached = True by default
print(mjHash)  # 'ff55be553d7bcfbf6233891554378ddd'

new_obj = {
    'key1': 'something',
    'key2': 'otherthing',
    'merkleHash': 'my_hash',
    'merkleHash2': 'my_valid_hash'
}
mj = MerkleJson(ignoreKeys=['merkleHash2'])
mjHash = mj.hash(new_obj, cached=False)  # cached = True by default
print(mjHash)  # 'ff55be553d7bcfbf6233891554378ddd'
ex_mjHash = mj.hash(new_obj)  # cached = True by default
print(ex_mjHash)  # 'my_hash'

# should be different as ex_mjHash should return the hash from the tag
assert not mjHash == ex_mjHash


mj = MerkleJson(hashTag='merkleHash2')
# cached = True by default but now the value of merkleHash2 will be retured as defined in hashTag parameter
mjHash = mj.hash(new_obj)
print(mjHash)  # 'my_valid_hash'

assert 'my_valid_hash' == mjHash


# let say you want to ignore 'key2'
new_obj = {
    'key1': 'something',
    'key2': 'otherthing'  # ignored
}
obj_without_key2 = {
    'key1': 'something'
}
mj = MerkleJson(ignoreKeys=['key2'])
mjHash = mj.hash(new_obj)
print(mjHash)  # '95f6d042c35c1cedc7e3dea0a255c332'
mjHash2 = mj.hash(obj_without_key2)
print(mjHash2)  # '95f6d042c35c1cedc7e3dea0a255c332'
assert (mjHash == mjHash2)


# nested
obj = {
    'keyD': 1,
    'keyA': 2,
    'keyC': [[4, 75], 3.2],
    'keyB': 4,
}
new_obj = {
    'keyC': [3.2, [75, 4]],  # changed order here
    'keyA': 2,
    'keyB': 4,
    'keyD': 1,
}
mj = MerkleJson()
assert mj.hash(obj) == mj.hash(new_obj)


obj = {
    'keyD': [
        {
            'somekey': [7, 88, 22],
            'otherkey': {
                'OK': 1
            }
        },
        {
            'someList': []
        }
    ],
    'keyA': 2,
    'keyC': [[4, 75], 3.2],
    'keyB': 4,
}
new_obj = {
    'keyC': [3.2, [75, 4]],
    'keyA': 2,
    'keyB': 4,
    'keyD': [
        {# changed order here
            'otherkey': {   
                'OK': 1
            },
            'somekey': [22, 7, 88],  # changed order here

        },
        {
            'someList': []
        }
    ],
}
mj = MerkleJson()
assert mj.hash(obj) == mj.hash(new_obj)


k = [{
    'test' : None,
    'test2': 1
}]

l = [{
    'test2': 1
}]


assert mj.hash(k, cached=False, ignoreNulls=True) == mj.hash(l, cached=False, ignoreNulls=False)
assert not mj.hash(k, cached=False, ignoreNulls=False) == mj.hash(l, cached=False, ignoreNulls=False)

assert mj.hash(l, cached=False, ignoreNulls=True) == mj.hash(l, cached=False, ignoreNulls=False)
assert mj.hash(l, cached=False) == mj.hash(l, cached=False, ignoreNulls=False)
assert mj.hash(k, cached=False) == mj.hash(k, cached=False, ignoreNulls=False)

print('All tests passed!')