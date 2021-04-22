class MyStorageChildProvider:
    def __init__(self, valobj, internal_dict):
        self.valobj = valobj
        print(valobj)
        storage = valobj.GetChildMemberWithName("storage")
        print(storage)
    def num_children(self):
        pass
    def get_child_index(self,name):
        pass
    def get_child_at_index(self,index):
        pass
   