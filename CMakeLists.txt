cmake_minimum_required(VERSION 3.16)

project(EigenTest)
add_executable(EigenTest main.cpp)

include(conan.cmake)
conan_cmake_run(CONANFILE conanfile.txt
    BUILD outdated)
conan_check_compiler()
conan_basic_setup(TARGETS)
target_link_libraries(EigenTest CONAN_PKG::eigen)

add_custom_command(
    OUTPUT .lldbinit
    DEPENDS .lldbinit
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/.lldbinit ${CMAKE_CURRENT_BINARY_DIR}/.lldbinit
)
add_custom_command(
    OUTPUT eigenlldb.py
    DEPENDS eigenlldb.py
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/eigenlldb.py ${CMAKE_CURRENT_BINARY_DIR}/eigenlldb.py
)
add_custom_target(LLDB ALL SOURCES ${CMAKE_CURRENT_BINARY_DIR}/.lldbinit ${CMAKE_CURRENT_BINARY_DIR}/eigenlldb.py)