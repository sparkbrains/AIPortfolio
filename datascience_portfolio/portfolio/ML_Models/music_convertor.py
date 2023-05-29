
import music21
import re
from music21 import converter, instrument, note, chord
from pydub import AudioSegment
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pickle
import numpy
import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
from music21 import converter, instrument, note, chord, stream, chord, midi, tempo

from keras.layers import Bidirectional
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from tqdm import tqdm
import glob
from django.conf import settings



def music_conversion(file):
    notes = []
    midi = converter.parse(file)

    # Extract notes from the MIDI file
    parts = instrument.partitionByInstrument(midi)
    if parts:
        notes_to_parse = parts.parts[0].recurse()
    else:
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
    n_vocab = len(set(notes))
    pitchnames = sorted(set(item for item in notes))
    sequence_length = 50

    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    network_input = []
    network_output = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(n_vocab)
    network_output = to_categorical(network_output)
    with open(os.path.join(settings.BASE_DIR,'Music_project/int_to_note.pkl'), 'rb') as f:
        int_to_note = pickle.load(f)
    model = load_model( os.path.join(settings.BASE_DIR,'Music_project/weights.234.0.8730.hdf5'))
    """ Generate notes from the neural network based on a sequence of notes """
    start = np.random.randint(0, len(network_input)-1)

    

    pattern = network_input[start]
    prediction_output = []
    for note_index in range(200):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input 

        prediction = model.predict(prediction_input, verbose=0)

        index = np.argmax(prediction)
        if index == pattern[-1] and index== pattern[-2]:
            index = np.random.randint(0,n_vocab-1)
        
        result = int_to_note[index]
        prediction_output.append(result)

        pattern = np.append(pattern, index)
        pattern = pattern[1:len(pattern)]
   
    midi = converter.parse(file)  #read file
    parts = instrument.partitionByInstrument(midi)
    Instr= []
    li=[]
    value_list = list()
    for i in parts:
        ins_1 = i.getInstrument()
        li.append(ins_1)

    double_list = list()
    for hth in li:
        aa  = str(hth).replace(" ", "")
        double_list.append(aa)

    m=[]
    for i in double_list:
        if len(i.split(":"))== 2:
            m.append(i.split(":")[1])

        else:
            m.append(i)
    output_file = add_instruments(m, pattern, prediction_output)
    return output_file



# MUlti - instruments
def add_instruments(m, pattern, prediction_output):
    offset = 0
    output_notes = []
    for pattern in prediction_output:
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                for i in m:
                    if i == 'Piano':
                        output_notes.append(instrument.Piano())
                    if i == 'ElectricGuitar':
                        output_notes.append(instrument.ElectricGuitar())
                       
                    if i == 'Percussion':
                        output_notes.append(instrument.Percussion())
                        
                    if i == 'AcousticBass':
                        output_notes.append(instrument.AcousticBass())
                    if i =="Flute":
                        output_notes.append(instrument.Flute())
                    if i == "Violin":
                        output_notes.append(instrument.Violin())
                    if i == "Choir":
                        output_notes.append(instrument.Choir())
                    if i == "StringInstrument":
                        output_notes.append(instrument.StringInstrument())
                    if i == "BassDrum":
                        output_notes.append(instrument.BassDrum())
                    if i == "ElectricPiano":
                        output_notes.append(instrument.ElectricPiano())
                    if i == "Harp":
                        output_notes.append(instrument.Harp())
                    if i == "Guitar":
                        output_notes.append(instrument.Guitar())
                    if i == "Trumpet":
                        output_notes.append(instrument.Trumpet())
                    if i == "Organ":
                        output_notes.append(instrument.Organ())
                    if i == "ElectricOrgan":
                        output_notes.append(instrument.ElectricOrgan())
                    if i == "AcousticPiano":
                        output_notes.append(instrument.AcousticPiano())
                cn=int(current_note) 
                new_note=note.Note(cn)
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            for i in m:
                    if i == 'Piano':
                        output_notes.append(instrument.Piano())
                    if i == 'ElectricGuitar':
                        output_notes.append(instrument.ElectricGuitar())   
                    if i == 'Percussion':
                        output_notes.append(instrument.Percussion())
                        
                    if i == 'AcousticBass':
                        output_notes.append(instrument.AcousticBass())
                    if i =="Flute":
                        output_notes.append(instrument.Flute())
                    if i == "Violin":
                        output_notes.append(instrument.Violin())
                    if i == "Choir":
                        output_notes.append(instrument.Choir())
                    if i == "StringInstrument":
                        output_notes.append(instrument.StringInstrument())
                    if i == "BassDrum":
                        output_notes.append(instrument.BassDrum())
                    if i == "ElectricPiano":
                        output_notes.append(instrument.ElectricPiano())
                    if i == "Harp":
                        output_notes.append(instrument.Harp())
                    if i == "Guitar":
                        output_notes.append(instrument.Guitar())
                    if i == "Trumpet":
                        output_notes.append(instrument.Trumpet())
                    if i == "Organ":
                        output_notes.append(instrument.Organ())
                    if i == "ElectricOrgan":
                        output_notes.append(instrument.ElectricOrgan())
                    if i == "AcousticPiano":
                        output_notes.append(instrument.AcousticPiano())
                   


            new_note = note.Note(pattern)
            new_note.offset = offset

            output_notes.append(new_note)
    scaling_factor = 0.5 # Adjust the scaling factor as desired

    # Scale the durations of notes and chords
    for element in output_notes:
        if isinstance(element, note.Note) or isinstance(element, chord.Chord):
            element.duration.quarterLength *= scaling_factor
     # output_notes
    midi_stream = stream.Stream()
    midi_stream.append(output_notes)
    midi_stream.insert(0, tempo.MetronomeMark(number=120))  #take any value from list [10,20, 30, 40,50,60,70,90, 100.....160] to add dynamic tempo
    output_file = os.path.join(settings.BASE_DIR,'static/music') +'/output_music.mid'
    midi_stream.write('midi', fp=output_file)
    return output_file




