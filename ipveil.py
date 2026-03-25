#!/usr/bin/env python3
# ============================================================
#   WOE AUTO IP  —  Termux IP Rotator
#   Designed exclusively for Termux on Android
# ============================================================

import os, sys, time, signal, random, subprocess
from datetime import datetime

# ─────────────────────────────────────────
#  TERMUX ENVIRONMENT DETECTION
# ─────────────────────────────────────────
TERMUX_PREFIX  = "/data/data/com.termux/files/usr"
TERMUX_HOME    = "/data/data/com.termux/files/home"
IS_TERMUX      = os.path.isdir(TERMUX_PREFIX)

# Paths to search for binaries — Termux first
_BIN_DIRS = [
    f"{TERMUX_PREFIX}/bin",
    f"{TERMUX_PREFIX}/sbin",
    "/usr/local/bin", "/usr/bin", "/usr/sbin", "/bin", "/sbin",
]

# Subprocess environment with enriched PATH so all tools are found
_ENV = os.environ.copy()
_ENV["PATH"] = ":".join(_BIN_DIRS) + ":" + _ENV.get("PATH", "")

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
#  BANNER
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
running          = False
_anonsurf_active = False

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

def hr(col=C.GRAY):
    try:
        w = min(os.get_terminal_size().columns, 60)
    except Exception:
        w = 55
    print(f"{col}{'-'*w}{C.RESET}")

def progress_bar(total_seconds):
    bar_width = 20
    start = time.monotonic()
    while running:
        elapsed_s = time.monotonic() - start
        if elapsed_s >= total_seconds:
            break
        remaining  = total_seconds - elapsed_s
        filled     = int((elapsed_s / total_seconds) * bar_width)
        empty      = bar_width - filled
        bar        = green(chr(9608) * filled) + gray(chr(9617) * empty)
        print("\r  [" + bar + "] " + yellow(f"{remaining:.0f}s") + "   ", end='', flush=True)
        time.sleep(0.2)
    print("\r  [" + green(chr(9608) * bar_width) + "] " + green("done") + "   ")

def elapsed():
    if not stats["start_time"]: return "00:00:00"
    s = int(time.time() - stats["start_time"])
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def is_valid_ipv4(ip):
    if not ip:
        return False
    parts = ip.strip().split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False

def show_banner():
    clear()
    print(red(BANNER))
    print(f"{C.RED}{C.BOLD}{'  W O E  A U T O  I P  '.center(58)}{C.RESET}")
    print(f"{C.GRAY}{'[ tor ip rotator — termux ]'.center(58)}{C.RESET}")
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

def reset_stats():
    stats.update({
        "rotations":  0,
        "errors":     0,
        "start_time": None,
        "current_ip": "Unknown",
        "old_ip":     "Unknown",
        "mode":       "",
    })

# ─────────────────────────────────────────
#  SYSTEM UTILS
# ─────────────────────────────────────────
def run_cmd(c, capture=True, timeout=20):
    """Run a shell command. Always uses the enriched PATH env."""
    try:
        if capture:
            r = subprocess.run(
                c, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, timeout=timeout, env=_ENV,
            )
            return r.stdout.strip(), r.returncode
        else:
            r = subprocess.run(c, shell=True, timeout=timeout, env=_ENV)
            return "", r.returncode
    except subprocess.TimeoutExpired:
        return "timeout", 1
    except Exception as e:
        return str(e), 1

def find_binary(name):
    """Return full path of a binary, checking Termux paths first."""
    for d in _BIN_DIRS:
        p = os.path.join(d, name)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    # Shell lookup as fallback
    o, c = run_cmd(f"command -v {name} 2>/dev/null")
    if c == 0 and o.strip():
        return o.strip()
    return name

def has(name):
    """Check if a binary is available — robust for Termux."""
    for d in _BIN_DIRS:
        if os.path.isfile(os.path.join(d, name)):
            return True
    o, c = run_cmd(f"command -v {name} 2>/dev/null")
    return c == 0 and bool(o.strip())

def pkg_install(name):
    """Install a package using the available package manager."""
    log_warn(f"Installing {name}...")
    # Determine available package manager
    if has("pkg"):
        mgr = f"pkg install {name} -y"
    elif has("apt-get"):
        mgr = f"apt-get install -y {name}"
    else:
        log_err("No package manager found (pkg / apt-get)")
        return False
    run_cmd(mgr, capture=False, timeout=120)
    # Give it a moment then verify
    time.sleep(1)
    return has(name)

