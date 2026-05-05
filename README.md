# DJ Intelligence Pro: Vibe Analyzer v5.5 🎧

**DJ Intelligence Pro** is a "Human-in-the-Loop" metadata enrichment utility designed for Rekordbox power users. It bridges the gap between raw Digital Signal Processing (DSP) and a DJ’s intuition, allowing you to batch-analyze tracks and manually verify the results through a custom web interface before updating your library.

---

## 🛑 The Problem Statement
Managing a large DJ library makes manual tagging nearly impossible. Standard software provides BPM and Key, but fails to quantify the **"vibe"**—the energy flux, the journey of the track, and the sonic brightness. Without these metrics, DJs spend more time scrolling and less time transitioning creatively.

## 🚀 The "Human-in-the-Loop" Workflow
Unlike automated tools that blindly overwrite data, this tool follows a **Review -> Refine -> Commit** pipeline:
1. **Analysis:** The tool samples 4 distinct points of a track to calculate Energy, Brightness, and Swing.
2. **Verification:** An interactive HTML dashboard allows you to "Accept" or "Skip" suggestions and manually tweak scores.
3. **Safety:** Every run automatically triggers a timestamped backup of your Rekordbox `master.db`.
4. **Integration:** Generates a non-destructive XML for a clean Rekordbox import.

---

## 🧠 The Metrics
The tool analyzes track characteristics using the `Librosa` library across three primary dimensions:

| Metric | Type | What it represents | Example Values |
| :--- | :--- | :--- | :--- |
| **Energy (E)** | 0.00 – 1.00 | Overall intensity and power levels using weighted RMS. | **0.95** (Peak) \| **0.20** (Chill) |
| **Brightness (B)** | 0.00 – 1.00 | High-frequency presence (Spectral Rolloff). | **0.85** (Crisp) \| **0.30** (Deep) |
| **Swing (S)** | **Category** | The "Energy Journey" based on variance across the track. | **L, B, or D** |

### **Decoding Energy Journey (S) Categories**
*   **S:L (Linear/Steady):** Range < 0.15. Consistent energy throughout. These are your "tools" and loop-friendly tracks.
*   **S:B (Building/Journey):** Range 0.15 - 0.35. Standard tracks that evolve and grow from intro to drop.
*   **S:D (Dramatic/Peak):** Range > 0.35. High-impact tracks with massive builds or high contrast between sections.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have `uv` installed for high-performance dependency management.
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```
### 2. Configure Your Database Path (Required)

For safety and path-transparency, you must explicitly point the script to your Rekordbox database.

Open vibe_batch.py in a text editor.

Locate the variable REKORDBOX_DB_PATH.

Replace the placeholder with your actual path.

Reference for macOS: /Users/YOUR_USERNAME/Library/Pioneer/rekordbox/master.db

### 3. Export Your Collection

In Rekordbox, go to File > Export Collection in xml format. Save it as collection_export.xml in the project root folder.

## 📖 Usage Instructions
### Phase 1: Analyze & Review

Run the analyzer on a specific playlist:

```Bash
uv run vibe_batch.py -p "Your Playlist Name"
```
**Database Backup:** A copy of your master.db is moved to /db_backups.

**Interactive UI:** A browser window opens at http://127.0.0.1:5000. Review suggestions, adjust sliders, and click Confirm & Save All.
<img width="1413" height="686" alt="Screenshot 2026-05-05 at 5 20 10 PM" src="https://github.com/user-attachments/assets/e3fbae2f-37de-41df-882b-2d9efab7659a" />



**Lockdown:** Once saved, the UI becomes read-only to ensure data integrity.

<img width="1413" height="686" alt="Screenshot 2026-05-05 at 5 33 18 PM" src="https://github.com/user-attachments/assets/ed4c7d48-3cca-4c37-9714-9cd54974e5c6" />


Return to your terminal and press Ctrl+C to stop the server.

### Phase 2: Generate & Import

```Bash
uv run vibe_batch.py --generate
```
**Final Output:** A fresh XML is created in /vibe_outputs.

**Import:** In Rekordbox, go to File > Import > Import Playlist and select your new file.

**Commit:** Right-click the tracks in the new playlist and select Import to Collection. Your comments will now be updated with the [E: | B: | S:] tags.
<img width="640" height="177" alt="Screenshot 2026-05-05 at 5 34 08 PM" src="https://github.com/user-attachments/assets/3bc7dead-ff22-416d-b08e-06fc0071cf20" />



## 🔒 Security & Data Privacy
**Zero-Cloud Footprint:** All analysis and the Review Dashboard run locally. No track data or metadata is ever uploaded to an external server.

**.gitignore Protection:** The repository is pre-configured to block the uploading of .xml, .json, and .db files.

**Database Safety:** The mandatory backup process ensures your original master.db remains untouched in the /db_backups folder.

Developed by Satyajeet Aparadh (Satyasin)
