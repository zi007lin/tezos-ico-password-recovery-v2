import time
from PyQt5.QtCore import QObject, pyqtSignal


class PasswordRecoveryModel(QObject):
    check_signal = pyqtSignal(tuple)  # Signal for check results

    def __init__(self, signal_rate=15):
        super().__init__()
        self.signal_rate = signal_rate  # Signals per second
        self.last_signal_time = 0

    def process_attempt(self, password):
        try:
            # Run the check
            result = check(password, self.email, self.mnemonic, self.address)

            # Check if we should emit signal based on rate
            current_time = time.time()
            if current_time - self.last_signal_time >= (1.0 / self.signal_rate):
                self.check_signal.emit(result)
                self.last_signal_time = current_time

            return result

        except Exception as e:
            logger.error(f"Error in process_attempt: {str(e)}")
            return None

    def set_signal_rate(self, rate):
        """Update signal rate (signals per second)"""
        self.signal_rate = max(1, min(rate, 60))  # Limit between 1-60 Hz