def check_root():
    out, code = run_cmd("id -u")
    return code == 0 and out.strip() == "0"

def ensure_requests():
    try:
        import requests  # noqa: F401
        return True
    except ImportError:
        log_warn("Installing requests library...")
        # Prefer pip3, fallback to pip
        pip = "pip3" if has("pip3") else "pip"
        run_cmd(f"{pip} install requests -q", capture=False, timeout=120)
        try:
            import requests  # noqa: F401
            return True
        except Exception:
            log_err("Failed to install requests. Run: pip3 install requests")
            return False

# ─────────────────────────────────────────
#  IP FETCHING
# ─────────────────────────────────────────
TOR_PROXY = {
    'http':  'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

def get_ip_tor_reliable():
    """Try multiple endpoints through Tor, validate IPv4."""
    curl = find_binary("curl")
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
                if r.status_code != 200:
                    continue
                ip = r.text.strip()
            else:
                ip, code = run_cmd(
                    f"{curl} -s --socks5-hostname 127.0.0.1:9050 {url} --max-time 8"
                )
                if code != 0:
                    continue
            if is_valid_ipv4(ip):
                return ip
        except Exception:
            continue
    return None

def get_real_ip():
    """Fetch real (non-Tor) IP address."""
    curl = find_binary("curl")
    for url in ["https://checkip.amazonaws.com",
                "https://api.ipify.org",
                "https://icanhazip.com"]:
        out, code = run_cmd(f"{curl} -s {url} --max-time 8")
        if code == 0 and is_valid_ipv4(out):
            return out.strip()
    return None

# ─────────────────────────────────────────
#  TORRC
# ─────────────────────────────────────────
TORRC_CANDIDATES = [
    f"{TERMUX_PREFIX}/etc/tor/torrc",
    os.path.expanduser("~/../usr/etc/tor/torrc"),
    "/etc/tor/torrc",
]
DEFAULT_TORRC = f"{TERMUX_PREFIX}/etc/tor/torrc"

def find_torrc():
    for p in TORRC_CANDIDATES:
        if os.path.exists(p):
            return p
    return DEFAULT_TORRC

def update_torrc(extra_settings):
    """
    Append missing directives to torrc.
    Ignores commented-out lines when checking what's already set.
    """
    torrc = find_torrc()
    os.makedirs(os.path.dirname(torrc), exist_ok=True)
    try:
        try:
            content = open(torrc).read()
        except Exception:
            content = ""
        active_keys = set()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                active_keys.add(stripped.split()[0].lower())
        additions = [s for s in extra_settings
                     if s.split()[0].lower() not in active_keys]
        if additions:
            with open(torrc, 'a') as f:
                f.write("\n" + "\n".join(additions) + "\n")
            log_ok(f"torrc updated ({gray(torrc)})")
    except Exception as e:
        log_warn(f"Could not update torrc: {e}")

def write_torrc():
    update_torrc(["ControlPort 9051", "CookieAuthentication 0"])

# ─────────────────────────────────────────
#  TOR CONTROL
# ─────────────────────────────────────────
TRANS_PORT = 9040
DNS_PORT   = 5353

def reload_tor_ip():
    """Send HUP to Tor to force a new circuit."""
    run_cmd("killall -HUP tor 2>/dev/null || pkill -HUP tor 2>/dev/null")

def start_tor():
    torrc_path = find_torrc()
    write_torrc()
    log_info(f"torrc: {gray(torrc_path)}")
    log_info("Starting Tor...")
    run_cmd("pkill tor 2>/dev/null || killall tor 2>/dev/null")
    time.sleep(2)
    tor_bin = find_binary("tor")
    log_info(f"tor binary: {gray(tor_bin)}")

    import tempfile
    err_file = tempfile.mktemp(prefix="tor_err_")
    try:
        with open(err_file, 'w') as ef:
            proc = subprocess.Popen(
                [tor_bin],
                stdout=subprocess.DEVNULL,
                stderr=ef,
                env=_ENV,
            )
    except Exception as e:
        log_err(f"Could not launch tor: {e}")
        return False

    log_info("Waiting for Tor to bootstrap (up to 90s on mobile)...")
    for i in range(90):
        time.sleep(1)
        if proc.poll() is not None:
            print()
            log_err("Tor process exited unexpectedly!")
            try:
                err = open(err_file).read().strip()
                if err:
                    print(f"  {red('Tor error:')} {gray(err[-500:])}")
            except Exception:
                pass
            return False
        ip = get_ip_tor_reliable()
        if ip:
            print()
            log_ok(f"Tor connected! IP: {green(bold(ip))}")
            try: os.remove(err_file)
            except Exception: pass
            return True
        print(f"\r  {yellow('Bootstrapping')} {'.' * (i % 4 + 1)}  [{i+1}s]   ", end='', flush=True)
    print()
    log_err("Tor failed to connect after 90 seconds.")
    try:
        err = open(err_file).read().strip()
        if err:
            print(f"  {red('Tor stderr:')} {gray(err[-500:])}")
    except Exception:
        pass
    return False

def get_tor_uid():
    """Get the UID that tor runs as (to exclude from iptables rules)."""
    for candidate in ["tor", "_tor", "debian-tor"]:
        out, code = run_cmd(f"id -u {candidate} 2>/dev/null")
        if code == 0 and out.strip().isdigit():
            return out.strip()
    return None

# ─────────────────────────────────────────
#  ANONSURF (transparent proxy via iptables)
# ─────────────────────────────────────────
def write_anonsurf_torrc():
    update_torrc([
        f"TransPort {TRANS_PORT}",
        f"DNSPort {DNS_PORT}",
        "AutomapHostsOnResolve 1",
        "VirtualAddrNetworkIPv4 10.192.0.0/10",
    ])

# Android system iptables binary — must use this, not Termux's
IPTABLES = "/system/bin/iptables"

def _ipt(rule):
    """
    Run a single iptables rule using /system/bin/iptables.
    -w = wait for xtables lock (critical on Android — netd holds it).
    Always runs as current process (must already be root).
    Returns True on success.
    """
    out, code = run_cmd(f"{IPTABLES} -w {rule} 2>&1")
    if code != 0:
        log_warn(f"iptables rule failed: {gray(rule)}")
        if out:
            log_warn(f"  reason: {gray(out)}")
    return code == 0

def iptables_anonsurf_start(tor_uid):
    """
    Transparent proxy — individual UID exclusions (confirmed working on this device).

    Strategy:
    - Exclude system UIDs one by one (range syntax not supported)
    - Exclude Tor UID to prevent traffic loop
    - Redirect everything else through Tor TransPort

    System UIDs identified from /proc/net/xt_qtaguid/stats and ps output:
    0=root/kernel, 1000=system, 1001=radio, 1010=wifi,
    1020,1021,1051,1073=other system services
    """
    # All system UIDs that must NEVER be redirected
    # Detected from this device's xt_qtaguid/stats + ps output
    SYSTEM_UIDS = [
        "0",     # root, kernel, netd, Tor itself
        "1000",  # Android system
        "1001",  # radio — rild, com.android.phone
        "1010",  # wifi — wificond, wpa_supplicant, hostapd
        "1020",  # GPS / location
        "1021",  # GPS
        "1051",  # nfc / other hw
        "1073",  # system service
        "2904",  # system service
        "5025",  # system service
    ]

    # Add Tor UID if different from 0 (usually same on Termux root)
    if tor_uid not in SYSTEM_UIDS:
        SYSTEM_UIDS.append(tor_uid)

    # Clean slate
    run_cmd(f"{IPTABLES} -w -t nat -F OUTPUT 2>/dev/null")

    # 1. Loopback — never redirect
    _ipt("-t nat -A OUTPUT -o lo -j RETURN")

    # 2. Exclude each system UID individually (RETURN = pass through untouched)
    log_info("Excluding system UIDs...")
    for uid in SYSTEM_UIDS:
        ok = _ipt(f"-t nat -A OUTPUT -m owner --uid-owner {uid} -j RETURN")
        status = green("OK") if ok else yellow("skipped")
        log_info(f"  UID {uid:>5} → {status}")

    # 3. Redirect DNS (UDP 53) for everything else → Tor DNS port
    _ipt(
        f"-t nat -A OUTPUT "
        f"-p udp --dport 53 "
        f"-j REDIRECT --to-ports {DNS_PORT}"
    )

    # 4. MAIN RULE: redirect all TCP for everything else → Tor TransPort
    ok = _ipt(
        f"-t nat -A OUTPUT "
        f"! -d 127.0.0.1 "
        f"-p tcp "
        f"-j REDIRECT --to-ports {TRANS_PORT}"
    )

    return ok

def iptables_anonsurf_stop():
    """Flush NAT OUTPUT — restores normal routing. Must be called as root."""
    run_cmd("chattr -i /etc/resolv.conf 2>/dev/null")
    _, code = run_cmd(f"{IPTABLES} -w -t nat -F OUTPUT 2>&1")
    return code == 0

# ─────────────────────────────────────────
#  MODE 1 & 2 — TOR HUP ROTATION
# ─────────────────────────────────────────
def tor_rotation_loop(interval, anonsurf=False):
    global running, _anonsurf_active

    if not has("tor"):
        if not pkg_install("tor"):
            log_err("Cannot install tor. Run: pkg install tor")
            return
    if not has("curl"):
        if not pkg_install("curl"):
            log_err("Cannot install curl. Run: pkg install curl")
            return
    if not ensure_requests():
        return

    if anonsurf:
        write_anonsurf_torrc()

    if not start_tor():
        return

    # Apply AnonSurf iptables rules if requested
    if anonsurf:
        _, ipt_ok = run_cmd("iptables -L -n 2>/dev/null" if check_root()
                            else "su -c 'iptables -L -n'")
        if ipt_ok != 0:
            log_warn("iptables not available — running as plain Tor rotation")
            anonsurf = False
        else:
            tor_uid = get_tor_uid()
            if not tor_uid:
                # In Termux running as root, tor may run as current user
                tor_uid_out, _ = run_cmd("id -u")
                tor_uid = tor_uid_out.strip() or "tor"
            log_info(f"Tor UID: {cyan(tor_uid)}")
            log_info("Applying iptables transparent proxy rules...")
            if iptables_anonsurf_start(tor_uid):
                _anonsurf_active = True
                log_ok("AnonSurf active — ALL traffic routed through Tor!")
            else:
                log_warn("Some iptables rules failed — partial routing may work")
                _anonsurf_active = True

    stats["current_ip"] = get_ip_tor_reliable() or "Unknown"
    stats["start_time"] = time.time()
    show_banner()

    if anonsurf:
        real_ip = get_real_ip()
        print()
        hr(C.RED)
        print(f"  {red(bold('ANONSURF ACTIVE'))} — All device traffic routes through Tor")
        print(f"  {cyan('Tor IP:')}  {green(bold(stats['current_ip']))}")
        if real_ip and real_ip != stats["current_ip"]:
            print(f"  {cyan('Real IP:')} {red(real_ip)} {gray('(hidden)')}")
        hr(C.RED)
        print()

    if interval < 5:
        log_warn(f"Low interval ({interval}s) - IP may not always change")
    log_ok(f"Rotating every {bold(str(interval) + 's')} | HUP method")
    show_status()

    reload_tor_ip()   # First HUP so new circuit builds during countdown

    next_interval = interval
    while running:
        progress_bar(next_interval)
        if not running:
            break

        t_start = time.monotonic()
        old_ip  = stats["current_ip"]
        new_ip  = get_ip_tor_reliable()

        if new_ip and new_ip != old_ip:
            stats["current_ip"] = new_ip
            stats["old_ip"]     = old_ip
            stats["rotations"] += 1
            log_change(old_ip, new_ip)

        elif new_ip == old_ip:
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
                log_warn("Still unchanged — Tor reused circuit")

        else:
            stats["errors"] += 1
            log_err("Could not fetch IP from any endpoint")

        fetch_took    = time.monotonic() - t_start
        next_interval = max(1, interval - int(fetch_took))
        log_info(f"Fetch: {gray(f'{fetch_took:.1f}s')} | Next in: {yellow(str(next_interval) + 's')}")
        reload_tor_ip()   # HUP now so circuit builds during countdown
        show_status()

    # Cleanup AnonSurf on normal loop exit
    if _anonsurf_active:
        log_warn("Flushing AnonSurf iptables rules...")
        if iptables_anonsurf_stop():
            log_ok("iptables flushed — normal routing restored")
        else:
            log_err("Could not flush! Run: iptables -t nat -F OUTPUT")
        _anonsurf_active = False

# ─────────────────────────────────────────
#  MODE 3 — PROXY ROTATION
# ─────────────────────────────────────────

# HTTP proxy sources (updated daily)
_HTTP_PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
]

