#!/usr/bin/env python3
# ============================================================
#   WOE AUTO IP - Termux IP Rotator
# ============================================================

import os, sys, time, signal, random, subprocess, threading
from datetime import datetime

# ─────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────
class C:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    CYAN    = '\033[96m'
    GRAY    = '\033[90m'
    BOLD    = '\033[1m'
    RESET   = '\033[0m'

def red(t):    return f"{C.RED}{t}{C.RESET}"
def green(t):  return f"{C.GREEN}{t}{C.RESET}"
def yellow(t): return f"{C.YELLOW}{t}{C.RESET}"
def cyan(t):   return f"{C.CYAN}{t}{C.RESET}"
def gray(t):   return f"{C.GRAY}{t}{C.RESET}"
def bold(t):   return f"{C.BOLD}{t}{C.RESET}"

# ─────────────────────────────────────────
#  BANNER  <- ضع رسمتك هنا داخل r"""..."""
# ─────────────────────────────────────────
BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⠾⠛⠛⠉⠉⠉⠉⠉⠙⠛⠳⢶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠈⠙⠷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠁⠀⠀⣠⣶⣿⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡏⠀⠀⢠⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣷⡄⠀⠀⠀⠀ ⠀⠀⠀⠀⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠐⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣼⣿⣄⡀⠀⠀⠈⠻⠿⠟⠋⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⣵⣌⠉⠻⢷⣄⡀⠀⠀⠀⠀⣴⣦⣄⣀⣀⣤⣀⠀⠉⠙⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⡶⠶⢶⣤⣄⡀⠀⣀⣤⡶⠾⠛⠛⣿⠟⢸⠇⠙⢷⡄⠀⠙⠻⣦⡀⠀⠀⠙⠻⢿⣿⣿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠶⣄⠀⠀⢉⣽⠿⠋⠁⠀⠀⠀⠐⠟⠀⠿⠀⠀⠀⠹⣦⠀⠀⠙⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠀⠈⠻⣶⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⡀⠀⠀⢻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⡇⢀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⣧⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣻⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡶⠶⠾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣀⠀⠀⠀⠀⠸⠏⠁⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢀⣾⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣀⣠⣿⣤⡄⠀⢰⣾⣷⡄⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⢀⣠⣤⣤⣤⣤⣿⠃⠀⠀⠀⣠⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⠉⢉⣿⣧⡄⠀⠸⠿⡿⠃⠀⢠⣤⡄⠀⠀⠀⠙⠋⠀⠀⠀⠀⠈⠉⠀⠀⠀⣰⣟⣠⣤⡶⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠐⠾⠛⢙⣿⣴⠆⠀⠀⠀⠀⣶⣌⣿⣧⣴⡿⠀⠀⠀⠀⠀⠀⠀⠀⢶⣶⣶⠶⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⠟⠙⢷⣄⡀⠀⠀⠀⠈⠉⠁⠈⠁⠀⠀⠀⠀⠀⠀⠀⢠⣾⠏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣟⠻⢶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠾⠋⠁⠀⠀⠀⠀ ⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠉⠙⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⠶⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⠀⢠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠶⠶⣶⣤⣶⣶⠶⠶⢿⣟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡄⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣴⠾⠟⠛⠻⠷⣦⣄⡀⠀⠀⢀⣼⢿⡇⠀⠀⠀⠀⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⣰⡿⠋⠁⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⠀
⣿⠁⠀⠀⠀⠀⠀⠀⠙⠻⣦⡀⣼⠇⠈⣿⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀
⢿⣆⣀⣀⣀⡀⠀⠀⠀⠀⠈⢻⣿⡀⠀⢻⡆⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⠀⠀
⠀⠉⠛⠛⠛⠛⢷⣤⡀⠀⠀⠀⢻⣇⠀⢸⣷⠀⠀⠀⠀⢸⡷⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢷⣄⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠻⣦⡄⣿⡆⠀⠀⠀⢸⣿⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠀⠀⠀⠀⠀⢀⣀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣹⣿⠆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠶⢦⣿⣄⣿⠀⠀⠀⢠⣾⠃⠀⠀⠀⣠⣿⡁⠀⠀⠀⠀⠀⠀⢀⣤⡾⠛⠳⠶⠶⠶⠶⠟⠛⠉⠁⠉⠛⢷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⡶⠟⠋⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣦⣤⣤⣼⣷⣀⣀⣠⣴⠟⠉⠙⠛⠿⠿⠿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⠶⣦⣤⣤⡶⠶⠾⠟⠛⠉⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# ─────────────────────────────────────────
#  STATS
# ─────────────────────────────────────────
stats = {
    "rotations":  0,
    "errors":     0,
    "start_time": None,
    "current_ip": "Unknown",
    "old_ip":     "Unknown",
    "mode":       "",
}
running = False

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def clear(): os.system('clear')

