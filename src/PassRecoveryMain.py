from functions import check  # Add this import
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QSplashScreen
import sys
import logging
from datetime import datetime
import os
import argparse
from models.password_recovery import (
    PasswordRecoveryModel,
    PasswordComponents,
    PasswordAttempt,
)
from ui.passrecoverywindow import PassRecoveryWindow  # Updated import name
from config import load_config


# Define a function to get absolute paths to assets
def get_asset_path(filename):
    """Get the absolute path to an asset file, searching in multiple possible locations."""
    # Get the directory where the script is located
    if getattr(sys, "frozen", False):
        # If running as compiled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # If running as script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define possible asset locations (in order of preference)
    possible_locations = [
        os.path.join(base_dir, "assets", filename),  # src/assets/filename
        os.path.join(
            os.path.dirname(base_dir), "assets", filename
        ),  # project_root/assets/filename
        os.path.join(base_dir, filename),  # src/filename
        os.path.join(os.path.dirname(base_dir), filename),  # project_root/filename
    ]

    # Return the first path that exists
    for path in possible_locations:
        if os.path.exists(path):
            print(f"Found asset: {filename} at {path}")
            return path

    # If not found, log the error and return the most likely path
    print(f"WARNING: Asset not found: {filename}")
    print(f"Searched in: {possible_locations}")
    return os.path.join(
        base_dir, "assets", filename
    )  # Return a default path for debugging


# Set up logging
def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("TezosPasswordFinder")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    log_file = f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler(sys.stdout)

    # Create formatters
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