# SOCKS5 proxy sources
_SOCKS5_PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
]

# Plain HTTP test endpoint — works with HTTP proxies, fast, no HTTPS tunnel needed
_PROXY_TEST_URL = "http://checkip.amazonaws.com"
_PROXY_TEST_URL2 = "http://api.ipify.org"

def _fetch_list(urls, label):
    """Fetch ip:port lines from a list of raw-text URLs."""
    import requests
    found = set()
    for url in urls:
        try:
            r = requests.get(url, timeout=12)
            if r.status_code != 200:
                continue
            for line in r.text.splitlines():
                line = line.strip()
                # Accept only ip:port format (no extra text)
                if ':' in line and 6 < len(line) < 24:
                    parts = line.split(':')
                    if len(parts) == 2 and parts[1].isdigit():
                        found.add(line)
        except Exception:
            pass
    log_info(f"  {label}: {green(str(len(found)))} proxies")
    return found

def fetch_proxies():
    if not ensure_requests():
        return []
    log_info("Fetching proxy lists (HTTP + SOCKS5)...")
    http_proxies  = _fetch_list(_HTTP_PROXY_SOURCES,  "HTTP ")
    socks5_proxies = _fetch_list(_SOCKS5_PROXY_SOURCES, "SOCKS5")
    # Tag type so test_proxy knows which protocol to use
    combined = [("http", p)   for p in http_proxies] + \
               [("socks5", p) for p in socks5_proxies]
    log_ok(f"Total: {green(bold(str(len(combined))))} proxies fetched")
    return combined

