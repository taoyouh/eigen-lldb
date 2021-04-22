#include <cstddef>
#include <iostream>
#include <Eigen/Dense>

struct my_storage {
    int* data;
    std::size_t count;
};

struct my_struct {
    my_storage storage;
};


int main() {
    my_struct obj;
    obj.storage.data = new int[10];
    obj.storage.count = 10;

    std::cout << obj.storage.data[0] << std::endl;

    Eigen::VectorXd vector(25, 1);
    Eigen::MatrixXd matrix(25, 25);
    vector[0] = 1;
    vector[1] = 2;
    vector[2] = 3;
    std::cout << vector << std::endl;
}