class PasswordRecoveryThread(QThread):
    # Clear signal names indicating their purpose
    improvement_found = pyqtSignal(dict)  # Emits when better result found
    new_best_attempt = pyqtSignal(object)  # Emits on best attempt
    component_update = pyqtSignal(object)  # Emits on component changes

    def __init__(self, model: PasswordRecoveryModel, parent=None):
        super().__init__(parent)
        self.model = model
        self.is_active = True
        self.is_paused = False
        self.current_stats = {}
        self.current_components = None
        self.current_attempt = None
        logger.info("Recovery thread initialized")

    def run(self):
        logger.info("Recovery thread started")
        try:
            while self.is_active:
                if self.is_paused:
                    self.msleep(100)
                    continue

                # Process password attempt
                components = self.model.components
                attempt_result = self.model.process_attempt(components.comp1)
                current_stats = self.model.get_statistics()

                # Emit only on improvements
                if attempt_result.is_improvement:
                    self.current_stats = current_stats
                    self.current_components = components
                    self.current_attempt = attempt_result

                    # Signal improvements
                    self.improvement_found.emit(current_stats)
                    self.component_update.emit(components)
                    self.new_best_attempt.emit(attempt_result)

                self.msleep(1)  # Prevent CPU overload

        except Exception as e:
            logger.error(f"Thread error: {str(e)}", exc_info=True)

    def get_current_stats(self):
        return self.current_stats

    def get_current_components(self):
        return self.current_components

    def get_current_attempt(self):
        return self.current_attempt

    def stop(self):
        logger.info("Stopping Password Recovery Thread")
        self.is_active = False
        self.wait()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, params=None, parent=None):
        super().__init__(parent)
        self.model = model
        self.ui = PassRecoveryWindow()  # Updated class name
        self.ui.setupUi(self)

        # Recovery thread
        self.recovery_thread = None

        # Set initial parameters if provided
        if params:
            self.set_initial_params(params)

        # Connect UI signals
        self.setup_connections()
        logger.info("PassRecoveryWindow initialized")

    def connect_thread_signals(self, recovery_thread: PasswordRecoveryThread):
        """Connect thread signals to UI updates"""
        self.recovery_thread = recovery_thread

        # Connect improvement signals to UI updates
        self.recovery_thread.new_best_attempt.connect(self.update_best_attempt)
        self.recovery_thread.improvement_found.connect(self.update_statistics)
        self.recovery_thread.component_update.connect(self.update_components)

    def update_best_attempt(self, attempt):
        """Update UI with new best attempt"""
        if attempt.is_improvement:
            self.update_attempt_display(attempt)
            self.ui.statusLabel.setText("New improvement found!")

    def set_initial_params(self, params):
        """Set initial parameters in UI fields"""
        try:
            # Set text fields
            if params.get("email"):
                self.ui.emailInput.setText(params["email"])
            if params.get("mnemonic"):
                self.ui.mnemonicInput.setText(params["mnemonic"])
            if params.get("address"):
                self.ui.addressInput.setText(params["address"])
            if params.get("comp1"):
                self.ui.comp1Input.setText(params["comp1"])
            if params.get("comp2"):
                self.ui.comp2Input.setText(params["comp2"])
            if params.get("comp3"):
                self.ui.comp3Input.setText(params["comp3"])
            if params.get("comp4"):
                self.ui.comp4Input.setText(params["comp4"])

            # Update model with initial values
            self.model.set_parameters(
                email=params.get("email", ""),
                mnemonic=params.get("mnemonic", ""),
                address=params.get("address", ""),
            )
            self.model.set_components(
                comp1=params.get("comp1", ""),
                comp2=params.get("comp2", ""),
                comp3=params.get("comp3", ""),
                comp4=params.get("comp4", ""),
            )

            logger.info("Initial parameters set in UI")
        except Exception as e:
            logger.error(f"Error setting initial parameters: {str(e)}")

    def setup_connections(self):
        """Set up UI signal connections"""
        try:
            self.ui.startButton.clicked.connect(self.start_button_clicked)
            self.ui.pauseButton.clicked.connect(self.pause_button_clicked)
            self.ui.testButton.clicked.connect(self.test_button_clicked)

            # Connect menu actions
            self.ui.actionNewSession.triggered.connect(self.new_session)
            self.ui.actionLoadSession.triggered.connect(self.load_session)
            self.ui.actionSaveSession.triggered.connect(self.save_session)
            self.ui.actionExit.triggered.connect(self.close)

            logger.debug("UI connections established")
        except Exception as e:
            logger.error(f"Error setting up connections: {str(e)}")

    def start_button_clicked(self):
        try:
            # Update model with current UI values
            self.model.set_parameters(
                email=self.ui.emailInput.text(),
                mnemonic=self.ui.mnemonicInput.text(),
                address=self.ui.addressInput.text(),
            )

            self.model.set_components(
                comp1=self.ui.comp1Input.text(),
                comp2=self.ui.comp2Input.text(),
                comp3=self.ui.comp3Input.text(),
                comp4=self.ui.comp4Input.text(),
            )

            # Start new recovery thread if not running
            if not self.recovery_thread or not self.recovery_thread.isRunning():
                self.recovery_thread = PasswordRecoveryThread(self.model)
                self.connect_thread_signals(self.recovery_thread)
                self.recovery_thread.start()
                self.ui.startButton.setText("Stop")
                self.ui.statusLabel.setText("Recovery running...")
            else:
                # Stop if already running
                self.recovery_thread.stop()
                self.recovery_thread.wait()
                self.recovery_thread = None
                self.ui.startButton.setText("Start")
                self.ui.statusLabel.setText("Recovery stopped")

            logger.info("Start/Stop button clicked")

        except Exception as e:
            logger.error(f"Error in start button handler: {str(e)}")
            self.ui.statusLabel.setText(f"Error: {str(e)}")

    def pause_button_clicked(self):
        try:
            if self.recovery_thread and self.recovery_thread.isRunning():
                self.recovery_thread.is_paused = not self.recovery_thread.is_paused
                if self.recovery_thread.is_paused:
                    self.ui.pauseButton.setText("Resume")
                    self.ui.statusLabel.setText("Recovery paused")
                else:
                    self.ui.pauseButton.setText("Pause")
                    self.ui.statusLabel.setText("Recovery running...")
                logger.info(
                    f"Recovery {'paused' if self.recovery_thread.is_paused else 'resumed'}"
                )
        except Exception as e:
            logger.error(f"Error in pause button handler: {str(e)}")

    def test_button_clicked(self):
        try:
            # Get current parameters
            password = self.ui.comp1Input.text()  # Test with first component
            email = self.ui.emailInput.text()
            mnemonic = self.ui.mnemonicInput.text()
            address = self.ui.addressInput.text()

            # Run single test using model
            attempt = self.model.process_attempt(password)
            test_address = attempt.password
            result = "True" if attempt.distance == 0 else "False"

            # Update status
            if result == "True":
                self.ui.statusLabel.setText(
                    f"Test SUCCESS! Address matches: {test_address}"
                )
            else:
                self.ui.statusLabel.setText(f"Test result: Generated {test_address}")

            logger.info(f"Test completed: {result}")

        except Exception as e:
            logger.error(f"Error in test button handler: {str(e)}")
            self.ui.statusLabel.setText(f"Test error: {str(e)}")

    def update_statistics(self, stats: dict):
        try:
            if not stats:
                return

            self.ui.attemptsLabel.setText(f"Attempts: {stats['total_attempts']:,}")
            self.ui.speedLabel.setText(f"Speed: {stats['attempts_per_second']:.2f}/s")

            if stats["best_distance"] == float("inf"):
                self.ui.distanceLabel.setText("Best Distance: ∞")
            else:
                self.ui.distanceLabel.setText(
                    f"Best Distance: {stats['best_distance']:.2f}"
                )

            if stats.get("best_password"):
                self.ui.bestResultLabel.setText(
                    f"Best Result: {stats['best_password']}"
                )

        except Exception as e:
            logger.error(f"Error updating stats: {str(e)}")

    def update_components(self, components: PasswordComponents):
        try:
            self.ui.currentCompLabel.setText(
                f"Current Components: {components.comp1}, {components.comp2}, "
                f"{components.comp3}, {components.comp4}"
            )
        except Exception as e:
            logger.error(f"Error updating components: {str(e)}")

    def update_attempt_display(self, attempt: PasswordAttempt):
        try:
            if attempt.is_improvement:
                self.ui.bestResultLabel.setText(
                    f"Best Result: {attempt.password} (Distance: {attempt.distance:.2f})"
                )
            self.ui.lastAttemptLabel.setText(
                f"Last Attempt: {attempt.password} (Distance: {attempt.distance:.2f})"
            )
        except Exception as e:
            logger.error(f"Error updating attempt: {str(e)}")

    def new_session(self):
        self.ui.emailInput.clear()
        self.ui.mnemonicInput.clear()
        self.ui.addressInput.clear()
        self.ui.comp1Input.clear()
        self.ui.comp2Input.clear()
        self.ui.comp3Input.clear()
        self.ui.comp4Input.clear()
        self.ui.statusLabel.setText("Status: Ready")

    def load_session(self):
        # Implement session loading
        pass

    def save_session(self):
        # Implement session saving
        pass

    def closeEvent(self, event):
        """Handle window close event"""
        try:
            if self.recovery_thread and self.recovery_thread.isRunning():
                self.recovery_thread.stop()
                self.recovery_thread.wait()
            event.accept()
        except Exception as e:
            logger.error(f"Error in close event: {str(e)}")
            event.accept()