def test_proxy(entry, timeout=7):
    """
    Test a (type, ip:port) proxy.
    Uses plain HTTP endpoint — works even for plain HTTP proxies
    that don't support HTTPS CONNECT tunneling.
    Returns (entry, ip) on success, None on failure.
    """
    try:
        import requests
        ptype, proxy = entry
        if ptype == "socks5":
            px = {
                "http":  f"socks5h://{proxy}",
                "https": f"socks5h://{proxy}",
            }
        else:
            px = {
                "http":  f"http://{proxy}",
                "https": f"http://{proxy}",
            }
        for test_url in (_PROXY_TEST_URL, _PROXY_TEST_URL2):
            try:
                r = requests.get(test_url, proxies=px, timeout=timeout)
                if r.status_code == 200:
                    ip = r.text.strip()
                    if is_valid_ipv4(ip):
                        return (entry, ip)
            except Exception:
                continue
    except Exception:
        pass
    return None

def find_working_proxies(plist, count=15):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    working     = []
    futures_map = {}
    log_info(f"Testing {min(len(plist), 400)} proxies (need {count} working)...")
    with ThreadPoolExecutor(max_workers=60) as ex:
        for entry in plist[:400]:
            fut              = ex.submit(test_proxy, entry, 7)
            futures_map[fut] = entry
        for f in as_completed(futures_map):
            result = f.result()
            if result:
                entry, ip = result
                ptype, proxy = entry
                working.append((proxy, ip, ptype))
                print(f"\r  {green('Found:')} {len(working)}/{count}  [{ptype}]  ", end='', flush=True)
                if len(working) >= count:
                    for pending in futures_map:
                        if not pending.done():
                            pending.cancel()
                    break
    print()
    return working

