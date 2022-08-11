import picosleep
import time
from machine import Pin
from epaper2in9 import EPD_2in9_Landscape

software_version = "0.0.1"

### User Configurable
color_mode = 'dark' # or light
deep_sleep_s = 10 # How long to sleep between readings

### DO NOT MODIFY BELOW
if color_mode == 'dark':
    bg_color = 0
    text_color = 1
else:
    bg_color = 1
    text_color = 0

led = Pin(25, Pin.OUT)

### Test Data
data = {'temp_f': 73.762, 'humid': 41.002, 'co2': 544.87}

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


def initializeDisplay():
    """
    Displays Very Good Technologies, model, and the version of software
    """
    epd = EPD_2in9_Landscape()
    epd.Clear(bg_color)
    epd.fill(bg_color)
    epd.text("Very Good Technologies", 5, 10, text_color)
    epd.text("IAQ-BADGE", 5, 20, text_color)
    epd.text("v{}".format(software_version), 5, 30, text_color)
    epd.text("Booting...", 5, 60, text_color)
    epd.display(epd.buffer)
    epd.delay_ms(10000)
    return epd


def mainContent():
    """
    Main display of Temp, Humid, CO2
    """
    #epd.Clear(bg_color) # Clears the buffer

    epd.fill(bg_color) # Starts building new buffer with background
    epd.text("Temperature", 5, 10, text_color)
    epd.text("Humidity", 5, 20, text_color)
    epd.text("CO2", 5, 30, text_color)
    epd.vline(102, 10, 30, text_color)
    epd.display_Base(epd.buffer)
    epd.delay_ms(2000)
    
    for i in range(0, 10):
        temp = '{}{}'.format(str('%.1f'%data['temp_f']),'F') #Limit decimals to 1
        humid = '{}{}'.format(str('%.1f'%data['humid']),'%')
        co2 = '{}{}'.format(str('%.0f'%data['co2']),'ppm')

        
        epd.fill_rect(110, 10, 72, 10, bg_color)
        epd.text(temp, 112, 12, text_color)

        epd.fill_rect(110, 20, 72, 10, bg_color)
        epd.text(humid, 112, 22, text_color)

        epd.fill_rect(110, 30, 72, 10, bg_color)
        epd.text(co2, 112, 32, text_color)

        epd.display_Partial(epd.buffer)
        # Temporarily increment things to test refresh
        data['temp_f'] = float(data['temp_f'] + 1.0)
        data['humid'] = float(data['humid'] + 1.0)
        data['co2'] = float(data['co2'] + 37.1)
        

def clearDisplayAndSleep():
    epd.init()
    epd.Clear(0xff)
    epd.delay_ms(2000)
    print("Putting display to sleep")
    epd.sleep()


def deepSleep(deep_sleep_s):
    print('Waiting 5 seconds then taking a nap.')
    time.sleep(5)
    clearDisplayAndSleep()
    print('Taking a nap, night night')
    picosleep.seconds(deep_sleep_s)


if __name__=='__main__':
    initialBootLED()
    epd = initializeDisplay()

    # Run the loop to collect data and update on display
    mainContent()
    
    deepSleep(deep_sleep_s)
    
