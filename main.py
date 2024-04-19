import sys
import time
import logging

from pyhubctl import Configuration, PyHubCtl

from weather import Weather
from config import OPENWEATHER_API_KEY, USB_HUB, USB_PORT


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":

    weather = Weather()
    phc = PyHubCtl()

    while True:
        try:
            # Start loop
            print("Press CTRL-C to stop")

            sunrise, sunset = weather.get_sunrise_and_sunset()

            current_unix_time = int(time.time())
            if sunrise <= current_unix_time <= sunset:
                logging.info(f"Lights on! Current time: {current_unix_time} is between sunrise {sunrise} and sunset {sunset}")
                phc.run(Configuration(location=USB_HUB, ports=USB_PORT, action="on"))
            else:
                logging.info(f"Lights off! Current time: {current_unix_time} is NOT between sunrise {sunrise} and sunset {sunset}")
                phc.run(Configuration(location=USB_HUB, ports=USB_PORT, action="off"))

            time.sleep(300)

        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)
