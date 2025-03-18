```markdown
# Tezos ICO Password Recovery Tool v2

![Tezos Logo](assets/tz_recovery.png)

A powerful, multi-threaded tool designed to help recover lost Tezos ICO passwords through advanced pattern matching and brute force techniques.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://pypi.org/project/PyQt5/)

## 📋 Project History

This project is the successor to the original [TEZOS_ICO_PASSWORD_RECOVERY_TOOL](https://github.com/zilin/TEZOS_ICO_PASSWORD_RECOVERY_TOOL) which was created to help Tezos ICO contributors recover their forgotten passwords. This v2 version brings significant improvements:

- Complete rewrite with modern Python practices
- Multi-CPU support for dramatically faster processing
- Improved UI with real-time feedback
- More flexible configuration options
- Better pattern matching algorithms

If you're looking for the original tool, please visit the [legacy repository](https://github.com/zilin/TEZOS_ICO_PASSWORD_RECOVERY_TOOL).

## 🚀 Features

- **Multi-CPU Processing**: Utilizes all available CPU cores (minus one) for maximum performance
- **User-Friendly GUI**: Intuitive interface with real-time progress monitoring
- **Flexible Configuration**: Configure via YAML, environment variables, or command line
- **Session Management**: Save and load recovery sessions
- **Smart Recovery**: Uses pattern matching to prioritize likely password combinations
- **Portable**: Available as both Python package and standalone executable

## 📋 Prerequisites

- Python 3.6 or higher
- PyQt5
- Bitcoin library for cryptographic operations
- PySodium for additional cryptographic functions
- PyYAML for configuration
- psutil for CPU management

## 🔧 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/zilin/tezos-ico-password-recovery-v2.git
cd tezos-ico-password-recovery-v2

# Create and activate virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Using Executable (Windows)

1. Download the latest release from the [Releases](https://github.com/zilin/tezos-ico-password-recovery-v2/releases) page
2. Extract the ZIP file
3. Run `TezosPasswordRecovery.exe`

## 🚀 Usage

### Running the Application

```bash
# Using the installed package
tezos-recovery

# Or directly from source
python src/PassRecoveryMain.py
```

### Configuration Options

#### 1. YAML Configuration File

Create a file named `TezosPasswordRecovery.yml` in the same directory as the executable:

```yaml
email: "your.email@example.com"
mnemonic: "word1 word2 word3 word4 ... word15"
address: "tz1..."
comp1: "component1"
comp2: "component2"
comp3: "component3"
comp4: "component4"
```

#### 2. Environment Variables

```bash
# Windows
set TEZOS_RECOVERY_EMAIL=your.email@example.com
set TEZOS_RECOVERY_MNEMONIC=word1 word2 word3...
set TEZOS_RECOVERY_ADDRESS=tz1...
set TEZOS_RECOVERY_COMP1=component1

# Unix/MacOS
export TEZOS_RECOVERY_EMAIL=your.email@example.com
export TEZOS_RECOVERY_MNEMONIC="word1 word2 word3..."
export TEZOS_RECOVERY_ADDRESS=tz1...
export TEZOS_RECOVERY_COMP1=component1
```

#### 3. Command Line Arguments

```bash
python src/PassRecoveryMain.py --email your.email@example.com --mnemonic "word1 word2..." --address tz1...
```

### Configuration Priority

1. Environment Variables (highest)
2. YAML Configuration File
3. Command Line Arguments
4. GUI Input (lowest)

## 📊 Password Recovery Process

1. **Input Parameters**: Provide your email, mnemonic phrase, and Tezos address
2. **Password Components**: Enter known parts of your password
3. **Start Recovery**: Click "Start" to begin the recovery process
4. **Monitor Progress**: Watch real-time statistics on attempts, speed, and best matches
5. **Test Results**: Use the "Test" button to verify potential matches

## 🛠️ Building from Source

### Building the UI

```bash
python uibuild.py
```

### Creating an Executable

```bash
python build_exe.py
```

The executable will be created in the `dist` directory.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_password_recovery.py
```

## 📁 Project Structure

```
tezos-ico-password-recovery-v2/
├── src/                      # Source code
│   ├── models/               # Core logic models
│   │   └── password_recovery.py
│   ├── ui/                   # UI definitions
│   │   └── passrecoverywindow.ui
│   ├── PassRecoveryMain.py   # Main application entry
│   ├── functions.py          # Utility functions
│   ├── config.py             # Configuration handling
│   └── processor_manager.py  # CPU management
├── assets/                   # Images and icons
│   ├── tz_recovery.ico
│   └── tz_recovery.png
├── tests/                    # Test suite
├── docs/                     # Documentation
├── .github/                  # GitHub templates and workflows
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
├── uibuild.py                # UI builder
├── build_exe.py              # Executable builder
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## 🔄 Performance Optimization

- The tool automatically detects available CPU cores and uses all but one
- CPU affinity is set to optimize performance
- Update frequency can be adjusted in the UI to balance UI responsiveness and recovery speed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- The original TEZOS_ICO_PASSWORD_RECOVERY_TOOL project and its contributors
- The Tezos community for their support and feedback
- PyQt5 for the GUI framework
- Bitcoin library contributors
- All open-source contributors who made this possible

## 📧 Contact

Zi Lin - zi.lin@zzv.io

Project Link: [https://github.com/zilin/tezos-ico-password-recovery-v2](https://github.com/zilin/tezos-ico-password-recovery-v2)

---

⭐️ If this tool helped you recover your Tezos ICO password, please consider starring the repository!
```
