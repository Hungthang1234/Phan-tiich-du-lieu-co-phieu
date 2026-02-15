# encoding_fix.py - Fix UTF-8 encoding cho Windows
import sys
import os

def fix_encoding():
    """Fix encoding cho Windows console"""
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')
        import io
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
