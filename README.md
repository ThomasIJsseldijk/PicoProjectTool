# PicoProjectTool

This project is designed to run on Raspberry Pi Pico or Pico W boards using FreeRTOS. The project includes a main application file (`main.cpp`) and configuration files for building and running the application.

## Prerequisites

Before you start, ensure you have the following dependencies installed:

- CMake (version 3.25 or later)
- Make
- Ninja
- arm-none-eabi-gcc (ARM GCC compiler)

### Installing Dependencies on Windows

1. **CMake:**

   Download and install CMake from the official website: [CMake Download](https://cmake.org/download/).

2. **Make:**

   Make can be installed as part of the MinGW toolset. Download and install MinGW from the official website: [MinGW Download](https://osdn.net/projects/mingw/releases/).

3. **Ninja:**

   Download and install Ninja from the official website: [Ninja Download](https://github.com/ninja-build/ninja/releases).

4. **arm-none-eabi-gcc:**

   Download and install the ARM GCC compiler from the official ARM website: [ARM GCC Download](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm).

   Make sure to add the path to `arm-none-eabi-gcc` and `arm-none-eabi-g++` executables to your system's PATH environment variable.

## using the tool


Follow these steps to use the `PicoProjectTool` to create a new project:

1. **Run the Tool**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `PicoProjectTool.py`.
   - Execute the script:
     ```sh
     python PicoProjectTool.py
     ```

2. **Enter Project Path**:
   - The tool will prompt you to enter the path of the folder where the project needs to be created.
   - Ensure the directory exists before proceeding.

3. **Enter Project Name**:
   - Enter the name of the project. If you leave this empty, the folder name will be used as the project name.

4. **Select Board Type**:
   - Specify the board type (`pico` or `picow`).

5. **Select Libraries**:
   - The tool will display a list of available libraries. Enter the library numbers to link them to your project, separated by spaces. Press Enter to skip this step if no additional libraries are needed.

6. **Specify Subdirectories**:
   - Enter subdirectories to include in the build, separated by semicolons.

7. **Select Stdio Mode**:
   - Choose the stdio mode (`usb` or `uart`).

8. **Wait for Configuration**:
   - The tool will clone the necessary repositories (FreeRTOS Kernel and Pico SDK), initialize submodules, and set up the project structure with the provided configuration options.

9. **Build the Project**:
   - Navigate to the project directory.
   - Create a build directory and navigate into it:
     ```sh
     mkdir build
     cd build
     ```
   - Run CMake and build the project using Ninja:
     ```sh
     cmake -G Ninja ..
     ninja
     ```

10. **Flash the Project**:
    - Connect your Raspberry Pi Pico/PicoW to your computer.
    - Use a flashing tool like `picotool` or drag-and-drop the generated UF2 file onto the Pico storage device.
