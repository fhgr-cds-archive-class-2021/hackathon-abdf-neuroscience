import asyncio
import time
import json
import logging
from idun_guardian_sdk import GuardianClient
from preprocessing import preprocessing_pipeline, map_index_to_brain_wave

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("datastream.log"),
        logging.StreamHandler()
    ]
)

RECORDING_TIMER: int =  60 * 60 * 10  # 10 hours
LED_SLEEP: bool = False

my_api_token = "idun_2YV1BILW_T95lLajPwP2WHLqAxuYyuYheMKj-frjs7jBQz1wsbuaxSOh"

def save_data(event):
    logging.info(event.message['stateless_z_scores'])
    alpha = event.message['stateless_z_scores'][0]['Alpha']
    beta = event.message['stateless_z_scores'][0]['Beta']
    gamma = event.message['stateless_z_scores'][0]['Gamma']
    theta = event.message['stateless_z_scores'][0]['Theta']
    sigma = event.message['stateless_z_scores'][0]['Sigma']
    wave_index = preprocessing_pipeline(alpha, beta, gamma, theta, sigma)
    if wave_index:
        print(f"Brain wave detected: {map_index_to_brain_wave(wave_index)}")

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