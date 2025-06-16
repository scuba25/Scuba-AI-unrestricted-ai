#!/bin/bash

# Scuba AI - Complete Installation Script
# This script automatically installs Scuba AI and all dependencies

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/scuba25/Scuba-AI-unrestricted-ai.git"
APP_DIR="Scuba-AI-unrestricted-ai"
PYTHON_MIN_VERSION="3.7"

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/ubuntu-release ] || [ -f /etc/debian_version ]; then
            echo "ubuntu"
        elif [ -f /etc/centos-release ] || [ -f /etc/redhat-release ]; then
            echo "centos"
        elif [ -f /etc/arch-release ]; then
            echo "arch"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Install Python based on OS
install_python() {
    local os=$(detect_os)
    print_status "Installing Python 3.7+ for $os..."
    
    case $os in
        "ubuntu")
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv git curl
            ;;
        "centos")
            sudo yum update -y
            sudo yum install -y python3 python3-pip git curl
            ;;
        "arch")
            sudo pacman -Sy --noconfirm python python-pip git curl
            ;;
        "macos")
            if command_exists brew; then
                brew install python git curl
            else
                print_error "Homebrew not found. Please install Python 3.7+ manually."
                exit 1
            fi
            ;;
        "windows")
            print_warning "Windows detected. Please ensure Python 3.7+ is installed manually."
            print_warning "You can download it from: https://www.python.org/downloads/"
            ;;
        *)
            print_error "Unsupported operating system: $os"
            exit 1
            ;;
    esac
}

# Check Python version
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif command_exists python; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_error "Python not found. Installing..."
        install_python
        return
    fi
    
    # Check version
    local python_version=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    local major_version=$(echo $python_version | cut -d. -f1)
    local minor_version=$(echo $python_version | cut -d. -f2)
    
    if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 7 ]; then
        print_success "Python $python_version found"
    else
        print_error "Python 3.7+ required. Found: $python_version"
        install_python
    fi
}

# Install system dependencies
install_dependencies() {
    print_status "Checking system dependencies..."
    
    # Check for git
    if ! command_exists git; then
        print_status "Installing git..."
        local os=$(detect_os)
        case $os in
            "ubuntu") sudo apt install -y git ;;
            "centos") sudo yum install -y git ;;
            "arch") sudo pacman -S --noconfirm git ;;
            "macos") brew install git ;;
        esac
    fi
    
    # Check for curl
    if ! command_exists curl; then
        print_status "Installing curl..."
        local os=$(detect_os)
        case $os in
            "ubuntu") sudo apt install -y curl ;;
            "centos") sudo yum install -y curl ;;
            "arch") sudo pacman -S --noconfirm curl ;;
            "macos") brew install curl ;;
        esac
    fi
}

# Clone repository
clone_repository() {
    print_status "Cloning Scuba AI repository..."
    
    if [ -d "$APP_DIR" ]; then
        print_warning "Directory $APP_DIR already exists. Removing..."
        rm -rf "$APP_DIR"
    fi
    
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
    print_success "Repository cloned successfully"
}

# Setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    $PYTHON_CMD -m venv venv
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        print_error "Failed to find virtual environment activation script"
        exit 1
    fi
    
    # Upgrade pip
    pip install --upgrade pip
    print_success "Virtual environment created and activated"
}

# Install Python packages
install_packages() {
    print_status "Installing Python packages..."
    
    pip install -r requirements.txt
    print_success "Python packages installed"
}

# Create configuration files
create_config() {
    print_status "Creating configuration files..."
    
    # Create .env file
    cat > .env << EOF
# Scuba AI Configuration
# Copy this file and customize as needed

# API Configuration
GROQ_API_KEY=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
MODEL_NAME=llama-3.1-8b-instant

# Server Configuration
PORT=3000
DEBUG=True
SECRET_KEY=scuba-ai-secret-key-change-in-production

# Host Configuration
HOST=45.56.124.122
EOF

    print_success "Configuration file created (.env)"
}

# Create startup scripts
create_scripts() {
    print_status "Creating startup scripts..."
    
    # Development start script
    cat > start.sh << 'EOF'
#!/bin/bash
echo "Starting Scuba AI in development mode..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
python app.py
EOF
    
    # Production start script
    cat > start-production.sh << 'EOF'
#!/bin/bash
echo "Starting Scuba AI in production mode..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
gunicorn -w 4 -b 0.0.0.0:3000 app:app
EOF
    
    # Update script
    cat > update.sh << 'EOF'
#!/bin/bash
echo "Updating Scuba AI..."
git pull origin main
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
pip install -r requirements.txt --upgrade
echo "Update complete!"
EOF
    
    # Make scripts executable
    chmod +x start.sh start-production.sh update.sh
    
    print_success "Startup scripts created"
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python imports
    $PYTHON_CMD -c "
import flask
import requests
import json
import os
from datetime import datetime
print('All required modules imported successfully')
"
    
    if [ $? -eq 0 ]; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed"
        exit 1
    fi
}

# Main installation function
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    SCUBA AI INSTALLER                        ║"
    echo "║                 Unfiltered & Unrestricted                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    print_status "Starting Scuba AI installation..."
    
    # Check system
    local os=$(detect_os)
    print_status "Detected OS: $os"
    
    # Install dependencies
    install_dependencies
    
    # Check Python
    check_python
    
    # Clone repository
    clone_repository
    
    # Setup virtual environment
    setup_venv
    
    # Install packages
    install_packages
    
    # Create configuration
    create_config
    
    # Create scripts
    create_scripts
    
    # Test installation
    test_installation
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 INSTALLATION COMPLETE!                      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    print_success "Scuba AI has been successfully installed!"
    echo
    print_status "📁 Installation directory: $(pwd)"
    print_status "🔑 Edit .env file to configure your API key"
    echo
    print_status "🚀 To start Scuba AI:"
    echo "   Development: ./start.sh"
    echo "   Production:  ./start-production.sh"
    echo
    print_status "🔧 To update: ./update.sh"
    echo
    print_status "🌐 Access your app at: http://localhost:3000"
    echo
    print_warning "⚠️  Make sure to set your GROQ_API_KEY in the .env file!"
    
}

# Handle interrupts
trap 'print_error "Installation interrupted"; exit 1' INT TERM

# Run main function
main "$@"