def proxy_rotation_loop(interval):
    global running
    if not ensure_requests():
        return

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
            log_warn("Proxy pool exhausted — refreshing...")
            new_plist = fetch_proxies()
            if new_plist:
                random.shuffle(new_plist)
                new_working = find_working_proxies(new_plist, count=15)
                if new_working:
                    working = new_working
                    idx     = 0
                else:
                    log_err("No working proxies. Retrying in 15s...")
                    time.sleep(15)
                    continue
            else:
                log_err("Could not fetch proxies. Retrying in 15s...")
                time.sleep(15)
                continue

        proxy, ip, ptype = working[idx]
        idx += 1
        old = stats["current_ip"]
        stats["current_ip"] = ip
        stats["rotations"] += 1
        log_change(old, f"{ip} {gray(f'[{ptype}]')}")
        show_status()
        progress_bar(interval)

# ─────────────────────────────────────────
#  MODE 4 — TORSOCKS GUIDE
# ─────────────────────────────────────────
def torsocks_menu():
    show_banner()
    print(f"  {cyan(bold('TORSOCKS — Route your tools through Tor'))}")
    print()
    print(f"  {gray('Lets your tools use the Tor IP directly.')}")
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
    print(f"  {cyan('1.')} Run this tool (Option 1 or 2) — starts Tor + rotates IP")
    print(f"  {cyan('2.')} Open a NEW Termux session")
    print(f"  {cyan('3.')} Run: {green('torsocks python3 yourtool.py')}")
    print(f"  {cyan('4.')} Done — your tool uses the rotating Tor IP")
    print()
    hr()

    if not has("torsocks"):
        log_warn("torsocks not installed — installing...")
        if pkg_install("torsocks"):
            log_ok("torsocks installed!")
        else:
            log_err("Failed. Run: pkg install torsocks")
    else:
        log_ok("torsocks is already installed")

    print()
    log_info("Testing torsocks (Tor must be running first)...")
    curl = find_binary("curl")
    torsocks = find_binary("torsocks")
    out, code = run_cmd(f"{torsocks} {curl} -s https://api.ipify.org --max-time 12")
    if code == 0 and is_valid_ipv4(out.strip()):
        real = get_real_ip()
        log_ok(f"torsocks IP: {green(bold(out.strip()))}")
        if real and real != out.strip():
            log_ok(f"Real IP {red(real)} is hidden!")
        else:
            log_warn("Same IP — start Tor first (Option 1 or 2) then test again.")
    else:
        log_warn("Test failed — start Tor first via Option 1 or 2.")

    print()
    input(gray("  Press Enter to go back..."))

