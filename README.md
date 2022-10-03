# BoomAI
<h2>Task # 4 Using Assembly AI</h2>
<br />
To demonstrate, using your mic, that you are able to perform live transcription from speech and display the text either in a terminal or a simple web UI.<br />
As part of the transcription service, identify the keywords that end in a vowel and append a “-v” to that word. <br />
As part of the transcription service, identify the keywords that end in a consonant and append a “-c” to that word.<br />
Transcript “The quick brown fox” becomes “The-v quick-c brown-c fox-c”<br />
<br />
!!! Always remember to stop / turn off your application to avoid wasting your funds in Assembly AI !!!<br />
<br />
<br />

Operating System: Windows<br />
Python version  : 3.10.1<br />

<h3>Install these dependencies:</h3>
  pip install pyaudio<br />
  pip install websockets<br />
<br />
Edit configure.py and put your API Key from Assembly AI<br />

<h2>----------- Terminal -----------</h2>
To run in terminal, run this command:<br />
  `python main_console.py`<br />
  You may speak when you see the "Sending messages..." <br />
  
To stop the application, go to your terminal:<br />
  Press `Ctrl+C`<br />

<h2>----------- GUI -----------</h2>
To run in a GUI, run this command in your terminal: <br />
  `streamlit run streamlit_gui.py` <br />
  After running streamlit, you will be directed to a new tab in your browser. <br />
  Click "Start Listening" to begin, then you may speak. <br />
  Click "Stop Listing" to stop. <br />
  
To stop the application, go to your terminal:<br />
  Press `Ctrl+C`<br />
