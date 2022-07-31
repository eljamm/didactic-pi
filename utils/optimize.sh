#!/bin/bash

# Install Zram
wget -O zram-swap.zip "https://github.com/foundObjects/zram-swap/archive/refs/heads/master.zip"
unzip zram-swap.zip && rm zram-swap.zip
cd zram-swap-master/ && sudo ./install.sh
cd .. && rm -rf zram-swap-master/

# Kernel Parameters
sudo tee -a /etc/sysctl.conf <<-'EOF'
vm.vfs_cache_pressure=500
vm.swappiness=100
vm.dirty_background_ratio=1
vm.dirty_ratio=50
EOF

# Remove Default Swap
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove
sudo apt purge -y dphys-swapfile

# Reboot
sudo reboot now