# ─────────────────────────────────────────
#  MODE 5 — SHOW REAL IP
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
#  MODE 6 — ANONSURF (standalone, ROOT required)
# ─────────────────────────────────────────
def anonsurf_start():
    show_banner()
    print(f"  {cyan(bold('ANONSURF MODE — Route ALL traffic through Tor'))}")
    print()
    print(f"  {yellow('Requires: Root access + iptables')}")
    print()
    hr()

def anonsurf_start():
    global running, _anonsurf_active
    show_banner()
    print(f"  {cyan(bold('ANONSURF MODE — Route ALL traffic through Tor'))}")
    print()
    print(f"  {yellow('Requires: root (su) + /system/bin/iptables')}")
    print()
    hr()

    if not check_root():
        py3    = find_binary("python3")
        me     = os.path.abspath(__file__)
        su_cmd = "su -c '" + py3 + " " + me + "'"
        log_err("No root access!")
        print()
        print(f"  {yellow('Run as root:')}")
        print(f"    {green(su_cmd)}")
        print()
        input(gray("  Press Enter to go back..."))
        return

    log_ok("Root access confirmed")

    # Verify /system/bin/iptables exists
    if not os.path.isfile(IPTABLES):
        log_err(f"iptables not found at {IPTABLES}")
        input(gray("  Press Enter to go back..."))
        return
    log_ok(f"iptables found: {gray(IPTABLES)}")

    # Quick kernel test — use ! operator (no range)
    test_uid = "0"
    test_out, test_code = run_cmd(
        f"{IPTABLES} -w -t nat -A OUTPUT -m owner ! --uid-owner {test_uid} "
        f"-p tcp --dport 9999 -j RETURN 2>&1"
    )
    if test_code != 0:
        log_err("iptables owner match not supported on this kernel")
        log_err(f"  {gray(test_out)}")
        input(gray("  Press Enter to go back..."))
        return
    # Remove test rule
    run_cmd(
        f"{IPTABLES} -w -t nat -D OUTPUT -m owner ! --uid-owner {test_uid} "
        f"-p tcp --dport 9999 -j RETURN 2>/dev/null"
    )
    log_ok("Kernel iptables owner match: supported")

    # Safety confirmation
    print()
    hr(C.YELLOW)
    print(f"  {yellow(bold('IMPORTANT — Read before continuing'))}")
    print()
    print(f"  {cyan('What this mode does:')}")
    print(f"    Routes ALL traffic (apps + Termux) through Tor.")
    print(f"    Only Tor itself is excluded to prevent loops.")
    print()
    print(f"  {yellow('Cleanup is automatic on exit — routing always restored.')}")
    hr(C.YELLOW)
    print()
    try:
        confirm = input(f"  {cyan('->')} Type {green('yes')} to continue: ").strip().lower()
    except EOFError:
        confirm = ""
    if confirm != "yes":
        log_warn("Cancelled.")
        return

    # Sub-menu: static or auto-rotate
    print()
    print(f"  {cyan(bold('Choose mode:'))}")
    print(f"  {green('[1]')} Static      {gray('-')} stay on until you press Enter")
    print(f"  {green('[2]')} Auto-rotate {gray('-')} change Tor IP every X seconds")
    print()
    hr()
    try:
        sub = input(f"  {cyan('->')} Choose [1/2]: ").strip()
    except EOFError:
        sub = '1'
    rotate   = (sub == '2')
    interval = 0
    if rotate:
        interval = get_interval(default=30, minimum=10)

    if not has("tor"):
        if not pkg_install("tor"):
            log_err("Cannot install tor. Run: pkg install tor")
            input(gray("  Press Enter to go back..."))
            return

    write_anonsurf_torrc()

    if not start_tor():
        log_err("Tor failed to start")
        input(gray("  Press Enter to go back..."))
        return

    # Get Tor UID — on Termux root, tor runs as UID 0
    tor_uid = get_tor_uid() or "0"
    log_info(f"Tor UID: {cyan(tor_uid)}")

    # Fetch real IP BEFORE applying iptables rules
    log_info("Saving real IP before routing...")
    real_ip = get_real_ip()

    log_info("Applying iptables rules...")
    if iptables_anonsurf_start(tor_uid):
        _anonsurf_active = True
        log_ok("iptables rules applied — all traffic through Tor!")
    else:
        log_warn("Main redirect rule failed — check output above")
        log_warn("Stopping to avoid partial routing...")
        run_cmd("pkill tor 2>/dev/null")
        input(gray("  Press Enter to go back..."))
        return

    tor_ip = get_ip_tor_reliable()
    stats["current_ip"] = tor_ip or "Unknown"
    stats["start_time"] = time.time()
    stats["mode"]       = f"AnonSurf-{'Rotate ' + str(interval) + 's' if rotate else 'Static'}"

    show_banner()
    print()
    hr(C.RED)
    print(f"  {red(bold('ANONSURF ACTIVE'))}")
    print(f"  {cyan('Tor IP:')}   {green(bold(tor_ip or 'unknown'))}")
    if real_ip:
        print(f"  {cyan('Real IP:')}  {red(real_ip)} {gray('(hidden from outside)')}")
    hr(C.RED)
    print()

    if not rotate:
        print(f"  {yellow('All traffic through Tor — press Enter to stop')}")
        input()
    else:
        print(f"  {yellow('Auto-rotating every')} {bold(str(interval) + 's')} {yellow('— Ctrl+C to stop')}")
        print()
        running = True
        show_status()
        reload_tor_ip()

        while running:
            progress_bar(interval)
            if not running:
                break

            old_ip = stats["current_ip"]
            reload_tor_ip()
            time.sleep(3)
            new_ip = get_ip_tor_reliable()

            if new_ip and new_ip != old_ip:
                stats["current_ip"] = new_ip
                stats["old_ip"]     = old_ip
                stats["rotations"] += 1
                log_change(old_ip, new_ip)
            elif new_ip == old_ip:
                log_warn(f"IP unchanged ({yellow(new_ip)}) — retrying...")
                reload_tor_ip()
                time.sleep(4)
                retry = get_ip_tor_reliable()
                if retry and retry != old_ip:
                    stats["current_ip"] = retry
                    stats["old_ip"]     = old_ip
                    stats["rotations"] += 1
                    log_change(old_ip, retry)
                else:
                    log_warn("Still unchanged — Tor reused circuit")
            else:
                stats["errors"] += 1
                log_err("Could not fetch IP")

            reload_tor_ip()
            show_status()

        running = False

    # Cleanup — always runs
    log_warn("Stopping AnonSurf — flushing iptables rules...")
    if iptables_anonsurf_stop():
        log_ok("iptables flushed — normal routing restored")
    else:
        log_err(f"Could not flush! Run manually: {IPTABLES} -w -t nat -F OUTPUT")

    _anonsurf_active = False
    run_cmd("pkill tor 2>/dev/null")
    log_ok("AnonSurf stopped.")
    print()
    input(gray("  Press Enter to go back..."))

