import lldb

class EigenMatrixChildProvider:
    _valobj: lldb.SBValue = None
    _scalar_type: lldb.SBType = None
    _scalar_size: int = None
    _rows_compile_time: int = None
    _cols_compile_time: int = None
    _row_major: bool = None
    _fixed_storage: bool = None

    def __init__(self, valobj, internal_dict):
        self._valobj = valobj
        valtype = valobj.GetType().GetCanonicalType()
        self._scalar_type = valtype.GetTemplateArgumentType(0)
        self._scalar_size = self._scalar_type.GetByteSize()

        name = valtype.GetName()
        template_begin = name.find("<")
        template_end = name.find(">")
        template_args = name[(template_begin + 1):template_end].split(",")
        self._rows_compile_time = int(template_args[1])
        self._cols_compile_time = int(template_args[2])
        self._row_major = (int(template_args[3]) & 1) != 0
        
        max_rows = int(template_args[4])
        max_cols = int(template_args[5])
        self._fixed_storage = (max_rows != -1 and max_cols != -1)
    def num_children(self):
        return self._cols() * self._rows()
    def get_child_index(self,name):
        try:
            indices = name.lstrip("[").rstrip("]").split(",")
            if self._row_major:
                return int(indices[0]) * self._cols() + int(indices[1])
            else:
                return int(indices[1]) * self._rows() + int(indices[0])
        except:
            return -1
    def get_child_at_index(self,index):
        storage = self._valobj.GetChildMemberWithName("m_storage")
        data = storage.GetChildMemberWithName("m_data")
        offset = self._scalar_size * index

        if self._row_major:
            row = index // self._cols()
            col = index % self._cols()
        else:
            row = index % self._rows()
            col = index // self._rows()
        if self._fixed_storage:
            data = data.GetChildMemberWithName("array")
        return data.CreateChildAtOffset(
            '[' + str(row) + ',' + str(col) + ']', offset, self._scalar_type
        )
    def _cols(self):
        if self._cols_compile_time == -1:
            storage = self._valobj.GetChildMemberWithName("m_storage")
            cols = storage.GetChildMemberWithName("m_cols")
            return cols.GetValueAsUnsigned()
        else:
            return self._cols_compile_time
    def _rows(self):
        if self._rows_compile_time == -1:
            storage = self._valobj.GetChildMemberWithName("m_storage")
            rows = storage.GetChildMemberWithName("m_rows")
            return rows.GetValueAsUnsigned()
        else:
            return self._rows_compile_time
