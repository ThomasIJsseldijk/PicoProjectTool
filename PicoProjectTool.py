import os
import subprocess

# List of available libraries
AVAILABLE_LIBRARIES = [
    "hardware_adc", "hardware_base", "hardware_claim", "hardware_clocks",
    "hardware_divider", "hardware_dma", "hardware_exception", "hardware_flash",
    "hardware_gpio", "hardware_i2c", "hardware_interp", "hardware_irq",
    "hardware_pio", "hardware_pll", "hardware_pwm", "hardware_resets",
    "hardware_rtc", "hardware_spi", "hardware_sync", "hardware_timer",
    "hardware_uart", "hardware_vreg", "hardware_watchdog", "hardware_xosc",
    "pico_async_contect", "pico_flash", "pico_i2c_slace", "pico_multicore",
    "pico_rand", "pico_stdlib", "pico_sync", "pico_time", "pico_unique_id",
    "pico_util", "tinyusb_device", "tinyusb_host", "pico_btstack", "pico_lwip",
    "pico_cyw43_driver", "pico_cyw43_arch"
]

def read_file(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'r') as file:
        return file.read()

def main():
    # Ask the user to enter the path of the folder where the project needs to be created
    project_path = input("Enter the path of the folder where the project needs to be created: ")
    if not os.path.isdir(project_path):
        print("Invalid path. Please make sure the directory exists.")
        return

    # Ask the user to enter the name of the project
    project_name = input("Enter the name of the project (leave empty to use the folder name): ")
    if not project_name:
        project_name = os.path.basename(os.path.normpath(project_path))

    # Prompt the user to enter configuration options
    board_type = input("Enter the board type (pico or picow): ")

    # Display available libraries for selection
    print("Available libraries:")
    for index, lib in enumerate(AVAILABLE_LIBRARIES, start=1):
        print(f"{index}. {lib}")

    # Ask the user to select libraries (multiple libraries can be entered, separated by spaces)
    selected_libraries = []
    while True:
        selection = input("Enter library number to link (press Enter to skip): ")
        if selection.strip():
            try:
                index = int(selection) - 1
                if 0 <= index < len(AVAILABLE_LIBRARIES):
                    selected_libraries.append(AVAILABLE_LIBRARIES[index])
                else:
                    print("Invalid library number. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            break
    
    linked_libraries = ';'.join(selected_libraries)

    sub_directories = input("Enter subdirectories to include in the build (separated by semicolons): ")
    stdio_mode = input("Enter stdio mode (usb or uart): ")

    # Clone the git repo for the FreeRTOS kernel
    freertos_repo = "https://github.com/FreeRTOS/FreeRTOS-Kernel.git"
    freertos_path = os.path.join(project_path, "FreeRTOS-Kernel")
    if not os.path.exists(freertos_path):
        subprocess.run(["git", "clone", freertos_repo, freertos_path])

    # Clone the git repo for the Pico C SDK
    pico_sdk_repo = "https://github.com/raspberrypi/pico-sdk.git"
    pico_sdk_path = os.path.join(project_path, "pico-sdk")
    if not os.path.exists(pico_sdk_path):
        subprocess.run(["git", "clone", pico_sdk_repo, pico_sdk_path])

    # Initialize the submodules in the Pico C SDK
    subprocess.run(["git", "submodule", "update", "--init"], cwd=pico_sdk_path)

    # Read and create the main.cpp file
    main_cpp_content = read_file("main.cpp")
    with open(os.path.join(project_path, "main.cpp"), "w") as main_cpp_file:
        main_cpp_file.write(main_cpp_content)

    # Read and create the CMakeLists.txt file
    cmake_lists_template = read_file("CMakeLists.txt")
    cmake_lists_content = cmake_lists_template.replace(
        "{project_name}", project_name
    ).replace(
        "{board_type}", board_type
    ).replace(
        "{linked_libraries}", linked_libraries
    ).replace(
        "{sub_directories}", sub_directories
    ).replace(
        "{stdio_mode}", stdio_mode
    ).replace(
        "{CMAKE_CURRENT_LIST_DIR}", "${CMAKE_CURRENT_LIST_DIR}"
    )
    
    with open(os.path.join(project_path, "CMakeLists.txt"), "w") as cmake_lists_file:
        cmake_lists_file.write(cmake_lists_content)

    # Read and create the FreeRTOSConfig.h file in the config directory
    config_path = os.path.join(project_path, "config")
    os.makedirs(config_path, exist_ok=True)
    freertos_config_content = read_file("FreeRTOSConfig.h")
    with open(os.path.join(config_path, "FreeRTOSConfig.h"), "w") as freertos_config_file:
        freertos_config_file.write(freertos_config_content)

    print("Project configured successfully!")

if __name__ == "__main__":
    main()
