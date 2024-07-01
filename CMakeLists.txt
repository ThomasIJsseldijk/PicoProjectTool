cmake_minimum_required(VERSION 3.25)

# Configuration options
set(PROJECT_NAME {project_name})
set(BOARD_TYPE "{board_type}" CACHE STRING "Select the board type (pico or picow)")
set(LINKED_LIBRARIES "{linked_libraries}" CACHE STRING "Libraries to be linked")
set(SUB_DIRECTORIES "{sub_directories}" CACHE STRING "Subdirectories to include in the build")
set(STDIO_MODE "{stdio_mode}" CACHE STRING "Select stdio mode (usb or uart)")
set(SOURCE_FILES main.cpp)
set(FREERTOS_SRC_DIRECTORY {CMAKE_CURRENT_LIST_DIR}/FreeRTOS-Kernel)
set(FREERTOS_CFG_DIR {CMAKE_CURRENT_LIST_DIR}/config)
set(PICO_SDK_PATH {CMAKE_CURRENT_LIST_DIR}/pico-sdk)

# Compiler settings
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_COMPILER "arm-none-eabi-gcc.exe")
set(CMAKE_CXX_COMPILER "arm-none-eabi-g++.exe")

# Set the board type
string(TOLOWER ${BOARD_TYPE} PICO_BOARD)

if (NOT PICO_BOARD STREQUAL "pico" AND NOT PICO_BOARD STREQUAL "picow")
    message(FATAL_ERROR "Invalid board type specified. Use 'pico' or 'picow'.")
endif ()

# Include Pico SDK
include(${PICO_SDK_PATH}/external/pico_sdk_import.cmake)
include(${FREERTOS_SRC_DIRECTORY}/portable/ThirdParty/GCC/RP2040/FreeRTOS_Kernel_import.cmake)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.4.0")
    message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.4.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif ()

project(${PROJECT_NAME} C CXX ASM)

# C++ options
set(PICO_CXX_ENABLE_EXCEPTIONS 1) # Enable exceptions in C++
set(PICO_CXX_ENABLE_RTTI 1) # Enable run time type information in C++

# Initialize the Pico SDK
pico_sdk_init()

# Include subdirectories
foreach (subdir IN LISTS SUB_DIRECTORIES)
    add_subdirectory(${subdir})
    message(STATUS "Adding subdirectory: ${subdir}")
endforeach ()

# Create the executable
add_executable(${PROJECT_NAME} ${SOURCE_FILES})

# Set stdio mode
if (STDIO_MODE STREQUAL "usb")
    pico_enable_stdio_usb(${PROJECT_NAME} 1)
    pico_enable_stdio_uart(${PROJECT_NAME} 0)
elseif (STDIO_MODE STREQUAL "uart")
    pico_enable_stdio_usb(${PROJECT_NAME} 0)
    pico_enable_stdio_uart(${PROJECT_NAME} 1)
else ()
    message(FATAL_ERROR "Invalid stdio mode specified. Use 'usb' or 'uart'.")
endif ()

# Add the Config directory to the include path
target_include_directories(${PROJECT_NAME} PRIVATE ${FREERTOS_CFG_DIR})

# Link libraries and include directories
target_link_libraries(${PROJECT_NAME} FreeRTOS-Kernel FreeRTOS-Kernel-Heap4 pico_stdlib pico_bootsel_via_double_reset ${LINKED_LIBRARIES})
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_LIST_DIR}/..)

# Add extra outputs
pico_add_extra_outputs(${PROJECT_NAME})