def now(): return gray(f"[{datetime.now().strftime('%H:%M:%S')}]")

def log_ok(m):   print(f"{now()} {green('[+]')} {green(m)}")
def log_err(m):  print(f"{now()} {red('[x]')} {red(m)}")
def log_warn(m): print(f"{now()} {yellow('[!]')} {yellow(m)}")
def log_info(m): print(f"{now()} {cyan('[*]')} {m}")

def log_change(old, new):
    print(f"{now()} {green('[IP]')} {gray(old)} {cyan('->>')} {green(bold(new))}")

def hr(ch='--', col=C.GRAY):
    try:
        w = min(os.get_terminal_size().columns, 60)
    except Exception:
        w = 55
    print(f"{col}{'-'*w}{C.RESET}")

def progress_bar(total_seconds):
    """Show a live progress bar that fills up over total_seconds"""
    bar_width = 20
    start = time.monotonic()
    while running:
        elapsed_s = time.monotonic() - start
        if elapsed_s >= total_seconds:
            break
        remaining = total_seconds - elapsed_s
        filled = int((elapsed_s / total_seconds) * bar_width)
        empty  = bar_width - filled
        bar    = green(chr(9608) * filled) + gray(chr(9617) * empty)
        print("\r  [" + bar + "] " + yellow(str(int(remaining)) + "s") + "   ", end='', flush=True)
        time.sleep(0.2)
    # Clear the line cleanly
    print("\r  [" + green(chr(9608) * bar_width) + "] " + green("done") + "   ")

def elapsed():
    if not stats["start_time"]: return "00:00:00"
    s = int(time.time() - stats["start_time"])
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def show_banner():
    clear()
    print(red(BANNER))
    print(f"{C.RED}{C.BOLD}{'  W O E  A U T O  I P  '.center(58)}{C.RESET}")
    print(f"{C.GRAY}{'[ tor ip rotator ]'.center(58)}{C.RESET}")
    hr()
    print()

def show_status():
    print()
    hr()
    print(f"  {cyan('Mode:')} {bold(stats['mode'])}   "
          f"{cyan('Rotations:')} {green(str(stats['rotations']))}   "
          f"{cyan('Errors:')} {red(str(stats['errors']))}   "
          f"{cyan('Uptime:')} {yellow(elapsed())}")
    print(f"  {cyan('Current IP:')} {green(bold(stats['current_ip']))}")
    hr()

# ─────────────────────────────────────────
#  SYSTEM UTILS
# ─────────────────────────────────────────
def run_cmd(c, capture=True):
    try:
        r = subprocess.run(c, shell=True, capture_output=capture, text=True, timeout=20)
        return r.stdout.strip(), r.returncode
    except Exception as e:
        return str(e), 1

def has(name):
    o, c = run_cmd(f"which {name}")
    return c == 0 and bool(o)

def pkg_install(name):
    log_warn(f"Installing {name}...")
    run_cmd(f"pkg install {name} -y", capture=False)
    return has(name)

def ensure_requests():
    try:
        import requests
        return True
    except ImportError:
        log_warn("Installing requests...")
        run_cmd("pip install requests -q")
        try:
            import requests
            return True
        except Exception:
            return False

