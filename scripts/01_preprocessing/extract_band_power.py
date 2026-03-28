import os
import mne
import pyxdf
import numpy as np
import pandas as pd
from mne.time_frequency import psd_array_welch

# Configuration

data_path = r"Projet_EEG2\data_primaire"

FREQUENCY_BANDS = {
'theta': (4, 8),
'alpha': (8, 12)
}

ROI_CHANNELS = {
'theta': ['AF3', 'F7', 'F3', 'F4', 'F8', 'AF4'],
'alpha': ['P7', 'O1', 'O2', 'P8']
}

CONDITION_KEYWORDS = {
'paper': ['papier', 'paper'],
'standard': ['standard', 'st'],
'adaptive': ['adapt', 'neuro', 'comp']
}

def process_xdf_file(file_path):
try:
streams, _ = pyxdf.load_xdf(file_path)

```
    eeg_stream = None
    for stream in streams:
        channel_count = int(stream['info']['channel_count'][0])
        stream_type = stream['info']['type'][0]
        if 'EEG' in stream_type and channel_count >= 14:
            eeg_stream = stream
            break

    if eeg_stream is None:
        return None

    data = eeg_stream['time_series'].T
    sfreq = float(eeg_stream['info']['nominal_srate'][0])
    ch_names = [c['label'][0] for c in eeg_stream['info']['desc'][0]['channels'][0]['channel']]

    mapping = {name: name.replace('EEG.', '') for name in ch_names}
    info = mne.create_info(ch_names, sfreq, ch_types='eeg')

    raw = mne.io.RawArray(data, info, verbose=False)
    raw.rename_channels(mapping)

    montage_channels = ['AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4']
    available_channels = [ch for ch in montage_channels if ch in raw.ch_names]
    raw.pick(available_channels)

    if len(raw.ch_names) == 0:
        return None

    raw.filter(1., 40., verbose=False)
    raw.set_eeg_reference('average', verbose=False)

    data_array = raw.get_data(start=int(sfreq * 2), stop=int(data.shape[1] - sfreq))

    if data_array.shape[1] < sfreq:
        return None

    psds, freqs = psd_array_welch(
        data_array,
        sfreq,
        fmin=1,
        fmax=40,
        n_fft=int(sfreq * 2),
        verbose=False
    )

    results = {}

    theta_mask = (freqs >= 4) & (freqs <= 8)
    theta_idx = [raw.ch_names.index(ch) for ch in ROI_CHANNELS['theta'] if ch in raw.ch_names]
    results['theta'] = psds[theta_idx][:, theta_mask].mean() if theta_idx else None

    alpha_mask = (freqs >= 8) & (freqs <= 12)
    alpha_idx = [raw.ch_names.index(ch) for ch in ROI_CHANNELS['alpha'] if ch in raw.ch_names]
    results['alpha'] = psds[alpha_idx][:, alpha_mask].mean() if alpha_idx else None

    return results

except Exception:
    return None
```

# Main loop

final_data = []

subjects = [
d for d in os.listdir(data_path)
if os.path.isdir(os.path.join(data_path, d))
]

print(f"Processing {len(subjects)} participants...")

for sub in subjects:
sub_path = os.path.join(data_path, sub)
sub_results = {'subject_id': sub}

```
files = [f for f in os.listdir(sub_path) if f.endswith('.xdf')]

for filename in files:
    file_path = os.path.join(sub_path, filename)
    filename_lower = filename.lower()

    condition = None
    if any(k in filename_lower for k in CONDITION_KEYWORDS['paper']):
        condition = 'paper'
    elif any(k in filename_lower for k in CONDITION_KEYWORDS['standard']):
        condition = 'standard'
    elif any(k in filename_lower for k in CONDITION_KEYWORDS['adaptive']):
        condition = 'adaptive'

    if condition:
        powers = process_xdf_file(file_path)
        if powers:
            sub_results[f'theta_{condition}'] = powers['theta']
            sub_results[f'alpha_{condition}'] = powers['alpha']

final_data.append(sub_results)
```

df_eeg = pd.DataFrame(final_data)

columns_order = [
'subject_id',
'theta_paper','alpha_paper',
'theta_standard','alpha_standard',
'theta_adaptive','alpha_adaptive'
]

existing_cols = [col for col in columns_order if col in df_eeg.columns]
df_eeg = df_eeg[existing_cols]

output_file = os.path.join(data_path, 'eeg_results_primary.csv')
df_eeg.to_csv(output_file, index=False)

print(f"Processing completed. File saved at: {output_file}")