# ─────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────
def get_interval(default=10, minimum=1):
    try:
        val = input(f"  {cyan('->')} Interval in seconds [{default}]: ").strip()
        if not val:
            return default
        val = int(val)
        if val < minimum:
            val = minimum
        if val < 5:
            log_warn(f"Low interval ({val}s) — IP may not always change. 10s recommended.")
        return val
    except (ValueError, EOFError):
        return default

def show_menu():
    show_banner()
    show_real_ip()
    print(f"  {cyan(bold('SELECT MODE'))}")
    print()
    is_root  = check_root()
    root_tag = f" {red('[ROOT→AnonSurf]')}" if is_root else ""
    print(f"  {green('[1]')} Tor Rotation     {gray('-')} every 10s     {gray('| stable')}")
    print(f"  {green('[2]')} Tor Custom        {gray('-')} your interval {gray('| flexible')}{root_tag}")
    print(f"  {green('[3]')} Proxy Rotation    {gray('-')} every Xs      {gray('| thousands of IPs')}")
    print(f"  {yellow('[4]')} torsocks Setup    {gray('-')} {yellow('route tools through Tor')}")
    print(f"  {cyan('[5]')} Show Real IP")
    print(f"  {red('[6]')} AnonSurf Mode    {gray('-')} {red('ROOT')} {gray('| ALL traffic through Tor | static or rotate')}")
    print(f"  {red('[0]')} Exit")
    print()
    hr()
    try:
        return input(f"  {cyan('->')} Choose: ").strip()
    except EOFError:
        return '0'

