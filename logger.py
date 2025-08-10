#!/usr/bin/env python3
"""
Logging utility for Spilled Mushrooms game
Captures print output and saves to timestamped log files
"""

import sys
import os
from datetime import datetime
from contextlib import contextmanager


class TeeOutput:
    """Redirect output to both console and file"""
    def __init__(self, file):
        self.file = file
        self.terminal = sys.stdout

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
        self.file.flush()

    def flush(self):
        self.terminal.flush()
        self.file.flush()


@contextmanager
def logged_output(filename=None):
    """Context manager to capture print output to both console and log file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_run_{timestamp}.txt"
        log_path = os.path.join("logs", filename)
    else:
        # If a full path is provided, use it directly
        log_path = filename
    
    # Ensure the directory exists
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    else:
        os.makedirs("logs", exist_ok=True)
    
    with open(log_path, 'w', encoding='utf-8') as log_file:
        # Write header to log file
        log_file.write(f"Spilled Mushrooms Game Log\n")
        log_file.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=" * 60 + "\n\n")
        
        # Redirect stdout
        original_stdout = sys.stdout
        sys.stdout = TeeOutput(log_file)
        
        try:
            yield log_path
        finally:
            # Write footer to log file
            sys.stdout = original_stdout
            log_file.write(f"\n\n" + "=" * 60 + "\n")
            log_file.write(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")