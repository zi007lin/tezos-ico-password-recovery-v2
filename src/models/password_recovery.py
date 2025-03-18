from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import logging
import hashlib
import unicodedata
import bitcoin
import pysodium
from hashlib import blake2b, pbkdf2_hmac
from functions import (
    saltmixer,
    sequenzerwithvsalt,
    sequenzernovsalt,
    component_mixer,
    check,
)
import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal
import time

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logger = logging.getLogger("TezosPasswordFinder")


@dataclass
class PasswordComponents:
    """Data structure for password components"""

    comp1: str = ""
    comp2: str = ""
    comp3: str = ""
    comp4: str = ""

    def to_list(self) -> List[str]:
        return [self.comp1, self.comp2, self.comp3, self.comp4]


@dataclass
class PasswordAttempt:
    """Data structure for a password attempt"""

    password: str
    components: PasswordComponents
    distance: float
    address: str
    timestamp: datetime
    is_improvement: bool = False


class PasswordRecoveryModel(QObject):
    check_signal = pyqtSignal(tuple)  # Signal for check results

    def __init__(self, signal_rate=15):
        super().__init__()
        self.signal_rate = signal_rate
        self.last_signal_time = 0
        self.email = ""
        self.mnemonic = ""
        self.address = ""
        self.components = PasswordComponents()

        # Initialize caches
        self._component_cache = {}
        self._distance_cache = {}
        self._is_running = False
        self.start_time = None
        self.total_attempts = 0
        self.best_distance = float("inf")
        self.best_attempt = None

    def process_attempt(self, password):
        try:
            # Run the check
            found_it, pwd, current_distance, best_distance, best_password = check(
                password, self.email, self.mnemonic, self.address
            )

            # Create attempt object with all required fields
            attempt = PasswordAttempt(
                password=password,
                components=self.components,  # Current components
                distance=current_distance,
                address=self.address,
                timestamp=datetime.now(),
                is_improvement=(current_distance < self.best_distance),
            )

            # Check if we should emit signal based on rate
            current_time = time.time()
            if current_time - self.last_signal_time >= (1.0 / self.signal_rate):
                self.check_signal.emit(
                    (found_it, pwd, current_distance, best_distance, best_password)
                )
                self.last_signal_time = current_time

            return attempt

        except Exception as e:
            logger.error(f"Error in process_attempt: {str(e)}")
            return None

    def set_signal_rate(self, rate):
        """Update signal rate (signals per second)"""
        self.signal_rate = max(1, min(rate, 60))  # Limit between 1-60 Hz

    def set_parameters(self, email: str, mnemonic: str, address: str) -> None:
        """Set core parameters for recovery"""
        self.email = email
        self.mnemonic = mnemonic
        self.address = address
        logger.debug(f"Parameters set - Target address: {address[:8]}...")

    def set_components(self, comp1: str, comp2: str, comp3: str, comp4: str) -> None:
        """Set password components"""
        self.components = PasswordComponents(comp1, comp2, comp3, comp4)
        logger.debug("Components updated")
        self._clear_cache()

    def start_session(self) -> None:
        """Start a new recovery session"""
        import time

        self.start_time = time.time()
        self.total_attempts = 0
        self.best_distance = float("inf")
        self.best_attempt = None
        self._is_running = True
        self._clear_cache()
        logger.info("New session started")

    def get_statistics(self) -> Dict:
        """Get current statistics"""
        if not self.start_time:
            return {}

        import time

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        attempts_per_second = (
            self.total_attempts / elapsed_time if elapsed_time > 0 else 0
        )

        return {
            "total_attempts": self.total_attempts,
            "best_distance": self.best_distance,
            "attempts_per_second": attempts_per_second,
            "elapsed_time": elapsed_time,
            "best_attempt": self.best_attempt,
        }

    def _generate_address(self, password: str) -> str:
        """Generate address from password"""
        # Implementation of your specific address generation logic
        salt = self.email.lower().encode("utf-8")
        hashed = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), salt, 2048, dklen=64
        )
        return hashed.hex()

    def _calculate_distance(self, generated_address: str) -> float:
        """Calculate distance between generated and target address"""
        if not generated_address or not self.address:
            return float("inf")

        # Skip the common prefix (tz1) in the comparison
        TEZOS_PREFIX = "tz1"
        if not generated_address.startswith(
            TEZOS_PREFIX
        ) or not self.address.startswith(TEZOS_PREFIX):
            return float("inf")

        # Compare only the part after the prefix
        gen_addr = generated_address[len(TEZOS_PREFIX) :]
        target_addr = self.address[len(TEZOS_PREFIX) :]

        # Log the addresses without prefix
        logger.info(f"Generated address (no prefix): {gen_addr}")
        logger.info(f"Target address (no prefix):    {target_addr}")

        # Calculate meaningful distance based on matching characters
        common_prefix_length = 0
        for i, (a, b) in enumerate(zip(gen_addr, target_addr)):
            if a != b:
                logger.info(f"First mismatch at position {i}: '{a}' vs '{b}'")
                break
            common_prefix_length += 1

        distance = 1.0 / (common_prefix_length + 0.1)
        logger.info(
            f"Common prefix length: {common_prefix_length}, Distance: {distance:.2f}"
        )

        return distance

    def _clear_cache(self) -> None:
        """Clear optimization caches"""
        self._component_cache.clear()
        self._distance_cache.clear()
        logger.debug("Caches cleared")

    def generate_password_candidates(self) -> List[str]:
        """Generate password candidates based on components"""
        try:
            # Use the existing functions to generate candidates
            salt_list = saltmixer(self.components.comp1, 2, True, False)

            # Generate sequences
            sequ_with_vsalt = sequenzerwithvsalt(1, 1, 1, 1, 1, 1, 1)
            sequ_no_vsalt = sequenzernovsalt(1, 1, 1, 1, 1, 1)

            # Mix components
            candidates = []
            count = 0
            used = 0

            candidates_count, candidates_used, pwd_list = component_mixer(
                [salt_list, sequ_with_vsalt, sequ_no_vsalt],
                min_char_num=8,
                max_char_num=50,
                candidate_count=count,
                candidate_used=used,
                window=None,
                pwd_list=candidates,
            )

            return pwd_list

        except Exception as e:
            logger.error(f"Error generating candidates: {str(e)}")
            return []
