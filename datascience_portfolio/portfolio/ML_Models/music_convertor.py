
import os
from django.conf import settings
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import music21
import pygame
import time

# Define the DQN agent class
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural network to approximate the Q-function
        model = tf.keras.Sequential()
        model.add(layers.Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)
        for i in minibatch:
            state, action, reward, next_state, done = self.memory[i]
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            q_values = self.model.predict(state)
            q_values[0][action] = target
            self.model.fit(state, q_values, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# Define the function to preprocess the input data
def preprocess_data(notes):
    # Map notes to integers
    pitchnames = sorted(set(item for item in notes))
    note_to_int = {note: number for number, note in enumerate(pitchnames)}
    int_to_note = {number: note for number, note in enumerate(pitchnames)}
    sequence_length = 100
    network_input = []
    network_output = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(len(set(notes)))
    network_output = tf.keras.utils.to_categorical(network_output)
    return network_input, network_output, note_to_int, int_to_note

# Define the function to train the DQN agent
def train_agent(agent, network_input, network_output, epochs, batch_size):
    for i in range(epochs):
#         print('Epoch {}/{}'.format(i + 1, epochs))
        agent.replay(batch_size)

# Define the function to generate new music
def music_conversion(midi_file_path):
    try:
        # Load MIDI file
        midi_file = music21.converter.parse(midi_file_path)

        # Extract notes and chords from MIDI file
        notes = []
        for element in midi_file.flat:
            if isinstance(element, music21.note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, music21.chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
            
        # Check if the notes list is empty
        if not notes:
            raise ValueError("Invalid MIDI file. No notes or chords found.")

        # Preprocess the input data
        network_input, network_output, note_to_int, int_to_note = preprocess_data(notes)

        # Reshape the network_output array to have an extra dimension
        network_output = np.reshape(network_output, (*network_output.shape, 1))

        # Set the input and output sizes
        state_size = network_input.shape[1]
        action_size = len(note_to_int)

        # Initialize the DQN agent
        agent = DQNAgent(state_size, action_size)

        # Train the DQN agent
        epochs = 100
        batch_size = 64
        train_agent(agent, network_input, network_output, epochs, batch_size)

        # Generate new music using the DQN agent
        generated_notes = []
        start_note = np.random.randint(0, len(network_input) - 1)
        pattern = network_input[start_note]

        for i in range(500):
            pattern_reshaped = np.reshape(pattern, (1, *pattern.shape))
            action = agent.act(pattern_reshaped)
            result = int_to_note[action]
            generated_notes.append(result)

            pattern = np.append(pattern, action)
            pattern = pattern[1:]

        # Create a new MIDI file with the generated notes
        offset = 0
        output_notes = []
        for pattern in generated_notes:
            if '.' in pattern:
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    new_note = music21.note.Note(int(current_note))
                    new_note.storedInstrument = music21.instrument.Piano()
                    notes.append(new_note)
                new_chord = music21.chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            else:
                try:
                    new_note = music21.note.Note(pattern)
                except music21.pitch.PitchException:
                    new_note = music21.note.Rest()
                new_note.offset = offset
                new_note.storedInstrument = music21.instrument.Piano()
                output_notes.append(new_note)

            offset += 0.5

        # Save the generated music as a new MIDI file
        # new_midi_file_path = midi_file_path.replace('.mid', 'output_music.mid')
        new_midi_file_path = os.path.join(settings.BASE_DIR,'static/music') +'/output_music.mid'

        midi_stream = music21.stream.Stream(output_notes)
        midi_stream.write('midi', fp=new_midi_file_path)

        return new_midi_file_path
    
    except Exception as e:
        return "Invalid File: " + str(e)




