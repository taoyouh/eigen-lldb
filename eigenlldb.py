import lldb
from typing import List

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand("type synthetic add -x Eigen::Matrix<.*> --python-class eigenlldb.EigenMatrixChildProvider")
    debugger.HandleCommand("type synthetic add -x Eigen::SparseMatrix<.*> --python-class eigenlldb.EigenSparseMatrixChildProvider")

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

class EigenSparseMatrixChildProvider:
    _valobj: lldb.SBValue
    _scalar_type: lldb.SBType
    _scalar_size: int
    _index_type: lldb.SBType
    _index_size: int
    _row_major: bool

    _outer_size: int
    _nnz: int
    _values: lldb.SBValue
    _inner_indices: lldb.SBValue
    _outer_starts: lldb.SBValue
    _inner_nnzs: lldb.SBValue
    _compressed: bool

    def __init__(self, valobj, internal_dict):
        self._valobj = valobj
        valtype = valobj.GetType().GetCanonicalType()
        self._scalar_type = valtype.GetTemplateArgumentType(0)
        self._scalar_size = self._scalar_type.GetByteSize()
        self._index_type = valtype.GetTemplateArgumentType(2)
        self._index_size = self._index_type.GetByteSize()

        name = valtype.GetName()
        template_begin = name.find("<")
        template_end = name.find(">")
        template_args = name[(template_begin + 1):template_end].split(",")
        self._row_major = (int(template_args[1]) & 1) != 0
    def num_children(self):
        return self._nnz
    def get_child_index(self,name):
        pass
    def get_child_at_index(self,index):
        total_nnzs = 0
        for outer_index in range(self._outer_size):
            if self._compressed:
                index_begin = self._outer_starts \
                    .CreateChildAtOffset("", outer_index * self._index_size, self._index_type) \
                    .GetValueAsUnsigned()
                index_end = self._outer_starts \
                    .CreateChildAtOffset("", (outer_index + 1) * self._index_size, self._index_type) \
                    .GetValueAsUnsigned()
                nnzs = index_end - index_begin
                if total_nnzs + nnzs > index:
                    item_index = index - total_nnzs + index_begin
                    inner_index = self._inner_indices \
                        .CreateChildAtOffset("", item_index * self._index_size, self._index_type) \
                        .GetValueAsUnsigned()
                    return self._values \
                        .CreateChildAtOffset(
                            self._child_name(outer_index, inner_index),
                            item_index * self._scalar_size,
                            self._scalar_type)
                else:
                    total_nnzs = total_nnzs + nnzs
            else:
                nnzs = self._inner_nnzs \
                    .CreateChildAtOffset("", outer_index * self._index_size, self._index_type) \
                    .GetValueAsUnsigned()
                if total_nnzs + nnzs > index:
                    item_index = index - total_nnzs + index_begin
                    index_begin = self._outer_starts \
                        .CreateChildAtOffset("", outer_index * self._index_size, self._index_type) \
                        .GetValueAsUnsigned()
                    inner_index = self._inner_indices \
                        .CreateChildAtOffset("", item_index * self._index_size, self._index_type) \
                        .GetValueAsUnsigned()
                    return self._values \
                        .CreateChildAtOffset(
                            self._child_name(outer_index, inner_index),
                            item_index * self._scalar_size,
                            self._scalar_type)
                else:
                    total_nnzs = total_nnzs + nnzs
    def update(self):
        valobj = self._valobj
        self._outer_size = valobj.GetChildMemberWithName("m_outerSize").GetValueAsUnsigned()
        data = valobj.GetChildMemberWithName("m_data")
        self._values = data.GetChildMemberWithName("m_values")
        self._inner_indices = data.GetChildMemberWithName("m_indices")
        self._outer_starts = valobj.GetChildMemberWithName("m_outerIndex")
        self._inner_nnzs = valobj.GetChildMemberWithName("m_innerNonZeros")

        self._compressed = self._inner_nnzs.GetValueAsUnsigned() == 0
        self._nnz = data.GetChildMemberWithName("m_size").GetValueAsUnsigned()
    def _child_name(self, outer_index, inner_index):
        if self._row_major:
            return "[{0},{1}]".format(outer_index, inner_index)
        else:
            return "[{1},{0}]".format(outer_index, inner_index)