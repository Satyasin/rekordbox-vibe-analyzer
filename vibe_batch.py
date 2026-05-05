import librosa
import numpy as np
import xml.etree.ElementTree as ET
import os
import shutil
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
INPUT_XML = "collection_export.xml"
OUTPUT_XML = "collection_vibe_updated.xml"

def get_vibe(file_path):
    """
    v3.0: 4-Point Analysis
    E: High-Res Log Energy
    B: Spectral Rolloff (Percussion friendly)
    S: Energy Swing (Progression Category)
    """
    try:
        duration = librosa.get_duration(path=file_path)
        
        # 4 sampling points: [Offset, Weight]
        sample_plan = [
            (0, 0.10),               # Intro
            (duration * 0.35, 0.20), # Build
            (duration * 0.50, 0.50), # Peak
            (duration * 0.75, 0.20)  # Outro/Post-drop
        ]
        
        energies = []
        rolloffs = []
        
        for offset, weight in sample_plan:
            y, sr = librosa.load(file_path, offset=offset, duration=15)
            
            # Raw Metrics
            rms = np.mean(librosa.feature.rms(y=y))
            roll = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
            
            # Store weighted values for final score, but raw for Swing
            energies.append(rms)
            rolloffs.append(roll * weight)
            
        # --- 1. ENERGY (E) ---
        weighted_energy = (energies[0]*0.1 + energies[1]*0.2 + energies[2]*0.5 + energies[3]*0.2)
        log_e = np.log10(weighted_energy + 1e-6)
        energy_score = np.clip((log_e - (-2.0)) / (-0.3 - (-2.0)), 0.0, 1.0)

        # --- 2. BRIGHTNESS (B) ---
        final_rolloff = sum(rolloffs)
        brightness_score = np.clip((final_rolloff - 2000) / (8000 - 2000), 0.0, 1.0)
        
        # --- 3. SWING (S) ---
        # Calculate range based on log energy to keep scale consistent
        log_energies = [np.log10(e + 1e-6) for e in energies]
        # Normalize these log values to 0-1 scale to find the delta
        norm_energies = [(le - (-2.0)) / (-0.3 - (-2.0)) for le in log_energies]
        swing_range = max(norm_energies) - min(norm_energies)
        
        if swing_range < 0.15:
            swing_cat = "L" # Linear/Steady
        elif swing_range < 0.35:
            swing_cat = "B" # Building
        else:
            swing_cat = "D" # Dramatic
        
        return f"E:{energy_score:.2f} B:{brightness_score:.2f} S:{swing_cat}"

    except Exception:
        return None

def main():
    if os.path.exists(INPUT_XML):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        shutil.copy(INPUT_XML, f"backup_{timestamp}_{INPUT_XML}")
        print(f"🛡️  Backup created.")
    else:
        print(f"❌ Error: {INPUT_XML} not found.")
        return

    tree = ET.parse(INPUT_XML)
    root = tree.getroot()
    tracks = root.find('COLLECTION').findall('TRACK')
    
    total = len(tracks)
    print(f"🚀 Starting v3.0 (Energy, Brightness, Swing) on {total} tracks...")

    for i, track in enumerate(tracks):
        location = track.get('Location')
        clean_path = urllib.parse.unquote(location.replace('file://localhost', ''))
        
        if not os.path.exists(clean_path):
            continue

        vibe_tag = get_vibe(clean_path)
        if vibe_tag:
            track.set('Comments', vibe_tag)
            print(f"[{i+1}/{total}] ✅ {vibe_tag} | {os.path.basename(clean_path)}")

    tree.write(OUTPUT_XML, encoding="UTF-8", xml_declaration=True)
    print(f"\n✨ SUCCESS! v3.0 file saved as: {OUTPUT_XML}")

if __name__ == "__main__":
    main()