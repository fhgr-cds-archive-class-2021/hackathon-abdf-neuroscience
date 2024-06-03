import asyncio
from idun_guardian_sdk import GuardianClient

RECORDING_TIMER: int =  60 * 60 * 10  # 10 hours
LED_SLEEP: bool = False

my_api_token = "idun_2YV1BILW_T95lLajPwP2WHLqAxuYyuYheMKj-frjs7jBQz1wsbuaxSOh"


# Example callback function
def print_data(event):
    print("CB Func:", event.message)


if __name__ == "__main__":
    client = GuardianClient(api_token=my_api_token)
    client.address = asyncio.run(client.search_device())

    client.subscribe_live_insights(raw_eeg=True, filtered_eeg=True, handler=print_data)
    # TODO: to be implemented
    # client.subscribe_realtime_predictions(fft=True, jaw_clench=False, handler=print_data)

    # start a recording session
    asyncio.run(
        client.start_recording(
            recording_timer=RECORDING_TIMER,
            led_sleep=LED_SLEEP,
        )
    )