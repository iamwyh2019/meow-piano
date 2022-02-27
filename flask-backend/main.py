import os, time
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from Meow import Meow
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
from scipy.io import wavfile

alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'

def getId():
    return ''.join([random.choice(alphabet) for i in range(16)])

def splitName(name):
    namelist = name.split('.')
    return '.'.join(namelist[:-1]), namelist[-1]

app = Flask(__name__, static_folder = './static')
upl_folder = 'upload'
app.config['UPLOAD_FOLDER'] = upl_folder

CORS(app, resources = r'/*')

transcriptor = PianoTranscription(device='cuda')
Meow_piano = Meow(allow_changetone = True, allow_highest_tone = 90, 
    threshold = 0.8, window_interval = 0.1)



@app.route('/', methods = ['POST'])
def work():
    f = request.files['file']
    fname, fext = splitName(f.filename)
    tempid = getId()
    newName = fname + tempid + '.' + fext
    newPath = os.path.join(upl_folder, newName)
    f.save(newPath)

    (audio, _) = load_audio(newPath, sr=sample_rate, mono=True)
    transcribed_dict = transcriptor.transcribe(audio, None)
    notes = transcribed_dict['est_note_events']
    notes.sort(key = lambda x: x['onset_time'])

    newJson = Meow_piano.transcriptMidijson(notes)
    songlist = Meow_piano.generateSonglist()

    resName = fname + tempid + '.wav'
    aftName = fname + tempid + '.mp3'

    songpath = os.path.join('static', resName)
    wavfile.write(songpath, Meow_piano.sr, songlist)

    aftPath = os.path.join('static', aftName)

    os.remove(newPath)
    os.remove(songpath)

    os.system(f'ffmpeg -i {songpath} -f mp3 -acodec libmp3lame -y {aftPath}')

    for i in range(len(newJson)):
        ele = newJson[i]
        ele['onset_time'] = ele['onset_time'].item()
        ele['offset_time'] = ele['offset_time'].item()

    return jsonify({
        'file': aftName,
        'json': newJson
    })


if __name__ == "__main__":
    app.run(port = 5001)