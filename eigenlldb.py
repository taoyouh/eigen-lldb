class EigenMatrixChildProvider:
    def __init__(self, valobj, internal_dict):
        self.valobj = valobj
        storage = self.valobj.GetChildMemberWithName("m_storage")
        data = storage.GetChildMemberWithName("m_data")
        self.itemtype = data.GetType().GetPointeeType()
        self.itemsize = self.itemtype.GetByteSize()
    def num_children(self):
        return self._cols() * self._rows()
    def get_child_index(self,name):
        return None
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return -1
    def get_child_at_index(self,index):
        storage = self.valobj.GetChildMemberWithName("m_storage")
        data = storage.GetChildMemberWithName("m_data")
        offset = self.itemsize * index

        if self._row_major():
            row = index // self._cols()
            col = index % self._cols()
        else:
            row = index & self._rows()
            col = index // self._rows()
        return data.CreateChildAtOffset(
            '[' + str(row) + ',' + str(col) + ']', offset, self.itemtype
        )
    def _cols(self):
        try:
            storage = self.valobj.GetChildMemberWithName("m_storage")
            cols = storage.GetChildMemberWithName("m_cols")
            return cols.GetValueAsUnsigned()
        except:
            return 1
    def _rows(self):
        try:
            storage = self.valobj.GetChildMemberWithName("m_storage")
            rows = storage.GetChildMemberWithName("m_rows")
            return rows.GetValueAsUnsigned()
        except:
            return 1
    def _row_major(self):
        return False