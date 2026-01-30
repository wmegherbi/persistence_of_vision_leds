#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <time.h>
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

    // Start frame
    for (int i = 0; i < 4; i++) buffer[i] = 0x00;

    // End frame
    for (int i = 0; i < 4; i++) buffer[4 + NUM_LEDS * 4 + i] = 0xFF;
}
void init_random() {
    srand((unsigned int)time(NULL));
}
char random_char(){
    return (char)(rand() % 256);
}
// Remplir le ruban selon le pattern alterné
void apa102_alternate(uint8_t brightness, int phase) {
    brightness &= 15;            // 5 bits
    uint8_t prefix = 0xE0 | brightness;

    for (int i = 0; i < NUM_LEDS; i++) {
        int p = 4 + i * 4;

        if ((i + phase) % 2 == 0) {
            // LED rouge
            buffer[p + 0] = prefix;
            buffer[p + 1] = random_char();   // Blue
            buffer[p + 2] = random_char();   // Green
            buffer[p + 3] = random_char(); // Red
        } else {
            // LED éteinte
            buffer[p + 0] = prefix;
            buffer[p + 1] = 0;
            buffer[p + 2] = 0;
            buffer[p + 3] = 0;
        }
    }
}

void apa102_show() {
    write(spi_fd, buffer, sizeof(buffer));
}

// Fonction utilitaire pour dormir en fonction de la fréquence
void sleep_for_frequency(double freq) {
    double period = 1.0 / freq / 2.0; // moitié ON, moitié OFF
    struct timespec ts;
    ts.tv_sec = (time_t) period;
    ts.tv_nsec = (long)((period - ts.tv_sec) * 1e9);
    nanosleep(&ts, NULL);
}

int main() {
    apa102_init();

    double freq = 1.0;
    int phase = 0;

    while (1) {
        // Alterner LEDs une sur deux
        apa102_alternate(31, phase);
        apa102_show();

        sleep_for_frequency(freq);

        // Alterne le décalage pour faire clignoter "inverse"
        phase = 1 - phase;

        // Augmenter la fréquence progressivement jusqu'à 1000Hz
        if (freq < 3000.0)
            freq += 1.0;
        else
            freq = 3000.0;
    }

    close(spi_fd);
    return 0;
}
