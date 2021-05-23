# Google Assistant Rotary Phone

This builds on [@rydercalmdown's excellent work](https://github.com/rydercalmdown/google_assistant_telephone) that they wrote [an article](https://www.tomshardware.com/how-to/turn-a-rotary-phone-into-google-assistant-with-raspberry-pi) about.

This repo makes the following changes:

1. It uses [Balena](balena.io) as the distribution mechanism, simplifying deployment and management of the Pi Zero W.
1. It uses Balena's [wifi-connect block](https://github.com/balenablocks/wifi-connect) to make it easy to give our rotary phone its first WiFi connection.
1. TODO: It adds support for a second "external" speaker to simulate ring sounds (actual rotary phone ringers need AC power, which the Pi can't provide).
1. TODO: It replaces use of the deprecated Google Assistant Library with the not-deprecated Google Assistant Service.

Next steps:

- Test that everything works as expected
- <checkpoint>
- External speaker
- <checkpoint>
- See about extracting the Docker container into a separately-published thing.
- See about slimming down the Docker container.
- <checkpoint>
- Publish via Deploy On Balena button?
- <checkpoint>
- Twilio stuff?
-
-

## Setup instructions

### Get and customize this code.

TODO: what needs to be customized?

### Prepare

1. Set up a virtualenv.
1. Run:
   (env)$ pip install google-auth-oauthlib[tool] google-assistant-sdk[samples]

### Get device credentials.

Follow these steps, partially following Google's Assistant SDK tutorial:

1. [Configure a Developer Project and Account Settings](https://developers.google.com/assistant/sdk/guides/service/python/embed/config-dev-project-and-account)
1. Make note of the `Project ID` for the project you just registered.
1. Under your Google Cloud Project's [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent), add your own Google account as a test user.
1. [Register the Device Model](https://developers.google.com/assistant/sdk/guides/service/python/embed/register-device), but don't take Google's advice about copying the file anywhere.
1. Make note of the `Model ID` you've just registered - you'll need it in a moment.
1. Take the downloaded JSON file and put it in this repository, naming it `oauth_config_credentials.json`:
   google_assistant_telephone$ mv ~/Downloads/your_unique_secret_file_name.json ./oauth_config_credentials.json
1. Pick a nice ID for your device (can be random), and register it:
   (env)$ googlesamples-assistant-devicetool --project-id=YOUR_PROJECT_ID register-device --device "YOUR_DEVICE_ID" --model="YOUR_MODEL_ID" --nickname="My Smart Rotary Phone" --client-type="SERVICE"

### Get your personal credentials.

1. Run:
   google_assistant_telephone$ make authenticate
1. Make note of the name of the file that the tool placed those credentials in.
1. Look at the contents of your credentials file; save them somewhere for later use in Balena. E.g.:
   $ cat ~/path/to/your/google-oauthlib-tool/credentials.json && echo "MAKE NOTE OF THE ABOVE, that line is your CREDENTIALS"

### Deploy with Balena.

TODO: sign up and deploy with Balena.

### Connect to WiFi.

TODO: explain captive portal.

### Get your personal credentials set up.
