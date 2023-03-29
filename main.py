import time

import requests
from datetime import datetime
import smtplib

ck3_email = "juststriveathletic@gmail.com"
password = "avhdrsagtyctsyvg"

MY_LAT = 29.760427
MY_LONG = -95.369804


def iss_isOverhead():
    response1 = requests.get(url="http://api.open-notify.org/iss-now.json")
    response1.raise_for_status()
    data = response1.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LONG - 5 <= iss_long <= MY_LONG + 5:
        return True


def isNightTime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split('T')[1].split(':')[0])
    sunset = int(data["results"]["sunset"].split('T')[1].split(':')[0])

    print(sunrise)
    print(sunset)

    time_now = datetime.now()
    print(time_now.hour)

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_isOverhead() and isNightTime():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=ck3_email, password=password)
            connection.sendmail(from_addr=ck3_email,
                                to_addrs="chriskuete@yahoo.fr",
                                msg="Subject:ISS OVERHEAD\n\nLook Up!!")

# your position is within +5 or -5 of the iss position
