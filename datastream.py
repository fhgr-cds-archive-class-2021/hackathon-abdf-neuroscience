import asyncio
import time
import json
import logging
from idun_guardian_sdk import GuardianClient
from preprocessing import preprocessing_pipeline, map_index_to_brain_wave
from random_data_generator import ContinuousLogger
from play_song import open_playlist_by_mood, client_id, client_secret, redirect_uri

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
last_wave_index = None

target_brain_wave = 2 # gamma

def save_data(event):
    global last_wave_index
    alpha = event.message['stateless_z_scores'][0]['Alpha']
    beta = event.message['stateless_z_scores'][0]['Beta']
    gamma = event.message['stateless_z_scores'][0]['Gamma']
    delta = event.message['stateless_z_scores'][0]['Delta']
    theta = event.message['stateless_z_scores'][0]['Theta']
    sigma = event.message['stateless_z_scores'][0]['Sigma']

    new_wave_index = preprocessing_pipeline(alpha, beta, gamma, delta, theta, sigma)

    if new_wave_index or new_wave_index == 0:
        print(f"Brain wave detected: {map_index_to_brain_wave(new_wave_index)}")
        # play spotipy song
        if new_wave_index != target_brain_wave:
            print(f"From {map_index_to_brain_wave(new_wave_index)} to Gamma")
        else:
            print("Gamma detected")
            
'''
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
'''

# for testing purposes with simulated data
if __name__ == "__main__":
    logger = ContinuousLogger(output='console')
    while True:
        data = logger.generate_mock_event()
        logging.info(data.message)
        save_data(data)
        time.sleep(0.5)
        mood = "happy"
        #open_playlist_by_mood(client_id, client_secret, redirect_uri, mood)
        
        