#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <time.h>

#define NUM_LEDS 72
#define MAX_FREQ 1000

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

    // Start frame
    for (int i = 0; i < 4; i++) buffer[i] = 0x00;

    // End frame
    for (int i = 0; i < 4; i++) buffer[4 + NUM_LEDS * 4 + i] = 0xFF;
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

void sleep_for_frequency(double freq) {
    // période en secondes = 1/freq, puis divisé par 2 pour ON/OFF
    double period = 1.0 / freq / 2.0;
    struct timespec ts;
    ts.tv_sec = (time_t) period;
    ts.tv_nsec = (long)((period - ts.tv_sec) * 1e9);
    nanosleep(&ts, NULL);
}

int main() {
    apa102_init();

    double freq = 1.0;
    int color_flag = 0; // 0 = rouge, 1 = jaune

    while (1) {
        if (color_flag == 0)
            apa102_fill(255, 0, 0, 1);  // rouge
        else
            apa102_fill(255, 255, 0, 1); // jaune

        apa102_show();

        sleep_for_frequency(freq);

        // alterne la couleur
        color_flag = 1 - color_flag;

        // augmente la fréquence jusqu'à MAX_FREQ
        if (freq < MAX_FREQ)
            freq += 1.0;
        else
            freq = MAX_FREQ; // boucle à 1000Hz
    }

    close(spi_fd);
    return 0;
}
