from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import logging
import hashlib
import unicodedata
import bitcoin
import pysodium
from hashlib import blake2b, pbkdf2_hmac
from src.functions import (
    saltmixer,
    sequenzerwithvsalt,
    sequenzernovsalt,
    component_mixer,
    check,
)

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


class PasswordRecoveryModel:
    """Model for password recovery process"""

    def __init__(self):
        # Core parameters
        self.email: str = ""
        self.mnemonic: str = ""
        self.target_address: str = ""

        # Components and constraints
        self.components = PasswordComponents()
        self.min_length: int = 8
        self.max_length: int = 32

        # Runtime state
        self.best_attempt: Optional[PasswordAttempt] = None
        self.best_distance: float = float("inf")
        self.total_attempts: int = 0
        self.start_time: Optional[datetime] = None
        self._is_running: bool = False

        # Cache for optimization
        self._component_cache: Dict[str, List[str]] = {}
        self._distance_cache: Dict[str, float] = {}

        logger.info("Password Recovery Model initialized")

    def set_parameters(self, email: str, mnemonic: str, address: str) -> None:
        """Set core parameters for recovery"""
        self.email = email
        self.mnemonic = mnemonic
        self.target_address = address
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

    def process_attempt(self, password: str) -> PasswordAttempt:
        """Process a password attempt and return results"""
        try:
            result, address = check(
                password=password,
                email=self.email,
                mnemonic=self.mnemonic,
                address=self.target_address,
            )

            # Calculate distance (you might want to customize this)
            distance = sum(a != b for a, b in zip(address, self.target_address))

            is_improvement = distance < self.best_distance
            if is_improvement:
                self.best_distance = distance
                self.best_attempt = PasswordAttempt(
                    password=password,
                    components=self.components,
                    distance=distance,
                    address=address,
                    timestamp=datetime.now(),
                    is_improvement=is_improvement,
                )
                logger.info(
                    f"New best password found: {password} (distance: {distance})"
                )

            self.total_attempts += 1

            return self.best_attempt

        except Exception as e:
            logger.error(f"Error processing attempt: {str(e)}")
            return PasswordAttempt(
                password=password,
                components=self.components,
                distance=float("inf"),
                address="",
                timestamp=datetime.now(),
                is_improvement=False,
            )

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
        # Implement your specific distance calculation
        if not generated_address or not self.target_address:
            return float("inf")

        # Simple Hamming distance for demonstration
        min_len = min(len(generated_address), len(self.target_address))
        distance = sum(
            a != b
            for a, b in zip(generated_address[:min_len], self.target_address[:min_len])
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
