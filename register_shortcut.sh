#!/bin/bash

# Configuration
KEY_Name="Clicky Area Screenshot"
KEY_Command="/home/yurix/Documentos/my-clicky/clicky_cli.sh --area"
KEY_Binding="<Shift><Super>s"
SCHEMA="org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"
PATH_PREFIX="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/clicky-area/"

# Generate UUID-like path or fixed path
# For simplicity, we use a fixed path 'clicky-area'

echo "Registering shortcut..."

gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['$PATH_PREFIX']"
gsettings set $SCHEMA:$PATH_PREFIX name "$KEY_Name"
gsettings set $SCHEMA:$PATH_PREFIX command "$KEY_Command"
gsettings set $SCHEMA:$PATH_PREFIX binding "$KEY_Binding"

echo "Shortcut '$KEY_Binding' registered to '$KEY_Command'"
