# Rekordbox Vibe Analyzer v3.0

An intelligent Python-based utility designed to automate the metadata enrichment of Rekordbox libraries. This tool uses Digital Signal Processing (DSP) to analyze track characteristics that standard software often misses.

---

## 🛑 The Problem Statement
Managing a large DJ library makes manual tagging nearly impossible. Standard software provides BPM and Key, but fails to quantify the **"vibe"**—the energy flux, the journey of the track, and the sonic brightness. Without these metrics, DJs spend more time scrolling and less time transitioning creatively.

## 🚀 What the Tool Does
The Analyzer parses a Rekordbox XML export, analyzes each audio file using the `Librosa` library, and calculates three essential metrics:
1.  **Energy (E):** Overall intensity and power levels.
2.  **Brightness (B):** High-frequency presence and "air" in the mix.
3.  **Energy Range / Swing (S):** Categorizes the "journey" or "drama" of the track's energy levels.

## 🧠 How it Works
The script follows a 4-step pipeline:
*   **Parsing:** Reads the `collection.xml` to locate track file paths.
*   **DSP Analysis:** Uses Fast Fourier Transforms (FFT) to analyze Spectral Rolloff and Energy Variance.
*   **Scaling:** Normalizes Energy and Brightness to a 0.00–1.00 scale.
*   **Classification:** Maps the Energy Range into three distinct performance categories (L, B, D).

---

## 📊 How to Read the Output
The tool outputs a specialized string into the **Comment** field:
`[E: 0.93 | B: 0.57 | S: L]`

| Metric | Type | What it represents | Example Values |
| :--- | :--- | :--- | :--- |
| **Energy (E)** | 0.00 – 1.00 | Overall intensity and power. | **0.95** (Peak) \| **0.20** (Chill) |
| **Brightness (B)** | 0.00 – 1.00 | High-frequency presence. | **0.85** (Crisp) \| **0.30** (Deep) |
| **Swing (S)** | **Category** | The "Energy Journey" of the track. | **L, B, or D** |

### **Decoding Energy Journey (S) Categories**
*   **S:L (Linear/Steady):** Range < 0.15. Consistent energy throughout. These are your "tools" and loop-friendly tracks.
*   **S:B (Building/Journey):** Range 0.15 - 0.35. Standard tracks that evolve and grow from intro to drop.
*   **S:D (Dramatic/Peak):** Range > 0.35. High-impact tracks with massive builds or high contrast between sections.

---

## ✅ Benefits & Lacunas
### **Benefits**
*   **Consistency:** Eliminates subjective "mood" tagging.
*   **Speed:** Processes bulk libraries faster than manual auditioning.
*   **Precision:** Uses a 0.00-1.00 scale for granular library sorting.

### **Lacunas (Things to check)**
*   **CPU Intensive:** Analyzing large libraries (6,000+ tracks) is heavy; run in batches.
*   **Privacy:** Ensure you do not upload your actual `.xml` data files to public repositories.
*   **File Paths:** Requires local absolute file paths within the XML to locate audio files.

---

## 🛠 How to Use

### 1. Generate XML
In Rekordbox, go to **File -> Export Collection in xml format**. Save it as `collection_export.xml` in the project root.

### 2. Run the Script
This project uses **uv** for high-performance dependency management. Run the analyzer with:

```bash
# Install dependencies and run the script automatically
uv run vibe_batch.py
```
### **3. Import back to Rekordbox**

The script will generate collection_vibe_updated.xml.

In Rekordbox, go to Preferences -> View -> Layout and enable rekordbox xml.

In the tree view (left panel), click the XML icon.

Right-click the tracks and select Import to Collection. Your comments will now be updated!


**🔮 Future Functionalities**

**Camelot Key Auto-Correction:** Verification of Rekordbox key detection.

**Vocal Detection:** Flagging tracks as "Instrumental" vs "Vocal".

**Auto-Playlist Generation:** Creating "Vibe Playlists" based on Energy/Swing thresholds.


**💬 Feedback**
This is an evolving project by a DJ/Product Manager. If you find edge cases where the energy detection feels "off," please open an Issue or reach out. Your feedback helps refine the DSP logic!

**Developed by Satyajeet Aparadh (Satyasin)**
