#!/bin/bash
# This script removes the custom .asoundrc file from the home directory.

set -e

ASOUNDRC_FILE=~/.asoundrc

echo "🔊 Deleting custom ALSA configuration..."

if [ -f "$ASOUNDRC_FILE" ]; then
    rm -f "$ASOUNDRC_FILE"
    echo "✅ Successfully removed $ASOUNDRC_FILE."
    echo "ALSA will now use the system default configuration."
    echo "You may need to restart applications for this to take effect."
else
    echo "✅ Custom .asoundrc file not found. Nothing to do."
fi