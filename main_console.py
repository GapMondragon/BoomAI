import pyaudio
 
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
   frames_per_buffer=FRAMES_PER_BUFFER
)

import websockets
import asyncio
import base64
import json
from configure import auth_key
 
# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 
 
def process_result(sampSent):
    # split the sample sentence into a list
    sentList = sampSent.split()
    
    # create empty list
    newList = []

    # declare consonants and vowels
    consonantsss = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z","B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Y","Z"]
    vowelsss = ["a","e","i","o","u","A","E","I","O","U"]

    # for every item in sentList list
    for i in (sentList):
        # if last character is a vowel
        if i[-1:] in vowelsss:
            # append '-v' to it and add to newList
            newList.append(f"{i}-v")
        # if last character is a consonant
        elif i[-1:] in consonantsss:
            # append '-c' to it and add to newList
            newList.append(f"{i}-c")
        # if neither consonant nor vowel, assume it is a comma,period,question mark, or exclamation point
        else:
            # create placeholders to separately append to newlist
            befstr = i[:-1]
            nonLetter = i[-1:]

            if befstr[-1:] in vowelsss:
                # append '-v' to it and add to newList
                newList.append(f"{befstr}-v")
            elif befstr[-1:] in consonantsss:
                # append '-c' to it and add to newList
                newList.append(f"{befstr}-c")
            # append {nonLetter} to newList
            newList.append(nonLetter)

    # join the list with spaces
    newSent = (' '.join(newList))
    # delete whitespace
    commaRep = newSent.replace(" ,", ",")
    periodRep = commaRep.replace(" .", ".")
    exclaRep = periodRep.replace(" !", "!")
    quesRep = exclaRep.replace(" ?", "?")
    return quesRep

async def send_receive():
   print(f'Connecting websocket to url ${URL}')
   async with websockets.connect(
       URL,
       extra_headers=(("Authorization", auth_key),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           while True:
               try:
                   data = stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               await asyncio.sleep(0.01)
          
           return True
      
       async def receive():
           while True:
               try:
                    result_str = await _ws.recv()  
                    if json.loads(result_str)['message_type'] == 'FinalTranscript': 
                        result = (json.loads(result_str)['text'])
                        final = process_result(result)
                        print(final)
                    
                    # print(json.loads(result_str)['text']) 
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
      
       send_result, receive_result = await asyncio.gather(send(), receive())

while True:
	asyncio.run(send_receive())


