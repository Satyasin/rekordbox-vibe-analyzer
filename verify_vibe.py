import librosa
import numpy as np
import os
import warnings

# This hides those messy metadata warnings to keep your screen clean
warnings.filterwarnings("ignore")

def analyze_track(file_path):
    try:
        # Load 45s of the track
        y, sr = librosa.load(file_path, duration=45, sr=22050)
        
        # Calculate Energy (RMS)
        rms = librosa.feature.rms(y=y)
        # We round(x, 2) to get 0.96 instead of 0.959999...
        energy = round(min(1.0, np.mean(rms) * 4.5), 2)
        
        # Calculate Brightness (Spectral Centroid)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        brightness = round(min(1.0, np.mean(centroid) / 5000), 2)
        
       # This formatting {energy:.2f} forces exactly 2 decimal places
        print(f"E:{energy:.2f} B:{brightness:.2f}")

    except Exception as e:
        print(f"Error analyzing {os.path.basename(file_path)}: {e}")

if __name__ == "__main__":
    # Your test path
    test_path = "/Users/satya/Desktop/Music/2025/Nov 2025/John_Summit__Hayla-Shiver-Radio_Edit-75568674.mp3" 
    analyze_track(test_path)