# ─────────────────────────────────────────
#  IP FETCHING
# ─────────────────────────────────────────
TOR_PROXY = {
    'http':  'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

def get_ip_tor():
    try:
        import requests
        r = requests.get("https://checkip.amazonaws.com",
                         proxies=TOR_PROXY, timeout=10)
        return r.text.strip()
    except Exception:
        pass
    # fallback curl
    out, code = run_cmd("curl -s --socks5-hostname 127.0.0.1:9050 "
                        "https://api.ipify.org --max-time 10")
    return out if (code == 0 and out and len(out) < 20) else None

def get_real_ip():
    for url in ["https://checkip.amazonaws.com",
                "https://api.ipify.org",
                "https://icanhazip.com"]:
        out, code = run_cmd(f"curl -s {url} --max-time 8")
        if code == 0 and out and len(out) < 20:
            return out.strip()
    return None

# ─────────────────────────────────────────
#  TOR
# ─────────────────────────────────────────
def write_torrc():
    candidates = [
        "/data/data/com.termux/files/usr/etc/tor/torrc",
        os.path.expanduser("~/../usr/etc/tor/torrc"),
        "/etc/tor/torrc",
    ]
    torrc = None
    for p in candidates:
        if os.path.exists(p):
            torrc = p
            break
    if not torrc:
        torrc = "/data/data/com.termux/files/usr/etc/tor/torrc"
        os.makedirs(os.path.dirname(torrc), exist_ok=True)
    try:
        try:
            content = open(torrc).read()
        except Exception:
            content = ""
        add = []
        if "ControlPort 9051" not in content:
            add.append("ControlPort 9051")
        if "CookieAuthentication 0" not in content:
            add.append("CookieAuthentication 0")
        if add:
            with open(torrc, 'a') as f:
                f.write("\n" + "\n".join(add) + "\n")
            log_ok(f"torrc updated ({gray(torrc)})")
    except Exception as e:
        log_warn(f"Could not update torrc: {e}")

def start_tor():
    write_torrc()
    log_info("Starting Tor...")
    run_cmd("pkill tor 2>/dev/null")
    time.sleep(2)
    subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log_info("Waiting for Tor to connect...")
    for i in range(40):
        time.sleep(1)
        ip = get_ip_tor_reliable()
        if ip:
            log_ok(f"Tor connected! IP: {green(bold(ip))}")
            return True
        print(f"\r  {yellow('Connecting')} {'.' * (i % 4 + 1)}   ", end='', flush=True)
    print()
    log_err("Tor failed to connect.")
    return False

def reload_tor_ip():
    """Send HUP signal to Tor -> forces new circuit -> new IP"""
    os.system("killall -HUP tor 2>/dev/null || pkill -HUP tor 2>/dev/null")

def get_ip_tor_reliable():
    """Try multiple endpoints for reliability"""
    endpoints = [
        ("requests", "https://checkip.amazonaws.com"),
        ("curl",     "https://api.ipify.org"),
        ("curl",     "https://icanhazip.com"),
        ("curl",     "https://ifconfig.me/ip"),
    ]
    for method, url in endpoints:
        try:
            if method == "requests":
                import requests
                r = requests.get(url, proxies=TOR_PROXY, timeout=8)
                ip = r.text.strip()
            else:
                ip, code = run_cmd(
                    f"curl -s --socks5-hostname 127.0.0.1:9050 {url} --max-time 8"
                )
                if code != 0: continue
            if ip and 7 <= len(ip) <= 15 and ip.count('.') == 3:
                return ip
        except Exception:
            continue
    return None

# ─────────────────────────────────────────
#  MODE 1 & 2 - TOR HUP ROTATION
# ─────────────────────────────────────────
def tor_rotation_loop(interval):
    global running

    if not has("tor"):
        if not pkg_install("tor"):
            log_err("Cannot install tor. Run: pkg install tor")
            return
    if not has("curl"):
        pkg_install("curl")
    ensure_requests()

    if not start_tor():
        return

    stats["current_ip"] = get_ip_tor_reliable() or "Unknown"
    stats["start_time"] = time.time()
    show_banner()

    if interval < 5:
        log_warn(f"Low interval ({interval}s) - IP may not always change")
    log_ok(f"Rotating every {bold(str(interval) + 's')} | HUP method")
    show_status()

    # First HUP immediately so circuit builds during first interval
    reload_tor_ip()

    while running:
        # Countdown display
        # Progress bar countdown
        progress_bar(interval)

        if not running:
            break

        t_start = time.monotonic()
        old_ip  = stats["current_ip"]

        # Fetch with reliable multi-endpoint fallback
        new_ip = get_ip_tor_reliable()

        if new_ip and new_ip != old_ip:
            stats["current_ip"] = new_ip
            stats["old_ip"]     = old_ip
            stats["rotations"] += 1
            log_change(old_ip, new_ip)

        elif new_ip == old_ip:
            # IP unchanged -> HUP again immediately and retry once
            log_warn(f"IP unchanged ({yellow(new_ip)}) - retrying...")
            reload_tor_ip()
            time.sleep(3)
            retry = get_ip_tor_reliable()
            if retry and retry != old_ip:
                stats["current_ip"] = retry
                stats["old_ip"]     = old_ip
                stats["rotations"] += 1
                log_change(old_ip, retry)
            else:
                log_warn("Still unchanged - Tor reused circuit")

        else:
            stats["errors"] += 1
            log_err("Could not fetch IP from any endpoint")

        fetch_took = time.monotonic() - t_start

        # Next HUP now so circuit builds during countdown
        reload_tor_ip()

        # Subtract fetch time from next interval for precision
        adjusted = max(1, interval - int(fetch_took))
        log_info(f"Fetch: {gray(f"{fetch_took:.1f}s")} | Next in: {yellow(str(adjusted) + 's')}")
        show_status()

# ─────────────────────────────────────────
#  MODE 3 - PROXY ROTATION
# ─────────────────────────────────────────
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
]

