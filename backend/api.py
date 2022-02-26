from piano_transcription_inference import PianoTranscription, sample_rate, load_audio

transcriptor = PianoTranscription(device='cuda')

'''
Param: file path
Return: a list of dict
    {
        onset_time: starting time of the note (in second)
        offset_time: ending time of the note (in second)
        midi_note: C4=60, F6=89
        velocity: amplitude, 0~127
    }
'''

def transcribe_audio(filepath):
    (audio, _) = load_audio(filepath, sr=sample_rate, mono=True)
    transcribed_dict = transcriptor.transcribe(audio, None)
    notes = transcribed_dict['est_note_events']
    notes.sort(key = lambda x: x['onset_time'])
    return notes

if __name__ == "__main__":
    print(transcribe_audio('music/snowflake.mp3'))