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

## 💻 Development Setup

### Visual Studio Code Configuration

For VS Code users, here's a sample `.vscode/launch.json` configuration for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Password Recovery (UI)",
            "type": "debugpy",
            "request": "launch",
            "program": "src/PassRecoveryMain.py",
            "args": [
                "--email",
                "example@example.com",
                "--mnemonic",
                "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14",
                "--address",
                "tz1exampleAddressxxxxxxxxxxxxxxxxxxx",
                "--comp1",
                "optional_component1",
                "--comp2",
                "optional_component2",
                "--comp3",
                "optional_component3",
                "--comp4",
                "optional_component4"
            ],
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Password Recovery (No UI)",
            "type": "debugpy",
            "request": "launch",
            "program": "src/PassRecoveryMain.py",
            "args": [
                "--noui",
                "--email",
                "example@example.com",
                "--mnemonic",
                "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14",
                "--address",
                "tz1exampleAddressxxxxxxxxxxxxxxxxxxx",
                "--comp1",
                "optional_component1",
                "--comp2",
                "optional_component2",
                "--comp3",
                "optional_component3",
                "--comp4",
                "optional_component4"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

Note: Replace the placeholder values with your actual test data. The components (comp1-4) are optional and can be left empty if not needed.

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

This project uses pytest for testing. Here's how to run the tests:

### Running Tests

```bash
# Install pytest if you don't have it
pip install pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_password_recovery.py

# Run a specific test class
pytest tests/test_password_recovery.py::TestPasswordRecovery

# Run a specific test method
pytest tests/test_password_recovery.py::TestPasswordRecovery::test_password_check_correct
```

### Setting Up Your Environment for Testing

If you encounter import errors when running tests, ensure your Python path is set correctly:

```bash
# Run pytest with the current directory in the Python path
PYTHONPATH=. pytest

# Or on Windows
set PYTHONPATH=.
pytest
```

### Test Structure

The tests follow these principles:
- Unit tests with predictable results
- Mocked dependencies for consistent behavior
- Comprehensive coverage of core functionality
- Clear assertions about expected outcomes

### Creating New Tests

When creating new tests:
1. Place them in the `tests/` directory
2. Name test files with the prefix `test_`
3. Use the `unittest.TestCase` class or pytest fixtures
4. Mock external dependencies to ensure predictable results

### Automated Test Generation

This project supports automated test generation using Ollama:

```bash
# Generate a test for a specific file
python generate_tests.py src/models/password_recovery.py

# Monitor the project directory and update tests automatically
python monitor_tests.py
```

See the "Using Ollama to Create and Maintain Test Cases" section for more details.

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

## Technical Overview

This application is built using:

- **Python 3.8+** as the core programming language
- **PyQt5** for the cross-platform desktop UI
- **Multi-threading** for performance optimization, allowing UI responsiveness during intensive operations
- **Model-View-Controller (MVC)** architecture:
  - **Model**: Handles password recovery logic and state management
  - **View**: PyQt5-based UI components
  - **Controller**: Manages interaction between model and view
- **Object-oriented design** with clear separation of concerns
- **Comprehensive logging** for debugging and analysis

The application can be run directly from Python or compiled into standalone executables for Windows, macOS, and Linux using PyInstaller.

## Using Ollama to Create and Maintain Test Cases

To use Ollama for creating test cases and continuously monitoring your project directory to adjust tests as your code evolves, you'll need to set up a workflow that combines Ollama's capabilities with file system monitoring. Here's a comprehensive approach:

## 1. Setting Up Ollama for Test Case Generation

First, ensure you have Ollama installed and running with an appropriate model:

```bash
# Install Ollama if you haven't already
# From https://ollama.com/

# Pull a suitable model for code generation
ollama pull codellama:7b-instruct  # Good balance of size and capability
# or
ollama pull llama3:8b  # Another good option
```

## 2. Create a Test Case Generation Script

Create a Python script that interfaces with Ollama to generate test cases:

```python
#!/usr/bin/env python3
import os
import json
import subprocess
import argparse

def get_file_content(file_path):
    """Read the content of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def generate_test_with_ollama(file_path, model="codellama:7b-instruct"):
    """Generate a test case for a given file using Ollama."""
    file_content = get_file_content(file_path)
    file_name = os.path.basename(file_path)
    
    prompt = f"""
    Create a comprehensive test case for the following Python file:
    
    ```python
    {file_content}
    ```README.md
    
    Please generate a pytest-compatible test file that:
    1. Tests all public functions and methods
    2. Includes edge cases and error conditions
    3. Uses mocks where appropriate for external dependencies
    4. Follows best practices for Python testing
    
    Return ONLY the test code without explanations.
    """
    
    # Call Ollama API
    result = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True,
        text=True
    )
    
    # Extract the test code from the response
    test_code = result.stdout.strip()
    
    # Clean up the response if needed (remove markdown code blocks if present)
    if test_code.startswith("```python"):
        test_code = "\n".join(test_code.split("\n")[1:-1])
    if test_code.startswith("```"):
        test_code = "\n".join(test_code.split("\n")[1:-1])
    
    # Create test file name
    base_name = os.path.splitext(file_name)[0]
    test_file_name = f"test_{base_name}.py"
    test_file_path = os.path.join("tests", test_file_name)
    
    # Ensure tests directory exists
    os.makedirs("tests", exist_ok=True)
    
    # Write the test file
    with open(test_file_path, 'w') as file:
        file.write(test_code)
    
    print(f"Generated test file: {test_file_path}")
    return test_file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate test cases using Ollama")
    parser.add_argument("file_path", help="Path to the Python file to generate tests for")
    parser.add_argument("--model", default="codellama:7b-instruct", help="Ollama model to use")
    
    args = parser.parse_args()
    generate_test_with_ollama(args.file_path, args.model)
```

## 3. Create a File Monitoring Script

Now, create a script that monitors your project directory for changes and triggers test generation:

```python
#!/usr/bin/env python3
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse

# Import the test generation function from the previous script
from generate_tests import generate_test_with_ollama

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, src_dir, test_dir, model):
        self.src_dir = src_dir
        self.test_dir = test_dir
        self.model = model
        self.last_modified = {}
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only process Python files in the source directory
        if not event.src_path.endswith('.py'):
            return
            
        # Skip test files
        if '/tests/' in event.src_path or event.src_path.startswith('test_'):
            return
            
        # Avoid processing the same file multiple times in quick succession
        current_time = time.time()
        if event.src_path in self.last_modified:
            if current_time - self.last_modified[event.src_path] < 5:  # 5 second cooldown
                return
                
        self.last_modified[event.src_path] = current_time
        
        print(f"File changed: {event.src_path}")
        try:
            # Generate or update test case
            test_file = generate_test_with_ollama(event.src_path, self.model)
            print(f"Updated test case: {test_file}")
            
            # Run the test to verify it works
            subprocess.run(["pytest", test_file, "-v"])
        except Exception as e:
            print(f"Error generating test for {event.src_path}: {str(e)}")

