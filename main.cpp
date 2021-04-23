#include <cstddef>
#include <iostream>
#include <Eigen/Dense>

int main() {
    Eigen::VectorXd vector(5, 1);
    Eigen::MatrixXd matrix(5, 5);
    Eigen::Vector3d vector3;
    Eigen::Matrix3d matrix3;
    std::cout << vector << std::endl;
}