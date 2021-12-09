import requests
import smtplib
from datetime import datetime
import time

# enter
MY_LAT = 0
MY_LNG = 0
# change the gmt time
GMT = 2
time_now = datetime.now()
# enter
SMTP_SERVER = ""
EMAIL_USER_NAME = ""
EMAIL_PASSWORD = ""

SUN_API = "https://api.sunrise-sunset.org/json"
ISS_API = "http://api.open-notify.org/iss-now.json"


def is_iss_overhead():
    response_iss = requests.get(url=ISS_API)
    response_iss.raise_for_status()

    longitude_iss = response_iss.json()["iss_position"]["longitude"]
    latitude_iss = response_iss.json()["iss_position"]["latitude"]
    iss_position = (float(longitude_iss), float(latitude_iss))
    # checks if the iss is above me
    if MY_LNG - 5 <= iss_position[0] <= MY_LNG + 5 and MY_LAT -5 <= iss_position[1] <= MY_LAT + 5:
        return True
    else:
        return False


def check_night():
    parameters = {
        "lat": MY_LNG,
        "lng": MY_LAT,
        "formatted": 0
    }

    response_sun = requests.get(url=SUN_API, params=parameters)
    response_sun.raise_for_status()

    sunrise, sunset = response_sun.json()['results']['sunrise'], response_sun.json()['results']['sunset']

    # fix to correct GMT time and to show the time
    sunrise = "+".join(sunrise.split("T"))
    sunrise = sunrise.split("+")
    # shows the prices hour and minutes
    sunrise = sunrise[1]
    # only the hour
    sunrise = sunrise.split(":")[0]

    sunset = "+".join(sunset.split("T"))
    sunset = sunset.split("+")
    # shows the prices hour and minutes
    sunset = sunset[1]
    # only the hour
    sunset = sunset.split(":")[0]

    if sunrise[1].isdigit():
        correct_time = int(sunrise[0:2]) + GMT
        sunrise = str(correct_time) + sunrise[2:]
    else:
        correct_time = int(sunrise[0]) + GMT
        sunrise = str(correct_time) + sunrise[1:]

    if sunset[1].isdigit():
        correct_time = int(sunset[0:2]) + GMT
        sunset = str(correct_time) + sunset[2:]
    else:
        correct_time = int(sunset[0]) + GMT
        sunset = str(correct_time) + sunset[1:]

    # checks if its night time
    if int(sunset) < time_now.hour < int(sunrise):
        return True
    else:
        return False


# checks every minute
while True:
    if is_iss_overhead() and check_night():
        connection = smtplib.SMTP(SMTP_SERVER)
        connection.starttls()
        connection.login(user=EMAIL_USER_NAME, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_USER_NAME,
            to_addrs=EMAIL_USER_NAME,
            msg="Subject:Look Up \n\n The ISS is above u"
        )

    time.sleep(60)

