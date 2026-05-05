import os
import xml.etree.ElementTree as ET
import librosa
import numpy as np
import webbrowser
import urllib.parse
import json
import argparse
import shutil
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- USER CONFIGURATION AREA ---
# EDIT THE PATH BELOW: 
# Reference for macOS: "/Users/YOUR_USERNAME/Library/Pioneer/rekordbox/master.db"
REKORDBOX_DB_PATH = "REPLACE_WITH_YOUR_MASTER_DB_PATH"

# Internal Folders (No need to edit)
DB_BACKUP_DIR = "db_backups"
OUTPUT_XML_DIR = "vibe_outputs"
PENDING_DATA = [] 

def run_db_backup(custom_db_path=None):
    """Safety backup of the master.db."""
    db_path = custom_db_path or REKORDBOX_DB_PATH
    
    # Check if user has updated the placeholder
    if db_path == "REPLACE_WITH_YOUR_MASTER_DB_PATH":
        print("\n❌ SETUP REQUIRED: Please open 'vibe_batch.py' and set your REKORDBOX_DB_PATH.")
        print("💡 Reference Path (macOS): /Users/YOUR_NAME/Library/Pioneer/rekordbox/master.db\n")
        return False

    if not os.path.exists(db_path):
        print(f"⚠️ Warning: master.db not found at {db_path}. Proceeding without backup.")
        return True
    
    if not os.path.exists(DB_BACKUP_DIR): 
        os.makedirs(DB_BACKUP_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(DB_BACKUP_DIR, f"master_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"🛡️  Database backed up to: {backup_path}")
    return True

def get_vibe(file_path):
    """4-Point Logarithmic Analysis for Energy, Brightness, and Swing."""
    try:
        duration = librosa.get_duration(path=file_path)
        sample_plan = [(0, 0.10), (duration*0.35, 0.20), (duration*0.50, 0.50), (duration*0.75, 0.20)]
        energies, rolloffs = [], []
        for offset, weight in sample_plan:
            y, sr = librosa.load(file_path, offset=offset, duration=15)
            rms = np.mean(librosa.feature.rms(y=y))
            roll = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
            energies.append(rms)
            rolloffs.append(roll * weight)
            
        weighted_e = (energies[0]*0.1 + energies[1]*0.2 + energies[2]*0.5 + energies[3]*0.2)
        log_e = np.log10(weighted_e + 1e-6)
        e_score = np.clip((log_e - (-2.0)) / (-0.3 - (-2.0)), 0.0, 1.0)
        b_score = np.clip((sum(rolloffs) - 2000) / (8000 - 2000), 0.0, 1.0)
        
        log_ens = [np.log10(e + 1e-6) for e in energies]
        norm_ens = [(le - (-2.0)) / (-0.3 - (-2.0)) for le in log_ens]
        swing_cat = "L" if (max(norm_ens)-min(norm_ens)) < 0.15 else "B" if (max(norm_ens)-min(norm_ens)) < 0.35 else "D"
        
        return round(float(e_score), 2), round(float(b_score), 2), f"S:{swing_cat}"
    except: return None

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Vibe Editor</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-200 p-10 font-sans">
    <div class="max-w-5xl mx-auto">
        <header class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-4xl font-black italic tracking-tighter">VIBE <span class="text-blue-500">PRO</span></h1>
                <p class="text-slate-500 font-medium">Reviewing: <span class="text-slate-200">{{ playlist_name }}</span></p>
            </div>
            <button id="save-btn" onclick="saveAll()" class="bg-blue-600 hover:bg-blue-500 px-8 py-3 rounded-xl font-bold transition shadow-lg flex items-center gap-2">
                <span>Confirm & Save All</span>
            </button>
        </header>
        <div class="bg-slate-900 rounded-2xl overflow-hidden shadow-2xl border border-slate-800">
            <table class="w-full text-left">
                <thead class="bg-slate-800 text-slate-400 uppercase text-xs tracking-widest">
                    <tr>
                        <th class="p-4">Action</th><th class="p-4">Track Details</th>
                        <th class="p-4 text-center">Energy</th><th class="p-4 text-center">Brightness</th><th class="p-4">Swing</th>
                    </tr>
                </thead>
                <tbody id="editor-body">
                    {% for t in tracks %}
                    <tr class="border-b border-slate-800 track-row hover:bg-slate-800/30 transition" data-id="{{ t.id }}" data-swing="{{ t.swing }}">
                        <td class="p-4">
                            <select class="bg-slate-800 border border-slate-700 rounded-lg p-2 text-sm status-select cursor-pointer outline-none">
                                <option value="accept">✅ Accept</option>
                                <option value="skip">⏭️ Skip</option>
                            </select>
                        </td>
                        <td class="p-4">
                            <div class="font-bold text-slate-100 leading-tight">{{ t.title }}</div>
                            <div class="text-slate-500 text-xs mt-1">{{ t.artist }}</div>
                        </td>
                        <td class="p-4 text-center">
                            <input type="number" step="0.01" min="0" max="1" value="{{ t.energy }}" class="bg-slate-950 border border-slate-700 rounded-lg p-2 w-24 text-center text-yellow-500 energy-input">
                        </td>
                        <td class="p-4 text-center">
                            <input type="number" step="0.01" min="0" max="1" value="{{ t.brightness }}" class="bg-slate-950 border border-slate-700 rounded-lg p-2 w-24 text-center text-cyan-400 bright-input">
                        </td>
                        <td class="p-4 font-mono text-blue-400 font-bold">{{ t.swing }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <script>
        function saveAll() {
            if(!confirm("Once saved, these choices are final. Proceed?")) return;
            const results = [];
            document.querySelectorAll('.track-row').forEach(row => {
                results.push({
                    id: row.dataset.id, swing: row.dataset.swing,
                    status: row.querySelector('.status-select').value,
                    energy: row.querySelector('.energy-input').value,
                    brightness: row.querySelector('.bright-input').value
                });
            });
            fetch('/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(results)
            }).then(() => {
                document.querySelectorAll('input, select').forEach(el => el.disabled = true);
                const btn = document.getElementById('save-btn');
                btn.disabled = true; btn.innerHTML = "🔒 Changes Locked & Saved";
                alert("Review Saved! Press Ctrl+C in terminal to stop.");
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_UI, tracks=PENDING_DATA, playlist_name=getattr(app, 'playlist_name', 'Playlist'))

@app.route('/save', methods=['POST'])
def save():
    with open('vibe_edits.json', 'w') as f:
        json.dump(request.json, f, indent=4)
    return jsonify({"status": "success"})

def generate_final_xml(input_xml):
    if not os.path.exists('vibe_edits.json'):
        print("❌ Error: No saved edits found. Run analysis first.")
        return
    if not os.path.exists(OUTPUT_XML_DIR):
        os.makedirs(OUTPUT_XML_DIR)
    with open('vibe_edits.json', 'r') as f:
        edits = json.load(f)
    accepted_map = {item['id']: item for item in edits if item['status'] == 'accept'}
    if not accepted_map:
        print("⚠️ No tracks were accepted. XML not created.")
        return

    tree = ET.parse(input_xml)
    root = tree.getroot()
    new_root = ET.Element("DJ_PLAYLISTS", Version="1.0.0")
    new_collection = ET.SubElement(new_root, "COLLECTION", Count=str(len(accepted_map)))
    
    found_count = 0
    for track in root.find('COLLECTION').findall('TRACK'):
        t_id = track.get('TrackID')
        if t_id in accepted_map:
            edit = accepted_map[t_id]
            new_comment = f"E:{float(edit['energy']):.2f} B:{float(edit['brightness']):.2f} {edit['swing']}"
            track.set('Comments', new_comment)
            new_collection.append(track)
            found_count += 1

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = os.path.join(OUTPUT_XML_DIR, f"vibe_final_{ts}.xml")
    ET.ElementTree(new_root).write(output_path, encoding="UTF-8", xml_declaration=True)
    print(f"✅ SUCCESS: Created {output_path} with {found_count} tracks.")

def main():
    parser = argparse.ArgumentParser(description="DJ Intelligence Pro: Vibe Analyzer")
    parser.add_argument("-p", "--playlist", help="Playlist name to analyze")
    parser.add_argument("-i", "--input", default="collection_export.xml", help="Rekordbox XML export file")
    parser.add_argument("--db", help="Path to master.db (optional override)")
    parser.add_argument("--generate", action="store_true", help="Generate XML from saved edits")
    args = parser.parse_args()

    if args.generate:
        generate_final_xml(args.input)
        return

    if not args.playlist:
        print("Usage: uv run vibe_batch.py -p 'Playlist Name'")
        return

    # Check setup before running
    if not run_db_backup(args.db):
        return

    if not os.path.exists(args.input):
        print(f"❌ Error: {args.input} not found.")
        return

    tree = ET.parse(args.input)
    root = tree.getroot()
    track_map = {t.get('TrackID'): t for t in root.find('COLLECTION').findall('TRACK')}
    
    for pl in root.findall('.//NODE[@Type="1"]'):
        if pl.get('Name') == args.playlist:
            app.playlist_name = args.playlist
            for entry in pl.findall('TRACK'):
                track = track_map.get(entry.get('Key'))
                if track:
                    loc = track.get('Location')
                    path = urllib.parse.unquote(loc.replace('file://localhost', ''))
                    res = get_vibe(path)
                    if res:
                        e, b, s = res
                        PENDING_DATA.append({
                            "id": track.get('TrackID'), "title": track.get('Name'),
                            "artist": track.get('Artist'), "energy": e, 
                            "brightness": b, "swing": s
                        })
            break

    if not PENDING_DATA:
        print(f"❌ No tracks found in playlist '{args.playlist}'.")
        return

    print(f"🚀 Launching Editor for {len(PENDING_DATA)} tracks...")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(port=5000, debug=False)

if __name__ == "__main__":
    main()