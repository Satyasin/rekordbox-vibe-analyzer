import numpy as np
import librosa
import os

def test_signal_processing():
    print("🧪 Running Test: Signal Processing...")
    # Create a 2-second synthetic tone
    sr = 22050
    t = np.linspace(0, 2, 2 * sr)
    y = 0.5 * np.sin(2 * np.pi * 440 * t)
    test_file = "test_tone.wav"
    
    import soundfile as sf
    sf.write(test_file, y, sr)
    
    # Verify Librosa can load and process it
    try:
        y_loaded, sr_loaded = librosa.load(test_file)
        rms = np.mean(librosa.feature.rms(y=y_loaded))
        
        if rms > 0:
            print(f"✅ Pass: Analyzer calculated energy: {rms:.4f}")
        else:
            print("❌ Fail: Analyzer returned zero energy.")
    except Exception as e:
        print(f"❌ Fail: Error during processing: {e}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_signal_processing()
