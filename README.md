# DJ Intelligence Pro (v3.0)

An automated audio analysis tool for Rekordbox libraries that uses Digital Signal Processing (DSP) to categorize tracks by Energy, Brightness, and Dynamic Swing.

## 🚀 Key Features
- **High-Res Energy (E):** Logarithmic RMS scaling calibrated for modern club loudness standards.
- **Spectral Rolloff Brightness (B):** Measures high-frequency "shimmer" (e.g., Afro House shakers) without being skewed by heavy bass.
- **Energy Swing (S):** Categorizes track progression into **Linear (L)**, **Building (B)**, or **Dramatic (D)**.

## 🛠 Technical Stack
- **Language:** Python 3.x
- **Core Library:** Librosa (Audio Analysis)
- **Integration:** XML ElementTree (Rekordbox Export/Import)

## 📖 How to Use
1. Export your Rekordbox Collection as an XML file named `collection_export.xml`.
2. Place the XML in this directory.
3. Run the script: `python3 vibe_batch.py`.
4. Import the generated `collection_vibe_updated.xml` back into Rekordbox.