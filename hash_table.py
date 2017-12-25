from graphviz import Digraph

class HashTable:
    def __init__(self, hash_function, max_load_factor, bucket_count=4):
        self.hash = hash_function
        self.max_load_factor = max_load_factor
        self.buckets = [HashTableEntry() for i in range(bucket_count)]
        self.entry_count = 0
    def insert(self, value):
        bc = len(self.buckets)
        if load_factor(self.entry_count + 1, bc) >\
                self.max_load_factor:
            og_buckets = self.buckets
            self.buckets = [HashTableEntry() for i in range(bc * 2)]
            for b in og_buckets:
                for e in b:
                    if e.value is not None:
                        self.insert(e.value)
        self.entry_count += 1
        self.buckets[self.hash(value) % bc].insert(value)
    def gv_serialize(self):
       t = Digraph()
       arr_label = '<0> 0'
       for i in range(1, len(self.buckets)):
           arr_label += '| <{}> {} '.format(str(i), str(i))
       t.node('arr', arr_label, shape='record')
       for i in range(len(self.buckets)):
           prev = 'arr:{}'.format(str(i))
           for e in self.buckets[i]:
               if e.value is None:
                   break
               t.node(str(id(e)), e.value)
               t.edge(prev, str(id(e)))
               prev = str(id(e))
       return t.source

def load_factor(entry_count, bucket_count):
    return entry_count / bucket_count

def djb2_hash(s):
    h = 5381
    for i in range(len(s)):
        h = ((h << 5) + h) + ord(s[i])
    return h

class HashTableEntry:
    def __init__(self, value=None):
        self.next = None
        self.value = value
    def has_value(self, value):
        if self.value is None or self.next is None:
            return False
        if self.value == value:
            return True
        return self.next.has_value(value)
    def insert(self, value):
        if self.value == value:
            return
        elif self.value is None:
            self.value = value
            return
        elif self.next is None:
            self.next = HashTableEntry(value)
            return
        else:
            self.next.insert(value)
    def __getitem__(self, key):
        n = self
        while key != 0:
            if n.value is None or n.next is None:
                raise IndexError
            n = n.next
            key -= 1
        return n
