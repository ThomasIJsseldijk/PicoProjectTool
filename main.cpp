#include "pico/stdlib.h"
#include "FreeRTOS.h"
#include "task.h"

// Define the stack overflow hook
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
    // Handle the stack overflow
    for(;;);
}

// Define the malloc failed hook
void vApplicationMallocFailedHook(void) {
    // Handle the malloc failure
    for(;;);
}

// Define the LED pin
#define LED_PIN 25

// Task to blink the LED
void vBlinkTask(void *pvParameters) {
    const TickType_t xDelay = 500 / portTICK_PERIOD_MS; // 500 ms delay

    // Initialize the GPIO for the LED
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    while (true) {
        // Toggle the LED
        gpio_put(LED_PIN, 1);
        vTaskDelay(xDelay);
        gpio_put(LED_PIN, 0);
        vTaskDelay(xDelay);
    }
}

int main() {
    // Initialize stdio
    stdio_init_all();

    // Create the blink task
    xTaskCreate(vBlinkTask, "Blink Task", 256, NULL, 1, NULL);

    // Start the scheduler
    vTaskStartScheduler();

    // Will never reach here
    while (true) {
    }
}
