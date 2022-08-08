#!/bin/bash
# Note: GPM Installation script

# Ensure installing on correct system
function checkOS {
    OS=$(uname)

    if [[ $OS == "Linux" ]]; then
        # Determine linux distro

        # Debian
        if [[ -f /etc/debian_version ]]; then
            DIST="Debian"

        # Arch
        elif [[ -f /etc/arch-release ]]; then
            DIST="Arch"

        # Fedora
        elif [[ -f /etc/fedora-release ]]; then
	        DIST="Fedora"

        # Other
        else
            printerr "This distribution is not supported, exiting!"
            exit

        fi

    elif [[ $OS == "Darwin" ]]; then
        : # Pass unsupported os trap

    else
        # NOTE: Consider support for Windows
        echo "Unsupported OS: $OS"
        exit

    fi

}

# Ensure Python is installed
function checkPython {
    :
}

# Ensure pip is installed
function checkPip {
    :
}