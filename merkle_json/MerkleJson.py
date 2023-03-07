import hashlib
import json

class MerkleJson:

    def __init__(self, hashTag = 'merkleHash', ignoreKeys = []):
        self.hashTag = hashTag
        self.ignoreKeys = ignoreKeys
        self.ignoreKeys.append(hashTag)
     
     
    def hash(self, value, cached = True, ignoreNulls = False):
        if isinstance(value, str):
            return hashlib.md5(value.encode('utf-8')).hexdigest()
        elif isinstance(value, list):
            acc = ""
            h_acc = []
            for v in value:
                #acc += self.hash(v, cached)
                h_acc.append(self.hash(v, cached, ignoreNulls)) 
                
            acc = acc.join(sorted(h_acc))
            return self.hash(acc, cached, ignoreNulls)
        elif isinstance(value, int):
            value = str(value)
            return self.hash(value)
        elif isinstance(value, bool):
            return self.hash(str(value))
        elif isinstance(value, type(None)):
                return self.hash(str(value), ignoreNulls=ignoreNulls)
        elif isinstance(value, type):
            return self.hash(str(value))
        elif isinstance(value, dict):
            if cached and value.get(self.hashTag):
                return value[self.hashTag]
            keys = sorted(value.keys())
            acc = ""
            for k in keys:
                #if k == self.hashTag: #ignore keys
                if k in self.ignoreKeys:
                    continue

                keyVal = value[k]
                if ignoreNulls and (keyVal == None):
                    continue

                acc += f"{k}:{self.hash(keyVal, ignoreNulls=ignoreNulls)},"
            return self.hash(acc, ignoreNulls=ignoreNulls)
        elif isinstance(value, (float, complex)):
            #raise ValueError("hash() not supported: " + str(type(value)))
            return self.hash(str(value))
        else:
            return self.hash(str(value), ignoreNulls=ignoreNulls)

    def stringify(self, value):
        if isinstance(value, list):
            body = ""
            for v in value:
                if body:
                    body += ","
                body += self.stringify(v)
            return f"[{body}]"
        elif isinstance(value, dict):
            if hasattr(value, "toJSON") and callable(value.toJSON):
                value = json.loads(json.dumps(value))
            keys = sorted(value.keys())
            body = ""
            for k in keys:
                if body:
                    body += ","
                body += f'"{k}":{self.stringify(value[k])}'
            return f"{{{body}}}"
        elif isinstance(value, bool):
            return json.dumps(value)
        elif isinstance(value, type(None)):
            return json.dumps(value)
        elif isinstance(value, (int, float, complex)):
            return json.dumps(value)
        elif isinstance(value, str):
            return json.dumps(value)
        elif isinstance(value, (bytes, bytearray)):
            return json.dumps(value.decode('utf-8'))
        elif isinstance(value, (set, frozenset)):
            raise ValueError("stringify() not supported: " + str(type(value)))
        elif isinstance(value, type):
            return json.dumps(str(value))
        elif isinstance(value, (object,)):
            return json.dumps(str(value))
        else:
            raise ValueError("stringify() not supported: " + str(type(value)))