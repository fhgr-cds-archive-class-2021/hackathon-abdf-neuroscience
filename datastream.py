import asyncio
import time
import json
import logging
import fastapi
import uvicorn
import threading
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

target_brain_wave = 2 # gamma
start_time = time.time()
time_delta = 0
target_song = None
current_state = None

def save_data(event):
    
    global start_time
    global time_delta
    global target_song
    global current_state
    
    alpha = event.message['stateless_z_scores'][0]['Alpha']
    beta = event.message['stateless_z_scores'][0]['Beta']
    gamma = event.message['stateless_z_scores'][0]['Gamma']
    delta = event.message['stateless_z_scores'][0]['Delta']
    theta = event.message['stateless_z_scores'][0]['Theta']
    sigma = event.message['stateless_z_scores'][0]['Sigma']

    new_wave_index = preprocessing_pipeline(alpha, beta, gamma, delta, theta, sigma)
    current_state = new_wave_index

    if new_wave_index or new_wave_index == 0:
        print(f"Brain wave detected: {map_index_to_brain_wave(new_wave_index)}")
        # play spotipy song
        if new_wave_index != target_brain_wave:
            print(f"From {map_index_to_brain_wave(new_wave_index)} to Gamma")
        else:
            print("Gamma detected")
        time_delta = time.time() - start_time
        print("time delta: ", time_delta)
        #print(f"Time Delta: {time.time()}")
        #print(f"Time Delta: {time_delta}")
        if time_delta > 10:
            start_time = time.time()
            print("10 seconds elapsed")
            if new_wave_index != target_brain_wave:
                target_song = '50 Hz: High Level Cognition'
                print(f"Change Song beausse we are no longer in Gamma")
                #open_playlist_by_mood(client_id, client_secret, redirect_uri, "happy")
            
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

app = fastapi.FastAPI()
@app.get("/")
async def root():
    global time_delta
    open_playlist_by_mood(client_id, client_secret, redirect_uri, "happy")
    return {"message": time_delta}

class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        logger = ContinuousLogger(output='console')
        #start_time = time.time()
        while True:
            data = logger.generate_mock_event()
            logging.info(data.message)
            save_data(data)
t = BackgroundTasks()

# for testing purposes with simulated data
if __name__ == "__main__":
    t.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)