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
start_time = time.time()
time_delta = 0

def save_data(event):
    
    global last_wave_index
    global start_time
    global time_delta
    
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
    time_delta = time.time() - start_time
    print("start time: ", start_time)
    #print(f"Time Delta: {time.time()}")
    #print(f"Time Delta: {time_delta}")
    if time_delta > 10:
        start_time = time.time()
        print("10 seconds elapsed")
        if last_wave_index != target_brain_wave:
            print(f"Change Song beausse we are no longer in Gamma")
            open_playlist_by_mood(client_id, client_secret, redirect_uri, "happy")
            

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
    start_time = time.time()
    while True:
        data = logger.generate_mock_event()
        logging.info(data.message)
        save_data(data)
        elapsed_time = time.time() - start_time
        #print(f"Elapsed time: {elapsed_time}")
        if elapsed_time >   10:
            print("10 seconds elapsed")
            start_time = time.time()
            if last_wave_index != target_brain_wave:
                print(f"Change Song beausse we are no longer in Gamma")
                open_playlist_by_mood(client_id, client_secret, redirect_uri, "happy")
        time.sleep(0.1)
        
        #mood = "happy"
        #open_playlist_by_mood(client_id, client_secret, redirect_uri, mood)
        
'''     