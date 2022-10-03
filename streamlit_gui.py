import streamlit as st
import websockets
import asyncio
import base64
import json
from configure import auth_key

import pyaudio

if "text" not in st.session_state:
    st.session_state["text"] = "Listening..."
    st.session_state["run"] = False


FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
)


def start_listening():
    st.session_state["run"] = True


def stop_listening():
    st.session_state["run"] = False


st.title("Get real-time transcription")

start, stop = st.columns(2)
start.button("Start listening", on_click=start_listening)

stop.button("Stop listening", on_click=stop_listening)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

def process_result(samp_sent):
    # split the sample sentence into a list
    sent_list = samp_sent.split()
    
    # create empty list
    new_list = []

    # declare consonants and vowels
    consonantsss = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z","B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Y","Z"]
    vowelsss = ["a","e","i","o","u","A","E","I","O","U"]

    # for every item in sent_list list
    for i in (sent_list):
        # if last character is a vowel
        if i[-1:] in vowelsss:
            # append '-v' to it and add to new_list
            new_list.append(f"{i}-v")
        # if last character is a consonant
        elif i[-1:] in consonantsss:
            # append '-c' to it and add to new_list
            new_list.append(f"{i}-c")
        # if neither consonant nor vowel, assume it is a comma,period,question mark, or exclamation point
        else:
            # create placeholders to separately append to new_list
            befstr = i[:-1]
            non_letter = i[-1:]

            if befstr[-1:] in vowelsss:
                # append '-v' to it and add to new_list
                new_list.append(f"{befstr}-v")
            elif befstr[-1:] in consonantsss:
                # append '-c' to it and add to new_list
                new_list.append(f"{befstr}-c")
            # append {non_letter} to new_list
            new_list.append(non_letter)

    # join the list with spaces
    new_sent = (' '.join(new_list))
    # delete whitespace
    comma_rep = new_sent.replace(" ,", ",")
    period_rep = comma_rep.replace(" .", ".")
    excla_rep = period_rep.replace(" !", "!")
    ques_rep = excla_rep.replace(" ?", "?")
    return ques_rep

async def send_receive():

    print(f"Connecting websocket to url ${URL}")

    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", auth_key),),
        ping_interval=5,
        ping_timeout=20,
    ) as _ws:

        r = await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while st.session_state["run"]:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    r = await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    print(e)
                    assert False, "Not a websocket 4008 error"

                r = await asyncio.sleep(0.01)

        async def receive():
            while st.session_state["run"]:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)["text"]

                    if json.loads(result_str)["message_type"] == "FinalTranscript":
                        final = process_result(result)
                        print(final)
                        st.session_state["text"] = final
                        st.markdown(st.session_state["text"])

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    print(e)
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())
