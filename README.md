# IAQ-BADGE

A conference size badge that is a air quality monitor, covering CO2, Temperature, and Humidity. It has an e-ink display to show levels and a calculated air quality legend (Great, Good, Caution, Evacuate).

### Development Unit

- [Raspberry Pi Pico (W)](https://www.pishop.us/product/raspberry-pi-pico-w/)
- [Adafruit SCD41](https://www.adafruit.com/product/5190)
- [Waveshare 2.9” e-Paper Display](https://www.amazon.com/gp/product/B07P6MJPTD/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [Adafruit Micro-Lipo Charger](https://www.adafruit.com/product/4410)
- [500mAh Lithium Ion Polymer Battery](https://www.adafruit.com/product/1578)

### Pinout

**Waveshare ePaper** 

| Connection | PIN        | Color   |
|------------|------------|---------|
| VCC        | 3.3v       | Gray    |
| GND        | GND        | Brown   |
| DIN        | GP11       | Blue    |
| CLK        | GP10       | Yellow  |
| CS         | GP9        | Orange  |
| DC         | GP8        | Green   |
| RST        | GP12       | White   |
| BUSY       | GP13       | Purple  |

**SCD41**

| Connection | PIN        |
|------------|------------|
| VCC        | 3.3v       |
| GND        | GND        |
| I2C0 SDA   | GP4        | 
| I2C0 SCL   | GP5        |

**Adafruit 4410 Micro Charger**

| Connection | PIN        |
|------------|------------|
| VCC        | VSYS       |
| GND        | GND        |

### Modules

- [Pico_ePaper](https://github.com/waveshare/Pico_ePaper_Code/tree/main/python)