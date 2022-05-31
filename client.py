from plistlib import load
from FlightRadar24.api import FlightRadar24API
from dotenv import load_dotenv
import smtplib, os, time

load_dotenv()


def send_email():
   gmail_user=os.getenv('EMAIL')
   gmail_password=os.getenv('PASSWORD')
   sent_from = 'simon.duperray4949@gmail.com'
   to = ['simon.duperray@reseau.eseo.fr']
   subject = 'SAMU49 Event'
   body = 'The SAMU is gone or arrived.'

   email_text = """\
   From: %s
   To: %s
   Subject: %s

   %s
   """ % (sent_from, ", ".join(to), subject, body)

   try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(gmail_user, gmail_password)
      server.sendmail(sent_from, to, email_text)
      server.close()
      print('Email sent!')
   except:
      print("Error: Unable to connect to SMTP server")


def get_flights_from_api():
   fr_api = FlightRadar24API()
   return fr_api.get_flights(bounds="51.27,42.28,-6.28,9.41")
    

# while True:
#    flights = get_flights_from_api()
#    for flight in flights:
#       if flight.callsign=="SAMU49":
#          print(f'SAMU detected (alt.: {flight.altitude})')
#          if int(flight.altitude)<100:
#             print("low altitude detected")
#             send_email()
#       else:
#          print("No SAMU detected")
#    print("finished, waiting for 10 sec")
#    time.sleep(10)

while True:
   flights = get_flights_from_api()
   for flight in flights:
      # and isinstance(int(flight.callsign[-2:]), int)
      if flight.callsign[:4]=="SAMU":
         print(f'{flight.callsign} detected. id: {flight.id} - lalo: ({flight.latitude},{flight.longitude}) - heading: {flight.heading} - altidude: {flight.altitude} - gound_speed: {flight.ground_speed} - aircraft_code: {flight.aircraft_code} - registration: {flight.registration} - time: {flight.time} - number: {flight.number} - on_ground: {flight.on_ground} - vertical_speed: {flight.vertical_speed}')
         if int(flight.altitude)<700:
            print("low altitude detected for {flight.callsign}")
            # send_email()
   print("finished, waiting for 10 sec")
   time.sleep(10)