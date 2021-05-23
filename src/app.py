import logging

logging.basicConfig(level=logging.INFO)

from threading import Timer
from typing import Optional

import click
import google.auth.transport.requests
import google.oauth2.credentials
import json
import os
import sys
import time

# import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause

from google_assistant import GoogleAssistant


@click.command()
@click.option('--credentials',
              metavar='<credentials>',
              show_default=True,
              default=os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json'),
              help='Path to read OAuth2 credentials.')
@click.option('--device-config',
              show_default=True,
              metavar='<device config>',
              default=os.path.join(
                  click.get_app_dir('googlesamples-assistant'),
                  'device_config.json'),
              help='Path to load the device configuration from')
def main(credentials, device_config):
    listen_for_contact_state_change()


assistant = GoogleAssistant()

MAX_PULSE_DURATION = 0.25  # In seconds.
MAX_PULSE_INTERVAL = 0.25  # In seconds.
hung_up_timer: Optional[Timer] = None
pulses_completed_timer: Optional[Timer] = None
num_pulses = 0


def phone_picked_up():
    """Called when the phone is picked up"""
    logging.info('Receiver picked up')
    assistant.assist()


def phone_hung_up():
    """Called when the phone is hung up"""
    logging.info('Receiver hung up')
    global hung_up_timer
    hung_up_timer = None


def number_dialed(number: int):
    logging.info(f"Dialed number: {number}")

def pulse():
    global pulses_completed_timer
    global num_pulses
    logging.debug("Pulse")

    def pulses_finished():
        global pulses_completed_timer
        global num_pulses
        pulses_completed_timer = None
        number = num_pulses % 10
        num_pulses = 0
        number_dialed(number)

    if pulses_completed_timer is None:
        # This is the first pulse of a sequence; reset.
        logging.debug("New pulse sequence")
        num_pulses = 0
    else:
        # This is a subsequent pulse in a sequence; reset the timer.
        pulses_completed_timer.cancel()
    num_pulses += 1
    pulses_completed_timer = Timer(MAX_PULSE_INTERVAL, pulses_finished)
    pulses_completed_timer.start()


def contact_made():
    global hung_up_timer
    logging.debug("Contact made")
    # If we were expecting this to be about a
    # This can mean one of two things:
    # 1. If this came after a short period of no contact, it indicates a pulse from
    #    the rotary dial. We know this was a short time period if the timer to declare
    #    this a hang-up is still running.
    if hung_up_timer is not None:
        hung_up_timer.cancel()
        hung_up_timer = None
        pulse()
    # 2. If this came after a long period of no contact, it means the receiver was
    #    picked up.
    else:
        phone_picked_up()


def contact_broken():
    logging.debug("Contact broken")

    # If contact remains broken for a long period, that means the phone was hung up.
    # If contact is quickly re-established this was only a pulse.
    global hung_up_timer
    if hung_up_timer is not None:
        raise RuntimeError(
            "Contact broken while hung-up timer was already running?")
    hung_up_timer = Timer(MAX_PULSE_DURATION, phone_hung_up)
    hung_up_timer.start()


def listen_for_contact_state_change():
    """Continuously listens for pickup/hangup of the hook"""

    contact = Button(18)
    contact.when_pressed = contact_made
    contact.when_released = contact_broken

    print("Listening to receiver changes...")
    pause()

    # pin_number = 18
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # try:
    #     while True:
    #         pin_current = GPIO.input(pin_number)
    #         if pin_current == 1:
    #             phone_picked_up()
    #         else:
    #             phone_hung_up()
    #         while GPIO.input(pin_number) == pin_current:
    #             time.sleep(0.1)
    # except KeyboardInterrupt:
    #     print('Exiting...')
    #     GPIO.cleanup()


if __name__ == "__main__":
    main()
