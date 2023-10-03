import os
import sys
import getopt
import signal
import time
import requests
import numpy as np
from scipy.io import wavfile
from edge_impulse_linux_custom.audio import AudioImpulseRunner

# Global variables
runner = None
EI_API_KEY = os.environ.get('EI_API_KEY') # add your Edge Impulse API key here or add it to your environment variables


# Signal handler function to handle interruptions gracefully
def signal_handler(sig, frame):
    print('Interrupted')
    if runner:
        runner.stop()
    sys.exit(0)

# Set up the signal handler for interrupt signals
signal.signal(signal.SIGINT, signal_handler)

# Function to display help message for command-line usage
def help():
    print('python3 classify.py <path_to_model.eim> <labels_to_upload, separated by comas, no space> <low_confidence_threshold> <high_confidence_threshold> <audio_device_ID, optional>' )

# Function to export audio data to Edge Impulse
def export_audio(data, freq, label='unknown', save=True):
    print("Uploading sample to Edge Impulse...")

    # Define the API endpoint for uploading audio data to the training endpoint.
    # Change this URL if you want to upload to a different endpoint (e.g., testing or anomaly).
    endpoint_url = 'https://ingestion.edgeimpulse.com/api/training/files'

    # Create the headers for the request, including the API key and label.
    headers = {
        'x-label': label,
        'x-api-key': EI_API_KEY,
    }

    try:
        # Create a temporary WAV file to store the audio data.
        timestamp = int(time.time())
        filename = f'{label}.{timestamp}.wav'
        wavfile.write(filename, freq, data)

        # Open and upload the WAV file to Edge Impulse.
        with open(filename, 'rb') as audio_file:
            files = {'data': (os.path.basename(filename), audio_file, 'audio/wav')}
            response = requests.post(url=endpoint_url, headers=headers, files=files)

        # Check the response status code to determine if the upload was successful.
        if response.status_code == 200:
            print('Successfully uploaded audio to Edge Impulse.')
        else:
            print('Failed to upload audio to Edge Impulse.')
            print('Response status code:', response.status_code)
            print('Response content:', response.content)

    except Exception as e:
        print('An error occurred while uploading audio:', str(e))
        
    finally:
        # Remove the temporary WAV file if save is False.
        if not save:
            os.remove(filename)

# Main function to run the classification
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) == 0:
        help()
        sys.exit(2)

    model = args[0]
    labels_to_upload = list(args[1].split(","))
    low_threshold =  float(args[2])
    high_threshold = float(args[3])
    print(args)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    with AudioImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            print(model_info)
            freq = model_info['model_parameters']['frequency']
            labels = model_info['model_parameters']['labels']
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

            # Initialize an empty array for audio features
            features = np.array([], dtype=np.int16)

            # Let the library choose an audio interface suitable for this model,
            # or pass device ID parameter to manually select a specific audio interface
            selected_device_id = None
            selected_device_id = 2

            if len(args) >= 5:
                selected_device_id = int(args[4])
                print("Device ID " + str(selected_device_id) + " has been provided as an argument.")

            # Main loop for classification
            for res, audio, features in runner.classifier(device_id=selected_device_id):
                
                print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    print('%s: %.2f\t' % (label, score), end='')
                    if (label in labels_to_upload) and (score > low_threshold) and (score < high_threshold):
                        export_audio(features, freq, label)

                print('', flush=True)

        finally:
            if runner:
                runner.stop()

if __name__ == '__main__':
    main(sys.argv[1:])