#include <cstddef>
#include <iostream>
#include <Eigen/Dense>

int main() {
    Eigen::VectorXd vector = Eigen::VectorXd::Ones(3, 1);
    Eigen::MatrixXd matrix = Eigen::MatrixXd::Ones(3, 3);
    Eigen::Vector3d vector3 = Eigen::Vector3d::Ones();
    Eigen::Matrix3d matrix3 = Eigen::Matrix3d::Ones();

    using MatrixCustom = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor, 4, 4>;
    MatrixCustom matrix_custom(2, 2);
    matrix_custom << 1, 2, 3, 4;
    std::cout << vector << std::endl;
}