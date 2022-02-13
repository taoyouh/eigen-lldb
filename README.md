# eigen-lldb
This project is used to inspect Eigen Matrices in LLDB.

## Notice
This project is the original version of the lldb inspector in the Eigen [GitLab repo](https://gitlab.com/libeigen/eigen/-/blob/master/debug/lldb/eigenlldb.py). Any new updates should directly go to the Eigen repo.

## Usage
1. download the file `eigenlldb.py`

2. Add the following line to the file `~/.lldbinit` (create one if it doesn't exist)
```
command script import /path/to/eigenlldb.py
```

3. Inspect the variables in LLDB command line
```
(lldb) frame variable vector3
(Eigen::Vector3d) vector3 = ([0,0] = 1, [1,0] = 1, [2,0] = 1)
(lldb) frame variable matrix3
(Eigen::Matrix3d) matrix3 = ([0,0] = 1, [1,0] = 1, [2,0] = 1, [0,1] = 1, [1,1] = 1, [2,1] = 1, [0,2] = 1, [1,2] = 1, [2,2] = 1)
(lldb) frame variable sparse_mat
(Eigen::SparseMatrix<double, 0, int>) sparse_mat = ([0,0] = 1, [0,1] = 2, [1,1] = 3)
```

## Example
The CMake project in this repo can be used to test the script.

1. Build the CMake project
```
mkdir build
cd build
cmake ..
cmake --build .
```

2. Launch LLDB
```
lldb EigenTest --local-lldbinit
```

3. Run the program and inspect the variables
```
(lldb) breakpoint set -l 30
Breakpoint 1: where = EigenTest`main + 947 at main.cpp:30:18, address = 0x000000000000299c

(lldb) run
Process 178 launched: '/home/zhaoquan/repos/eigen-lldb/build/EigenTest' (x86_64)
...

(lldb) frame variable
(Eigen::VectorXd) vector = ([0,0] = 1, [1,0] = 1, [2,0] = 1)
(Eigen::MatrixXd) matrix = ([0,0] = 1, [1,0] = 1, [2,0] = 1, [0,1] = 1, [1,1] = 1, [2,1] = 1, [0,2] = 1, [1,2] = 1, [2,2] = 1)
....
(Eigen::SparseMatrix<double, 0, int>) sparse_mat = ([0,0] = 1, [0,1] = 2, [1,1] = 3)
