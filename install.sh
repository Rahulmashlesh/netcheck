#!/bin/bash
echo "Installing NetCheck dependencies..."
pip3 install -r requirements.txt
chmod +x netcheck.py
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  python3 netcheck.py    # Run the monitor"
echo "  ./netcheck.py          # Run directly"