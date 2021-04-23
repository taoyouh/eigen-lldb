import lldb

class EigenMatrixChildProvider:
    valobj: lldb.SBValue = None
    scalar_type: lldb.SBType = None
    scalar_size: int = None
    rows_compile_time: int = None
    cols_compile_time: int = None
    options: int = None

    def __init__(self, valobj, internal_dict):
        self.valobj = valobj
        storage = self.valobj.GetChildMemberWithName("m_storage")
        data = storage.GetChildMemberWithName("m_data")
        self.scalar_type = data.GetType().GetPointeeType()
        self.scalar_size = self.scalar_type.GetByteSize()

        name = self.valobj.GetType().GetCanonicalType().GetName()
        template_begin = name.find("<")
        template_end = name.find(">")
        template_args = name[(template_begin + 1):template_end].split(",")
        self.rows_compile_time = int(template_args[1])
        self.cols_compile_time = int(template_args[2])
        self.options = int(template_args[3])
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
        offset = self.scalar_size * index

        if self._row_major():
            row = index // self._cols()
            col = index % self._cols()
        else:
            row = index % self._rows()
            col = index // self._rows()
        return data.CreateChildAtOffset(
            '[' + str(row) + ',' + str(col) + ']', offset, self.scalar_type
        )
    def _cols(self):
        if self.cols_compile_time == -1:
            storage = self.valobj.GetChildMemberWithName("m_storage")
            cols = storage.GetChildMemberWithName("m_cols")
            return cols.GetValueAsUnsigned()
        else:
            return self.cols_compile_time
    def _rows(self):
        if self.rows_compile_time == -1:
            storage = self.valobj.GetChildMemberWithName("m_storage")
            rows = storage.GetChildMemberWithName("m_rows")
            return rows.GetValueAsUnsigned()
        else:
            return self.rows_compile_time
    def _row_major(self):
        return (self.options & 1) != 0