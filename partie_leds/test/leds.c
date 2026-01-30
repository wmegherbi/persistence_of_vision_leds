#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>

#define NUM_LEDS 72

static const char *spi_device = "/dev/spidev0.0";
static uint32_t speed = 8000000;   // 8 MHz
static uint8_t mode = SPI_MODE_0;
static int spi_fd;

// Buffer complet : start + LED frames + end frame
uint8_t buffer[4 + NUM_LEDS * 4 + 4];

void apa102_init() {
    spi_fd = open(spi_device, O_RDWR);
    if (spi_fd < 0) {
        perror("SPI open");
        exit(1);
    }

    ioctl(spi_fd, SPI_IOC_WR_MODE, &mode);
    ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);

    // start frame
    for (int i = 0; i < 4; i++)
        buffer[i] = 0x00;

    // end frame
    for (int i = 0; i < 4; i++)
        buffer[4 + NUM_LEDS * 4 + i] = 0xFF;
}

void apa102_fill(uint8_t r, uint8_t g, uint8_t b, uint8_t brightness) {
    brightness &= 0x1F;            // 5 bits
    uint8_t prefix = 0xE0 | brightness;

    for (int i = 0; i < NUM_LEDS; i++) {
        int p = 4 + i * 4;
        buffer[p + 0] = prefix;
        buffer[p + 1] = b;
        buffer[p + 2] = g;
        buffer[p + 3] = r;
    }
}

void apa102_show() {
    write(spi_fd, buffer, sizeof(buffer));
}

int main() {
    apa102_init();

    // Allumer 72 LEDs en rouge (255,0,0)
    apa102_fill(255, 0, 0, 31);  // RGB + brightness (0–31)
    apa102_show();

    close(spi_fd);
    return 0;
}
