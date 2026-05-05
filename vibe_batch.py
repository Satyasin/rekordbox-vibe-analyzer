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
    # Use the custom path from CLI, then the hardcoded config, then check if it's still the placeholder
    db_path = custom_db_path or REKORDBOX_DB_PATH
    
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

# ... [Rest of the script logic from v5.5 remains the same] ...

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

    # ... [Rest of the XML parsing logic] ...