# ─────────────────────────────────────────
#  SIGNAL HANDLER
# ─────────────────────────────────────────
def handle_exit(sig, frame):
    global running, _anonsurf_active
    running = False
    print()
    log_warn("Stopping...")
    if _anonsurf_active:
        log_warn("Flushing AnonSurf iptables rules...")
        if iptables_anonsurf_stop():
            log_ok("iptables flushed — normal routing restored")
        else:
            log_err("Could not flush! Run: iptables -t nat -F OUTPUT")
        _anonsurf_active = False
    run_cmd("pkill tor 2>/dev/null")
    time.sleep(0.5)
    print()
    print(f"  {cyan('Rotations:')} {green(str(stats['rotations']))}")
    print(f"  {cyan('Errors:')}    {red(str(stats['errors']))}")
    print(f"  {cyan('Uptime:')}    {yellow(elapsed())}")
    print()
    log_ok("Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT,  handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def print_session_summary():
    print()
    log_warn("Session ended.")
    print(f"  {cyan('Rotations:')} {green(str(stats['rotations']))}   "
          f"{cyan('Errors:')} {red(str(stats['errors']))}   "
          f"{cyan('Uptime:')} {yellow(elapsed())}")
    print()
    input(gray("  Press Enter to go back to menu..."))

def main():
    global running, _anonsurf_active

    # Termux startup check
    if not IS_TERMUX:
        log_warn("Not running in Termux — some features may not work correctly.")

    while True:
        choice = show_menu()

        if choice == '0':
            log_ok("Goodbye!")
            sys.exit(0)

        elif choice == '1':
            stats["mode"] = "Tor 10s"
            running = True
            try:
                tor_rotation_loop(10)
            except Exception as e:
                log_err(f"Loop crashed: {e}")
            running = False
            run_cmd("pkill tor 2>/dev/null")
            print_session_summary()
            reset_stats()

        elif choice == '2':
            interval = get_interval(default=10, minimum=2)
            is_root  = check_root()
            if is_root:
                stats["mode"] = f"AnonSurf+Tor {interval}s"
                log_ok("Root detected — AnonSurf will be enabled automatically")
            else:
                stats["mode"] = f"Tor {interval}s"
            running = True
            try:
                tor_rotation_loop(interval, anonsurf=is_root)
            except Exception as e:
                log_err(f"Loop crashed: {e}")
                if _anonsurf_active:
                    log_warn("Flushing AnonSurf iptables rules after crash...")
                    iptables_anonsurf_stop()
                    _anonsurf_active = False
            running = False
            run_cmd("pkill tor 2>/dev/null")
            print_session_summary()
            reset_stats()

        elif choice == '3':
            interval = get_interval(default=5, minimum=2)
            stats["mode"] = "Proxy Rotation"
            running = True
            try:
                proxy_rotation_loop(interval)
            except Exception as e:
                log_err(f"Loop crashed: {e}")
            running = False
            print_session_summary()
            reset_stats()

        elif choice == '4':
            torsocks_menu()

        elif choice == '5':
            show_banner()
            show_real_ip()
            input(gray("  Press Enter to go back..."))

        elif choice == '6':
            anonsurf_start()
            running = False
            reset_stats()

        else:
            log_err("Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()
