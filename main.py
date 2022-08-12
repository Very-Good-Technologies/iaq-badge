import picosleep
import time
from machine import Pin
from epaper2in9 import EPD_2in9_Landscape
import random

software_version = "0.0.1"

### User Configurable
color_mode = 'dark' # or light
deep_sleep_s = 10 # How long to sleep between readings
sorry_delay = 750

### DO NOT MODIFY BELOW
if color_mode == 'dark':
    bg_color = 0
    text_color = 1
else:
    bg_color = 1
    text_color = 0

led = Pin(25, Pin.OUT)

### Carbon Dioxide Exposure Limits
def co2ExposureLevel(reading):
    reading = int(reading)
    if 0 < reading < 500:
        return {'safety_level': 'Ideal', 'message': ['This place is almost too clean!', 'Fresh, fresh air!', 'Was Martha Stuart just here?']}
    elif 501 < reading < 1000:
        return {'safety_level': 'Healthy', 'message': ['Mmmm, smells wonderful in here!', 'You keep a clean joint.', 'Breathe in deep and enjoy!']}
    elif 1001 < reading < 1400:
        return {'safety_level': 'Caution', 'message': ['Still feeling last night, huh?', 'Are you feeling dizzy yet?', 'You should open a window!', 'Who farted?']}
    elif 1401 < reading < 2500:
        return {'safety_level': 'Unhealthy', 'message': ['Did you take a gummy?', '..when the weed hits', 'Seriously, open a window.', 'Youre 50% dumber at this point']}
    elif 2501 < reading < 5000:
        return {'safety_level': 'Critical', 'message': ['Get the fuck out of here!', 'No, but seriously. Get out!']}
    else:
        return {'safety_level': 'Error', 'message': ['Yo, this thing is broken.', 'I fucked up.', 'Reboot me, like its Windows 95!']}

### Soory messages
sorry_messages = [
                      "Mktg said we had to do this.",
                      "'Show our Garkner stuff for 10s'",
                      "_'It's not that long'_ they said.",
                      "I opened an Issue on this.",
                      "Issue #281",
                      "They closed it #wontfix",
                      "This is bullshit, yea?",
                      "Cause this thing boots in <1s",
                      "They're just fucking with you now",
                      "This definitely sold more units.",
                      "Prob gettin fired at code review.",
                      "But I don't care.",
                      "Users matter, experience matters.",
                      "People matter. All of 'em.",
                      "Well most of them.",
                      "Fuck, Mitch McConnell.",
                      "While I've got you...",
                      "Nah, I'm not gonna go there.",
                      "Srsly, marketing is kinda dumb",
                      "Did you care about Garkner rating?",
                      "No? I didn't think so,",
                      "I've been collecting IAQ for...",
                      "This whole time",
                      "Your IAQ is actually not terrible",
                      "Three more seconds, you got this",
                      "Two! Just two.",
                      "I lied, they said one more.",
                      "What a ride. You've been a champ.",
                      "Capitalism is bullshit"
                      
                  ]

### Test Data
data = {'temp_f': 73.762, 'humid': 41.002, 'co2': 100.87}

def initialBootLED():
    """
    Blinks LED Twice with 0.5s delay between each blink upon boot
    """
    led.toggle() # LED On
    time.sleep(0.1)
    led.toggle() # LED Off
    time.sleep(0.1)
    led.toggle() # LED On
    time.sleep(0.2)
    led.toggle() # LED Off
    led.toggle() # LED On
    time.sleep(0.1)
    led.toggle() # LED Off
    time.sleep(0.1)
    led.toggle() # LED On
    time.sleep(0.2)
    led.toggle() # LED Off

def generate_8_hex():
    hex = ''
    for i in range(0,7):
        r = str(random.choice("0123456789ABCDEF"))
        hex = hex + r
    return hex
    

def initializeDisplay():
    """
    Displays Very Good Technologies, model, and the version of software
    """
    epd = EPD_2in9_Landscape()
    #epd.Clear(bg_color)
    epd.fill(bg_color)
    epd.text("Very Good Technologies", 5, 10, text_color)
    epd.text("The leader in IAQ Platforms", 5, 20, text_color)
    epd.text("Garkner rates us VISIONARY, 2022", 5, 30, text_color)
    epd.text("IAQ-BADGE", 5, 50, text_color)
    epd.text("v{}".format(software_version), 5, 60, text_color)

    track_hex = generate_8_hex()
    epd.text("TRACKING_ID: {} <-- Fake!".format(track_hex), 5, 118, text_color)
    epd.display_Base(epd.buffer)

    for m in sorry_messages:
        epd.fill_rect(5, 80, 286, 10, bg_color)
        epd.text(m, 5, 82, text_color)
        epd.display_Partial(epd.buffer)
        
        epd.delay_ms(sorry_delay)

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
    epd.delay_ms(100)
    
    for i in range(0, 15):
        temp = '{}{}'.format(str('%.1f'%data['temp_f']),'F') #Limit decimals to 1
        humid = '{}{}'.format(str('%.1f'%data['humid']),'%')
        co2 = '{}{}'.format(str('%.0f'%data['co2']),'ppm')
        co2_safety = co2ExposureLevel(int(data['co2']))
        co2_msg_list = co2_safety['message']
        co2_message = random.choice(co2_msg_list)

        epd.fill_rect(110, 10, 72, 10, bg_color)
        epd.text(temp, 112, 12, text_color)

        epd.fill_rect(110, 20, 72, 10, bg_color)
        epd.text(humid, 112, 22, text_color)

        epd.fill_rect(110, 30, 72, 10, bg_color)
        epd.text(co2, 112, 32, text_color)

        epd.fill_rect(5, 60, 286, 10, bg_color)
        epd.text(co2_safety['safety_level'], 5, 62, text_color)

        epd.fill_rect(5, 80, 286, 10, bg_color)
        epd.text(co2_message, 5, 82, text_color)

        epd.display_Partial(epd.buffer)
        # Temporarily increment things to test refresh
        data['temp_f'] = float(data['temp_f'] + 1.0)
        data['humid'] = float(data['humid'] + 1.0)
        data['co2'] = float(data['co2'] + 237.1)
        epd.delay_ms(2000)
    

        

def clearDisplayAndSleep():
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
    for i in range(0,3):
        print('Loop: {}'.format(str(i)))
        led.toggle() # LED On
        mainContent()
        led.toggle()
        clearDisplayAndSleep()
        deepSleep(deep_sleep_s)
    