def fetch_proxies():
    ensure_requests()
    import requests
    log_info("Fetching fresh proxy list...")
    proxies = set()
    for url in PROXY_SOURCES:
        try:
            r = requests.get(url, timeout=10)
            for line in r.text.strip().split('\n'):
                line = line.strip()
                if ':' in line and len(line) < 25:
                    proxies.add(line)
        except Exception:
            pass
    log_ok(f"Fetched {green(bold(str(len(proxies))))} proxies")
    return list(proxies)

def test_proxy(proxy, timeout=4):
    try:
        import requests
        px = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        r = requests.get("https://api.ipify.org", proxies=px, timeout=timeout)
        if r.status_code == 200:
            return r.text.strip()
    except Exception:
        pass
    return None

def find_working_proxies(plist, count=15):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    working = []
    log_info(f"Testing proxies in parallel (need {count})...")
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(test_proxy, p, 4): p for p in plist[:250]}
        for f in as_completed(futures):
            ip = f.result()
            if ip:
                working.append((futures[f], ip))
                print(f"\r  {green('Found:')} {len(working)}/{count}   ",
                      end='', flush=True)
                if len(working) >= count:
                    break
    print()
    return working

def proxy_rotation_loop(interval):
    global running
    ensure_requests()

    plist = fetch_proxies()
    if not plist:
        log_err("No proxies fetched.")
        return

    random.shuffle(plist)
    working = find_working_proxies(plist, count=15)
    if not working:
        log_err("No working proxies found.")
        return

    log_ok(f"Got {len(working)} working proxies!")
    random.shuffle(working)
    stats["start_time"] = time.time()
    show_banner()
    log_ok(f"Rotating every {bold(str(interval) + 's')}")
    show_status()

    idx = 0
    while running:
        if idx >= len(working):
            log_warn("Pool exhausted - refreshing...")
            plist = fetch_proxies()
            random.shuffle(plist)
            working = find_working_proxies(plist, count=15)
            idx = 0
            if not working:
                log_err("No proxies. Retrying in 15s...")
                time.sleep(15)
                continue

        proxy, ip = working[idx]
        idx += 1
        old = stats["current_ip"]
        stats["current_ip"] = ip
        stats["rotations"] += 1
        log_change(old, ip)
        show_status()
        time.sleep(interval)
        if not running:
            break