class PassRecoveryMain:
    def __init__(self, show_ui=True, params=None):
        logger.info("Initializing Password Recovery Main")
        self.model = PasswordRecoveryModel()
        self.recovery_thread = None
        self.window = None

        # Load config if exists
        if getattr(sys, "frozen", False):
            # Running as compiled
            config = load_config(sys.executable)
        else:
            # Running as script
            config = load_config()

        # Override params with config if exists
        if config:
            params = config
            logger.info("Using configuration from YAML file")

        self.params = params

        if show_ui:
            self.init_ui()

    def init_ui(self):
        """Initialize UI in a separate thread if needed"""
        try:
            self.app = QtWidgets.QApplication(sys.argv)

            # Get path relative to executable
            if getattr(sys, "frozen", False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))

            # Create and show splash screen
            splash_path = get_asset_path("tz_recovery.png")
            print(f"Loading splash image from: {splash_path}")

            # Force load the image and check if it's valid
            splash_pix = QPixmap(splash_path)
            if splash_pix.isNull():
                print(f"ERROR: Failed to load splash image from {splash_path}")
            else:
                print(
                    f"Splash image loaded successfully: {splash_pix.width()}x{splash_pix.height()}"
                )

            class MovableSplash(QSplashScreen):
                def mousePressEvent(self, event):
                    self.offset = event.pos()

                def mouseMoveEvent(self, event):
                    x = event.globalX()
                    y = event.globalY()
                    self.move(x - self.offset.x(), y - self.offset.y())

                def mouseDoubleClickEvent(self, event):
                    self.close()

            splash = MovableSplash(splash_pix, Qt.WindowStaysOnTopHint)
            splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            splash.showMessage(
                "TEZOS PASSWORD RECOVERY V.2.00.01",
                Qt.AlignCenter | Qt.AlignBottom,
                Qt.white,
            )
            splash.show()

            # Process events to show splash immediately
            self.app.processEvents()

            # Set up main window
            icon_path = get_asset_path("tz_recovery.ico")
            print(f"Loading icon from: {icon_path}")

            # Force load the icon and check if it's valid
            app_icon = QIcon(icon_path)
            if app_icon.isNull():
                print(f"ERROR: Failed to load icon from {icon_path}")
            else:
                print("Icon loaded successfully")

            self.app.setWindowIcon(app_icon)

            if sys.platform == "win32":
                import ctypes

                myappid = "tezos.password.recovery.1.0"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

            self.window = MainWindow(self.model, self.params)
            self.window.setWindowIcon(app_icon)

            # Close splash after 2 seconds
            QTimer.singleShot(2000, splash.close)

            # Show main window
            self.window.show()

            logger.info("UI initialized with splash screen")
        except Exception as e:
            logger.error(f"Error initializing UI: {str(e)}", exc_info=True)
            sys.exit(1)

    def start_recovery(self, params=None):
        """Start recovery process with optional parameters"""
        try:
            logger.info("Starting password recovery")

            # If params provided (command line mode), set them
            if params:
                self.model.set_parameters(
                    email=params.get("email", ""),
                    mnemonic=params.get("mnemonic", ""),
                    address=params.get("address", ""),
                )
                self.model.set_components(
                    comp1=params.get("comp1", ""),
                    comp2=params.get("comp2", ""),
                    comp3=params.get("comp3", ""),
                    comp4=params.get("comp4", ""),
                )

            self.model.start_session()

            # Clean up old thread if exists
            if self.recovery_thread:
                self.recovery_thread.stop()
                self.recovery_thread.wait()

            # Create and start new thread
            self.recovery_thread = PasswordRecoveryThread(self.model)

            # Connect window to thread if UI exists
            if self.window:
                self.window.connect_thread_signals(self.recovery_thread)

            self.recovery_thread.start()
            logger.info("Recovery thread started")

        except Exception as e:
            logger.error(f"Error starting recovery: {str(e)}", exc_info=True)
            raise

    def stop_recovery(self):
        """Stop the recovery process"""
        if self.recovery_thread:
            self.recovery_thread.stop()
            logger.info("Recovery stopped")

    def run(self):
        """Main run method"""
        try:
            if self.window:
                # If UI exists, start Qt event loop
                return self.app.exec_()
            else:
                # If no UI, just run the recovery process
                self.start_recovery()
                # Wait for recovery thread to finish
                if self.recovery_thread:
                    self.recovery_thread.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.stop_recovery()
        except Exception as e:
            logger.error(f"Error in main run: {str(e)}")
            return 1
        return 0


def main():
    parser = argparse.ArgumentParser(description="Tezos Password Recovery Tool")
    parser.add_argument("--noui", action="store_true", help="Run without UI")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--mnemonic", help="Mnemonic phrase")
    parser.add_argument("--address", help="Target address")
    parser.add_argument("--comp1", help="Component 1")
    parser.add_argument("--comp2", help="Component 2")
    parser.add_argument("--comp3", help="Component 3")
    parser.add_argument("--comp4", help="Component 4")

    args = parser.parse_args()

    # Create params dictionary from arguments
    params = {
        "email": args.email,
        "mnemonic": args.mnemonic,
        "address": args.address,
        "comp1": args.comp1,
        "comp2": args.comp2,
        "comp3": args.comp3,
        "comp4": args.comp4,
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Icon path: {get_asset_path('tz_recovery.ico')}")
    print(f"Splash path: {get_asset_path('tz_recovery.png')}")

    recovery = PassRecoveryMain(show_ui=not args.noui, params=params)

    if args.noui:
        recovery.start_recovery(params)

    return recovery.run()


if __name__ == "__main__":
    sys.exit(main())
