#include <cstddef>
#include <iostream>
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <vector>

int main() {
    Eigen::VectorXd vector = Eigen::VectorXd::Ones(3, 1);
    Eigen::MatrixXd matrix = Eigen::MatrixXd::Ones(3, 3);
    Eigen::Vector3d vector3 = Eigen::Vector3d::Ones();
    Eigen::Matrix3d matrix3 = Eigen::Matrix3d::Ones();

    using MatrixCustom = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor, 4, 4>;
    MatrixCustom matrix_custom(2, 2);
    matrix_custom << 1, 2, 3, 4;
    std::cout << vector << std::endl;

    Eigen::SparseMatrix<double> sparse_mat(2, 2);
    std::vector<Eigen::Triplet<double>> triplets;
    triplets.emplace_back(0, 0, 1);
    triplets.emplace_back(0, 1, 2);
    triplets.emplace_back(1, 1, 3);
    sparse_mat.setFromTriplets(triplets.begin(), triplets.end());
    std::cout << sparse_mat << std::endl;

    Eigen::SparseMatrix<double> sparse_uncompressed(2, 2);
    sparse_uncompressed.coeffRef(0, 0) = 1;
    sparse_uncompressed.coeffRef(0, 1) = 2;
    sparse_uncompressed.coeffRef(1, 1) = 3;
    std::cout << sparse_uncompressed << std::endl;
}