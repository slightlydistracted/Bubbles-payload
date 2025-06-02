#!/bin/bash
echo "[*] Installing core systems..."

# Ensure base folders exist
mkdir -p ~/feralsys/inbox ~/feralsys/sandbox ~/feralsys/logs

# Set up .bashrc launcher if not already present
if ! grep -q "autopilot.txt" ~/.bashrc; then
  echo "bash ~/feralsys/autopilot.txt &" >> ~/.bashrc
fi

# Permissions and boot files
chmod +x ~/feralsys/*.sh

echo "[+] Core system ready. Autopilot will start on next Termux session."
