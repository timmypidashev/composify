#!/bin/bash
# Note: GPM Installation script 

# Determine Linux distribution if applicable
function whichDist {

    # Debian
    if [[ -f /etc/debian_version ]]; then
        DIST="Debian"
    
    # Arch
    elif [[ -f /etc/arch-release ]]; then
        DIST="Arch"
        
    else
        # NOTE: Add more distribution support with time 
        echo "Unsupported distribution"
        exit 1
    fi
}
}

# Ensure installing on correct system
function whichOS {
    OS=$(uname)

    if [[ $OS == "Linux" ]]; then
        whichDist
    
    elif [[ $OS == "Darwin" ]]; then
        :
    
    else
        # NOTE: Add support for Windows in the future 
        echo "Unsupported OS"
        exit 1
    fi

}

# Ensure python is installed
function ensurePython {
    :
}

# Ensure pip is installed
function ensurePip {
    :
}