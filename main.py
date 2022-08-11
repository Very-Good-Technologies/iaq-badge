import picosleep
import time
from machine import Pin
from epaper2in9 import EPD_2in9_Landscape

software_version = "0.0.1"

led = Pin(25, Pin.OUT)
deep_sleep_s = 10 # How long to sleep between readings

epd = EPD_2in9_Landscape()
epd.Clear(0xff)

# while sleeptime <= 10:
#     led.toggle()
#     time.sleep(5)
#     led.toggle()
#     picosleep.seconds(sleeptime)
#     sleeptime = sleeptime + 1

def initialBootLED():
    """
    Blinks LED Twice with 0.5s delay between each blink upon boot
    """
    led.toggle() # LED On
    time.sleep(0.5)
    led.toggle() # LED Off
    time.sleep(0.5)
    led.toggle() # LED On
    time.sleep(0.5)
    led.toggle() # LED Off

def initialBootDisplay():
    """
    Displays Very Good Technologies, model, and the version of software
    """
    epd.fill(0xff)
    epd.text("Very Good Technologies", 5, 10, 0x00)
    epd.text("IAQ-BADGE", 5, 20, 0x00)
    epd.text("v{}".format(software_version), 5, 30, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)
    
    epd.vline(10, 40, 60, 0x00)
    epd.vline(120, 40, 60, 0x00)
    epd.hline(10, 40, 110, 0x00)
    epd.hline(10, 100, 110, 0x00)
    epd.line(10, 40, 120, 100, 0x00)
    epd.line(120, 40, 10, 100, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)
    
    epd.rect(150, 5, 50, 55, 0x00)
    epd.fill_rect(150, 65, 50, 115, 0x00)
    epd.display_Base(epd.buffer)
    epd.delay_ms(2000)
    
    for i in range(0, 10):
        epd.fill_rect(220, 60, 10, 10, 0xff)
        epd.text(str(i), 222, 62, 0x00)
        epd.display_Partial(epd.buffer)

    epd.init()
    epd.Clear(0xff)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()

def updateDisplay(payload):
    print(payload)

if __name__=='__main__':
    initialBootLED()
    initialBootDisplay()

    while True:
        # logic here then deep sleep until next reading
        picosleep.seconds(deep_sleep_s)