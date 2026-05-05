# Rekordbox Vibe Analyzer v3.0

An intelligent Python-based utility designed to automate the metadata enrichment of Rekordbox libraries. This tool uses Digital Signal Processing (DSP) to analyze track characteristics that standard software often misses.

---

## 🛑 The Problem Statement
Managing a large DJ library makes manual tagging nearly impossible. Standard software provides BPM and Key, but fails to quantify the **"vibe"**—the energy flux, the rhythmic complexity (swing), and the sonic brightness. Without these metrics, DJs spend more time scrolling and less time transitioning creatively.

## 🚀 What the Tool Does
The Analyzer parses a Rekordbox XML export, analyzes each audio file using the `Librosa` library, and calculates three custom metrics:
1.  **Energy Swing:** Detects rhythmic "groove" vs. "straight" beats.
2.  **Spectral Brightness:** Identifies "dark" underground tracks vs. "bright" mainstage tracks.
3.  **Vibe Score:** A composite metric that identifies the track's functional role in a set.

## 🧠 How it Works
The script follows a 4-step pipeline:
*   **Parsing:** Reads the `collection.xml` to locate track file paths.
*   **DSP Analysis:** Uses Fast Fourier Transforms (FFT) to analyze Spectral Rolloff and Onset Strength.
*   **Scaling:** Normalizes values to a 1–10 scale for easy reading.
*   **XML Injection:** Writes the new data back into the `Comment` or `Color` fields of a new XML file.

---

## 📊 How to Read the Output
The tool outputs a specialized string into the **Comment** field:
`[E: 8.2 | B: 4.5 | S: 6.0]`

| Metric | Meaning | High Value (8-10) | Low Value (1-3) |
| :--- | :--- | :--- | :--- |
| **Energy (E)** | Intensity | Peak-hour Techno/Trance | Ambient/Chill-out |
| **Brightness (B)** | High Frequencies | Crisp Hi-hats/Synths | Muddy/Deep/Dubby |
| **Swing (S)** | Rhythmic Groove | Organic House/Jazz-swing | Industrial/Straight 4x4 |

---

## ✅ Benefits & Lacunas
### **Benefits**
*   **Consistency:** Eliminates subjective "mood" tagging.
*   **Speed:** Processes bulk libraries faster than manual auditioning.
*   **Discovery:** Find hidden gems with high energy in your older folders.

### **Lacunas (Things to check)**
*   **CPU Intensive:** Analyzing 6,000+ tracks can take significant time; run in batches.
*   **File Paths:** Ensure your Rekordbox XML export uses absolute file paths.
*   **Genre Bias:** A "bright" Techno track may still be "darker" than a "bright" Pop track.

---

## 🛠 How to Use
### 1. Generate XML
In Rekordbox, go to **File -> Export Collection in xml format**. Save it as `collection_export.xml`.

### 2. Run the Script
Ensure you have the requirements installed:
```bash
pip install -r requirements.txt
python vibe_batch.py

### **3. Import back to Rekordbox**

The script will generate collection_vibe_updated.xml.

In Rekordbox, go to Preferences -> View -> Layout and enable rekordbox xml.

In the tree view (left panel), click the XML icon.

Right-click the tracks and select Import to Collection. Your comments will now be updated!

🔮 Future Functionalities
**Camelot Key Auto-Correction:** Verification of Rekordbox key detection.

**Vocal Detection:** Flagging tracks as "Instrumental" vs "Vocal".

**Auto-Playlist Generation:** Creating "Vibe Playlists" based on Energy/Swing thresholds.

💬 Feedback
This is an evolving project by a DJ/Product Manager. If you find edge cases where the energy detection feels "off," please open an Issue or reach out. Your feedback helps refine the DSP logic!

Developed by Satyajeet Aparadh (Satyasin)
