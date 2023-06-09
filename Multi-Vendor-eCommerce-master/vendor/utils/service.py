import threading

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import requests


class EmailThread(threading.Thread):
    ''' Thread to send email in background. '''

    def __init__(self, mail):
        self.mail = mail
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.mail.send()
        except Exception as e:
            print('Error sending email: %s' % e)


def send_welcome_mail(request, user):
    ''' Send welcome mail to vendor. '''
    current_site = get_current_site(request)

    body = render_to_string("vendor/mail/welcome_email.html",
                            {'current_site': request.META['HTTP_USER_AGENT'], 'domain': current_site.domain, 'user': request.user.vendor})

    mail = EmailMessage(
        subject="Welcome to Lomofy!",
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[request.user.vendor.email],
    )
    mail.content_subtype = "HTML"
    mail.send()
    return None



# def geocode_address(address):
#     api_key = 'your-api-key'  # Replace with your Google Maps API key
#     url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
#
#     response = requests.get(url)
#     data = response.json()
#
#     if data['status'] == 'OK':
#         location = data['results'][0]['geometry']['location']
#         latitude = location['lat']
#         longitude = location['lng']
#         return latitude, longitude
#
#     return None, None

# def geocode_address(address):
#     # https: // geocode.maps.co /
#     url = f'https://geocode.maps.co/search?q={address}'
#
#     response = requests.get(url)
#     data = response.json()
#
#     if data and 'lat' in data[0] and 'lon' in data[0]:
#         latitude = float(data[0]['lat'])
#         longitude = float(data[0]['lon'])
#         return latitude, longitude
#
#     return None, None
