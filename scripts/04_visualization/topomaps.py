import os
import mne
import pyxdf
import numpy as np
import pandas as pd
from mne.time_frequency import psd_array_welch

# Channel definition (Emotiv EPOC X)
CH_NAMES = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

# Function: extract band power per channel
def process_xdf_per_channel(file_path):
    try:
        streams, _ = pyxdf.load_xdf(file_path)
        eeg_stream = next(s for s in streams if 'EEG' in s['info']['type'][0])

        data = eeg_stream['time_series'].T
        sfreq = float(eeg_stream['info']['nominal_srate'][0])

        raw_ch_names = [c['label'][0] for c in eeg_stream['info']['desc'][0]['channels'][0]['channel']]
        mapping = {name: name.replace('EEG.', '') for name in raw_ch_names}

        info = mne.create_info(raw_ch_names, sfreq, ch_types='eeg')
        raw = mne.io.RawArray(data, info, verbose=False)
        raw.rename_channels(mapping)
        raw.pick(CH_NAMES)

        # Preprocessing
        raw.filter(1., 40., verbose=False)
        raw.set_eeg_reference('average', verbose=False)

        # Power spectral density (Welch)
        data_array = raw.get_data(start=int(sfreq * 2), stop=int(data.shape[1] - sfreq * 2))
        psds, freqs = psd_array_welch(
            data_array,
            sfreq,
            fmin=1,
            fmax=40,
            n_fft=int(sfreq * 2),
            verbose=False
        )

        # Extract band power per channel
        theta_mask = (freqs >= 4) & (freqs <= 8)
        alpha_mask = (freqs >= 8) & (freqs <= 12)

        results = {}
        for i, ch in enumerate(CH_NAMES):
            results[f'{ch}_theta'] = psds[i, theta_mask].mean()
            results[f'{ch}_alpha'] = psds[i, alpha_mask].mean()

        return results, info

    except Exception:
        return None

# Processing loop (channel-level extraction)
subjects_clean = df_clean['subject_id'].tolist()
all_channels_data = []

for sub in subjects_clean:
    sub_path = os.path.join(data_path, sub)
    sub_row = {'subject_id': sub}

    for filename in os.listdir(sub_path):
        if not filename.endswith('.xdf'):
            continue

        name = filename.lower()
        condition = None

        if 'papier' in name:
            condition = 'No-screen'
        elif 'standard' in name or 'st' in name:
            condition = 'standard'
        elif 'adapt' in name or 'comp' in name:
            condition = 'adaptive'

        if condition:
            result = process_xdf_per_channel(os.path.join(sub_path, filename))

            if result:
                ch_results, info = result

                for key, val in ch_results.items():
                    sub_row[f'{key}_{condition}'] = val

    all_channels_data.append(sub_row)

df_topo = pd.DataFrame(all_channels_data)

# Select EEG columns
eeg_columns = [col for col in df_topo.columns if 'theta' in col or 'alpha' in col]

# Log transformation (dB)
for col in eeg_columns:
    df_topo[col] = 10 * np.log10(df_topo[col])



import mne
import matplotlib.pyplot as plt

# Montage and channel configuration
CH_NAMES = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
montage = mne.channels.make_standard_montage('standard_1020')
info = mne.create_info(CH_NAMES, sfreq=128, ch_types='eeg')
info.set_montage(montage)

# Topomap plotting function
def plot_topomaps(df, band='theta'):
    conditions = ['No-screen', 'standard', 'adaptive']
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))

    cols = [c for c in df.columns if band in c]
    vmin = df[cols].mean().min()
    vmax = df[cols].mean().max()

    for i, cond in enumerate(conditions):
        data_cols = [f'{ch}_{band}_{cond}' for ch in CH_NAMES]
        existing_cols = [c for c in data_cols if c in df.columns]

        if len(existing_cols) == len(CH_NAMES):
            grand_average = df[existing_cols].mean().values

            im, _ = mne.viz.plot_topomap(
                grand_average,
                info,
                axes=axes[i],
                show=False,
                names=CH_NAMES,
                cmap='Reds',
                vlim=(vmin, vmax)
            )
            axes[i].set_title(cond.capitalize(), fontsize=15)
        else:
            axes[i].set_title(f"{cond}\n(missing data)", fontsize=10)

    cbar_ax = fig.add_axes([0.92, 0.25, 0.015, 0.5])
    fig.colorbar(im, cax=cbar_ax, label=f'{band.capitalize()} power (dB)')

    plt.suptitle(f'{band.capitalize()} power topography (N={len(df)})', fontsize=18)
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig(f"EN-topomap_{band}.pdf", bbox_inches='tight')
    #plt.savefig(f"EN-topomap_{band}.png", dpi=300, bbox_inches='tight')
    plt.show()

# Generate topomaps
plot_topomaps(df_topo, band='theta')
plot_topomaps(df_topo, band='alpha')


import matplotlib.pyplot as plt

# Topomap: adaptive vs standard difference (theta)
fig, ax = plt.subplots(figsize=(8, 8))

adapt_cols = [f'{ch}_theta_adaptive' for ch in CH_NAMES]
standard_cols = [f'{ch}_theta_standard' for ch in CH_NAMES]

diff_data = df_topo[adapt_cols].mean().values - df_topo[standard_cols].mean().values

im, _ = mne.viz.plot_topomap(
    diff_data,
    info,
    axes=ax,
    cmap='RdBu_r',
    vlim=(-1.5, 1.5),
    names=CH_NAMES,
    show=False
)

cbar_ax = fig.add_axes([0.88, 0.25, 0.03, 0.5])
fig.colorbar(im, cax=cbar_ax, label='Theta difference (dB)')

ax.set_title(
    "Adaptive vs standard condition effect on cognitive load (N=36)",
    fontsize=15,
    pad=25
)
plt.rcParams['pdf.fonttype'] = 42

plt.savefig(
    "EN-theta_difference_topomap.pdf",
    bbox_inches='tight'
)
#plt.savefig("EN-theta_difference_topomap.png", dpi=300, bbox_inches='tight')
plt.show()