def monitor_directory(src_dir, test_dir, model):
    event_handler = CodeChangeHandler(src_dir, test_dir, model)
    observer = Observer()
    observer.schedule(event_handler, src_dir, recursive=True)
    observer.start()
    
    print(f"Monitoring directory: {src_dir}")
    print(f"Test cases will be saved to: {test_dir}")
    print(f"Using Ollama model: {model}")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor directory and generate tests with Ollama")
    parser.add_argument("--src", default="src", help="Source directory to monitor")
    parser.add_argument("--tests", default="tests", help="Directory to save test files")
    parser.add_argument("--model", default="codellama:7b-instruct", help="Ollama model to use")
    
    args = parser.parse_args()
    
    # Create test directory if it doesn't exist
    os.makedirs(args.tests, exist_ok=True)
    
    monitor_directory(args.src, args.tests, args.model)
```

## 4. Install Required Dependencies

```bash
pip install watchdog pytest
```

## 5. Run the Monitoring Script

```bash
python monitor_tests.py --src src --tests tests --model codellama:7b-instruct
```

## 6. Integrating with Your Development Workflow

For a more integrated approach:

1. **Create a pre-commit hook** that generates tests for changed files
2. **Set up a CI/CD pipeline** that uses Ollama to validate and update tests
3. **Create a VS Code task** to run the monitoring script

### Example VS Code Task

Add this to your `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Monitor and Generate Tests",
            "type": "shell",
            "command": "python monitor_tests.py",
            "isBackground": true,
            "problemMatcher": []
        }
    ]
}
```

## 7. Best Practices for AI-Generated Tests

1. **Always review generated tests** - AI might miss edge cases or misunderstand your code
2. **Maintain a test baseline** - Keep some manually written tests as a quality benchmark
3. **Customize the prompts** - Adjust the prompts to match your project's testing style
4. **Use test coverage tools** - Verify that generated tests actually cover your code
5. **Periodically regenerate all tests** - As your LLM models improve, regenerate tests

## 8. Handling Complex Projects

For larger projects:

1. **Create a test generation configuration file** that specifies:
   - Which files to monitor
   - Special testing requirements for each module
   - Custom prompts for different types of code

2. **Implement test merging** to preserve manual additions to generated tests

This approach creates a continuous feedback loop where your tests evolve alongside your code, leveraging Ollama's capabilities to maintain comprehensive test coverage.