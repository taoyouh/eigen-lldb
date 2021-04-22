cmake_minimum_required(VERSION 3.16)

project(EigenTest)
add_executable(EigenTest main.cpp)

include(conan.cmake)
conan_cmake_run(CONANFILE conanfile.txt
    BUILD outdated)
conan_check_compiler()
conan_basic_setup(TARGETS)
target_link_libraries(EigenTest CONAN_PKG::eigen)