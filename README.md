# IODMs

Immutable, content-addressable, reusable

##Definitions

##Objects

DataObjects are immutable and therefore must have a unique, non-reusable "identifier". This differs from the DataObjects current "key" accessed via a collection which can be reused. The key is used to reference the DataObjects identifier, thereby providing immutability constraints. Hashes are preferred because they can be consistently generated from the data itself; this also (TODO: hashes are ideal). For two IODMs to be compliant, the namespace of the algorithms used to generate the identifiers must not conflict.

For example, if I have a "BlogEntries" collection that stores the text of my blog posts, I might have one DataObject with a key that is the blog post title (e.g., "My Summer Project"_ with an identifier equal to the  hash of the data in that entry (e.g., "My summer project was making a bla bla bla"). In this way, I can re-associate the key with a new DataObject (and therefore new identifier; i.e., editing the blog post but keeping the old version) or a new key with the same identifier (i.e., renaming the title of the blog post).  

##Collections

A Collection is the interface to access a uniquely namespaced group of DataObjects. It access its state via snapshot, history via operation logs, and  

```
class Collection():

    def __init__(self, uid=None):
        pass

    def create(self, key, data):
        pass
    
    def read(self, key):
        pass

    def update(self, key, data):
        pass
		
    def replace(self, key, data):
        pass
	
    def delete(self, key):
        pass
	
    def rename(self, original_key, new_key):
        pass
        
    def snapshot(self):
        pass
	
    # ---
		
    def rename_collection(self, new_name):
        pass
    
    def get_identifier(self, key)
        pass
        
```

##Operations
Operations
- 'create'
- 'read'
- 'update'

# snapshot 2015102016210100022 {} 

##Snapshot

key reference timestamp snapshotmd{}

```
class Snapshot:
    def get(self, key):
        return reference, timestamp
    
    def list():
        pass
    
    def build_from_logs()
    
    def build_from_snapshot()
```        

A snapshot is an interface (and optionally datastructure) that stores the state of a collection at a given point in time. Most simply this is a list of keys and DataObject identifiers.