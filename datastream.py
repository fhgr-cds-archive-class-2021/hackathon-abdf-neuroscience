import asyncio
import time
import json
import logging
from idun_guardian_sdk import GuardianClient
from preprocessing import preprocessing_pipeline

RECORDING_TIMER: int =  60 * 60 * 10  # 10 hours
LED_SLEEP: bool = False

my_api_token = "idun_2YV1BILW_T95lLajPwP2WHLqAxuYyuYheMKj-frjs7jBQz1wsbuaxSOh"

# global file
current_timestamp = time.time()

data_stream = []


# Example callback function
def save_data(event):
    alpha = event.message['stateless_z_scores'][0]['Alpha']
    beta = event.message['stateless_z_scores'][0]['Beta']
    gamma = event.message['stateless_z_scores'][0]['Gamma']
    theta = event.message['stateless_z_scores'][0]['Theta']
    sigma = event.message['stateless_z_scores'][0]['Sigma']
    preprocessing_pipeline(alpha, beta, gamma, theta, sigma)


if __name__ == "__main__":
    client = GuardianClient(api_token=my_api_token)
    client.address = asyncio.run(client.search_device())

    client.subscribe_realtime_predictions(fft=True, jaw_clench=False, handler=save_data)

    # start a recording session
    asyncio.run(
        client.start_recording(
            recording_timer=RECORDING_TIMER,
            led_sleep=LED_SLEEP,
        )
    )