# ─────────────────────────────────────────
#  MODE 4 - TORSOCKS GUIDE
# ─────────────────────────────────────────
def torsocks_menu():
    show_banner()
    print(f"  {cyan(bold('TORSOCKS - Route your tools through Tor'))}")
    print()
    print(f"  {gray('Lets your tools actually use the Tor IP.')}")
    print()
    hr()
    print(f"  {yellow('USAGE:')}")
    print()
    print(f"    {green('torsocks python3 yourtool.py')}")
    print(f"    {green('torsocks bash yourtool.sh')}")
    print(f"    {green('torsocks ./yourtool')}")
    print()
    hr()
    print(f"  {yellow('STEPS:')}")
    print()
    print(f"  {cyan('1.')} Run this tool (Option 1 or 2) -> starts Tor + rotates IP")
    print(f"  {cyan('2.')} Open a NEW Termux window")
    print(f"  {cyan('3.')} Run: {green('torsocks python3 yourtool.py')}")
    print(f"  {cyan('4.')} Done - your tool uses the rotating Tor IP")
    print()
    hr()

    if not has("torsocks"):
        log_warn("torsocks not installed - installing...")
        if pkg_install("torsocks"):
            log_ok("torsocks installed!")
        else:
            log_err("Failed. Run: pkg install torsocks")
    else:
        log_ok("torsocks is already installed")

    print()
    log_info("Testing torsocks (Tor must be running first)...")
    out, code = run_cmd("torsocks curl -s https://api.ipify.org --max-time 12")
    if code == 0 and out and len(out.strip()) < 20:
        real = get_real_ip()
        log_ok(f"torsocks IP: {green(bold(out.strip()))}")
        if real and real != out.strip():
            log_ok(f"Real IP {red(real)} is hidden!")
        else:
            log_warn("Same IP - start Tor first (Option 1 or 2) then test again.")
    else:
        log_warn("Test failed - start Tor first via Option 1 or 2.")

    print()
    input(gray("  Press Enter to go back..."))

# ─────────────────────────────────────────
#  SHOW REAL IP
# ─────────────────────────────────────────
def show_real_ip():
    log_info("Fetching your real IP...")
    ip = get_real_ip()
    if ip:
        print()
        hr()
        print(f"  {yellow('Your real IP:')} {bold(red(ip))}")
        hr()
        print()
    else:
        log_warn("Could not fetch IP (no internet?)")

# ─────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────
def get_interval(default=10, minimum=1):
    try:
        val = input(f"  {cyan('->')} Interval in seconds [{default}]: ").strip()
        if val == "":
            return default
        val = int(val)
        if val < 1:
            val = 1
        if val < 5:
            log_warn(f"Low interval ({val}s) - IP may not always change. 10s recommended.")
        return val
    except Exception:
        return default

def show_menu():
    show_banner()
    show_real_ip()
    print(f"  {cyan(bold('SELECT MODE'))}")
    print()
    print(f"  {green('[1]')} Tor Rotation     {gray('-')} every 10s    {gray('| stable')}")
    print(f"  {green('[2]')} Tor Custom        {gray('-')} your interval {gray('| flexible')}")
    print(f"  {green('[3]')} Proxy Rotation    {gray('-')} every Xs     {gray('| thousands of IPs')}")
    print(f"  {yellow('[4]')} torsocks Setup    {gray('-')} {yellow('route tools through Tor')}")
    print(f"  {cyan('[5]')} Show Real IP")
    print(f"  {red('[0]')} Exit")
    print()
    hr()
    return input(f"  {cyan('->')} Choose: ").strip()

# ─────────────────────────────────────────
#  SIGNAL HANDLER
# ─────────────────────────────────────────
def handle_exit(sig, frame):
    global running
    running = False
    print()
    log_warn("Stopping...")
    run_cmd("pkill tor 2>/dev/null")
    time.sleep(1)
    print()
    print(f"  {cyan('Rotations:')} {green(str(stats['rotations']))}")
    print(f"  {cyan('Errors:')}    {red(str(stats['errors']))}")
    print(f"  {cyan('Uptime:')}    {yellow(elapsed())}")
    print()
    log_ok("Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    global running
    while True:
        choice = show_menu()

        if choice == '0':
            log_ok("Goodbye!")
            sys.exit(0)

        elif choice == '1':
            stats["mode"] = "Tor 10s"
            running = True
            tor_rotation_loop(10)

        elif choice == '2':
            interval = get_interval(default=10, minimum=2)
            stats["mode"] = f"Tor {interval}s"
            running = True
            tor_rotation_loop(interval)

        elif choice == '3':
            interval = get_interval(default=5, minimum=2)
            stats["mode"] = "Proxy Rotation"
            running = True
            proxy_rotation_loop(interval)

        elif choice == '4':
            torsocks_menu()

        elif choice == '5':
            show_banner()
            show_real_ip()
            input(gray("  Press Enter to go back..."))

        else:
            log_err("Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()
