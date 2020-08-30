from pydub import AudioSegment
song = AudioSegment.from_mp3("01.mp3")
first_10_seconds = song[:10000]
last_5_seconds = song[-5000:]
целая = first_10_seconds + last_5_seconds
целая.export("mashup.mp3", format="mp3")