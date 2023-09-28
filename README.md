# Active learning - Linux Python SDK - Audio

This example comes from the [Edge Impulse Linux Python SDK](https://github.com/edgeimpulse/linux-sdk-python/) that has been slightly modify to upload the raw data back to Edge Impulse based on the inference results.

To run the example:

1. Install the depedencies:

```
pip3 install -r requirements.txt
```

2. Grab your the API key of the project you want to upload the infered results raw data:

![EI API KEY](/assets/grab-api-key.png)

3. Past the new key in the `EI_API_KEY` variable in the `audio-classify-export.py` file:

4. Run the script:

```
python3 audio-classify-export.py modelfile.eim yes,no 0.6 0.8
```

Here are the arguments you can set:

* `modelfile.eim`, path the model.eim
* `yes,no`, labels to upload, separated by comas, no space
* `0.6`, low confidence threshold
* `0.8`, high confidence threshold
* `<audio_device_ID, optional>`

In a keyword spotting model, it can give the following results:

```
python3 audio-classify-export.py modelfile.eim yes,no 0.6 0.8
['modelfile.eim', 'yes,no', '0.6', '0.8']
{'model_parameters': {'axis_count': 1, 'frequency': 16000, 'has_anomaly': 0, 'image_channel_count': 0, 'image_input_frames': 0, 'image_input_height': 0, 'image_input_width': 0, 'input_features_count': 16000, 'interval_ms': 0.0625, 'label_count': 4, 'labels': ['no', 'noise', 'unknown', 'yes'], 'model_type': 'classification', 'sensor': 1, 'slice_size': 4000, 'use_continuous_mode': True}, 'project': {'deploy_version': 29, 'id': 10487, 'name': 'Keywords Detection', 'owner': 'Demo Team'}}
Loaded runner for "Demo Team / Keywords Detection"
0 --> MacBook Pro Microphone
2 --> Microsoft Teams Audio
3 --> Descript Loopback Recorder
4 --> ZoomAudioDevice
Type the id of the audio device you want to use: 
0
selected Audio device: 0

Result (0 ms.) no: 0.18 noise: 0.16     unknown: 0.20   yes: 0.46
Result (0 ms.) no: 0.13 noise: 0.58     unknown: 0.22   yes: 0.07
Result (0 ms.) no: 0.00 noise: 0.89     unknown: 0.10   yes: 0.01
Result (0 ms.) no: 0.00 noise: 0.01     unknown: 0.04   yes: 0.95
Result (0 ms.) no: 0.00 noise: 0.82     unknown: 0.10   yes: 0.07
Result (0 ms.) no: 0.02 noise: 0.77     unknown: 0.13   yes: 0.08
Result (0 ms.) no: 0.01 noise: 0.14     unknown: 0.26   yes: 0.59
Result (0 ms.) no: 0.07 noise: 0.76     unknown: 0.15   yes: 0.01
Result (0 ms.) no: 0.04 noise: 0.24     unknown: 0.11   yes: 0.61       Uploading sample to Edge Impulse...
Successfully uploaded audio to Edge Impulse.

Result (0 ms.) no: 0.02 noise: 0.93     unknown: 0.04   yes: 0.00
Result (0 ms.) no: 0.01 noise: 0.67     unknown: 0.32   yes: 0.01
Result (0 ms.) no: 0.02 noise: 0.18     unknown: 0.23   yes: 0.57
Result (0 ms.) no: 0.07 noise: 0.70     unknown: 0.22   yes: 0.01
Result (0 ms.) no: 0.03 noise: 0.83     unknown: 0.12   yes: 0.02
Result (0 ms.) no: 0.24 noise: 0.44     unknown: 0.21   yes: 0.11
Result (0 ms.) no: 0.23 noise: 0.25     unknown: 0.42   yes: 0.10
Result (0 ms.) no: 0.04 noise: 0.76     unknown: 0.18   yes: 0.02
Result (0 ms.) no: 0.16 noise: 0.67     unknown: 0.12   yes: 0.05
Result (0 ms.) no: 0.12 noise: 0.81     unknown: 0.06   yes: 0.01
Result (0 ms.) no: 0.54 noise: 0.24     unknown: 0.12   yes: 0.10
Result (0 ms.) no: 0.01 noise: 0.91     unknown: 0.05   yes: 0.03
Result (0 ms.) no: 0.65 Uploading sample to Edge Impulse...
Successfully uploaded audio to Edge Impulse.
noise: 0.08     unknown: 0.17   yes: 0.10
Result (0 ms.) no: 0.00 noise: 0.96     unknown: 0.03   yes: 0.00
Result (0 ms.) no: 0.04 noise: 0.80     unknown: 0.13   yes: 0.03
Result (0 ms.) no: 0.03 noise: 0.27     unknown: 0.16   yes: 0.54
Result (0 ms.) no: 0.05 noise: 0.66     unknown: 0.15   yes: 0.14
Result (0 ms.) no: 0.08 noise: 0.74     unknown: 0.14   yes: 0.04
Result (0 ms.) no: 0.01 noise: 0.87     unknown: 0.11   yes: 0.02
Result (0 ms.) no: 0.01 noise: 0.87     unknown: 0.06   yes: 0.06
...
```

![results](/assets/results.gif)
