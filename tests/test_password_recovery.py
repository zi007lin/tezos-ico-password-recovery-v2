import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
# This is the critical fix - we need to add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import with the correct paths
from src.models.password_recovery import (
    PasswordRecoveryModel,
    PasswordComponents,
    PasswordAttempt,
)

# Import the check function with the correct path
from src.functions import check


class TestPasswordRecovery(unittest.TestCase):
    """Test cases for the PasswordRecoveryModel class with predictable results."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a test configuration with known values
        self.email = "test@example.com"
        self.mnemonic = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14"
        self.address = "tz1testAddressForUnitTestingPurposes"

        # Create password components with known values
        self.components = PasswordComponents(
            comp1="test", comp2="password", comp3="123", comp4="!"
        )

        # Create a model instance with the correct parameters
        # Adjust this based on the actual PasswordRecoveryModel constructor
        self.model = PasswordRecoveryModel()

        # Set the model properties after initialization
        self.model.email = self.email
        self.model.mnemonic = self.mnemonic
        self.model.address = self.address
        self.model.components = self.components

        # Store the correct password for testing
        self.correct_password = "testpassword123!"

    @patch("src.functions.check")
    def test_password_check_correct(self, mock_check):
        """Test that a correct password is identified."""
        # Configure the mock to return True for the correct password
        mock_check.return_value = True

        # Create a password attempt with the correct password
        attempt = PasswordAttempt(
            password=self.correct_password, score=100, components=self.components
        )

        # Check if the password is correct
        result = self.model.check_password(attempt)

        # Assert that the result is True
        self.assertTrue(result)
        # Verify that the check function was called with the correct arguments
        mock_check.assert_called_once_with(
            self.email, self.mnemonic, self.correct_password, self.address
        )

    @patch("src.functions.check")
    def test_password_check_incorrect(self, mock_check):
        """Test that an incorrect password is identified."""
        # Configure the mock to return False for incorrect passwords
        mock_check.return_value = False

        # Create a password attempt with an incorrect password
        incorrect_password = "wrongpassword"
        attempt = PasswordAttempt(
            password=incorrect_password, score=50, components=self.components
        )

        # Check if the password is correct
        result = self.model.check_password(attempt)

        # Assert that the result is False
        self.assertFalse(result)
        # Verify that the check function was called with the correct arguments
        mock_check.assert_called_once_with(
            self.email, self.mnemonic, incorrect_password, self.address
        )

    def test_generate_password_combinations(self):
        """Test that password combinations are generated correctly."""
        # Set up components with predictable values
        components = PasswordComponents(comp1="A", comp2="B", comp3="C", comp4="D")

        # Generate a limited set of combinations for testing
        combinations = self.model.generate_combinations(components, max_combinations=10)

        # Assert that combinations were generated
        self.assertTrue(len(combinations) > 0)
        self.assertLessEqual(len(combinations), 10)

        # Check that the combinations contain the components
        for combo in combinations:
            # Each combination should contain at least one of the components
            self.assertTrue(
                "A" in combo.password
                or "B" in combo.password
                or "C" in combo.password
                or "D" in combo.password
            )

    def test_score_calculation(self):
        """Test that password scores are calculated correctly."""
        # Create password attempts with known characteristics
        attempts = [
            PasswordAttempt(
                password="testpassword", score=0, components=self.components
            ),
            PasswordAttempt(password="test123", score=0, components=self.components),
            PasswordAttempt(password="password!", score=0, components=self.components),
        ]

        # Calculate scores
        scored_attempts = self.model.score_attempts(attempts)

        # Verify that scores were assigned
        for attempt in scored_attempts:
            self.assertGreaterEqual(attempt.score, 0)

        # Verify that attempts are sorted by score (highest first)
        for i in range(1, len(scored_attempts)):
            self.assertGreaterEqual(
                scored_attempts[i - 1].score, scored_attempts[i].score
            )

    @patch("src.functions.check")
    def test_recovery_process(self, mock_check):
        """Test the complete password recovery process with a mock."""

        # Configure the mock to return True only for the correct password
        def check_side_effect(email, mnemonic, password, address):
            return password == self.correct_password

        mock_check.side_effect = check_side_effect

        # Create a simplified version of the recovery process
        def simplified_recovery():
            # Generate some test password attempts
            attempts = [
                PasswordAttempt(
                    password="wrongpassword1", score=0, components=self.components
                ),
                PasswordAttempt(
                    password=self.correct_password, score=0, components=self.components
                ),
                PasswordAttempt(
                    password="wrongpassword2", score=0, components=self.components
                ),
            ]

            # Score the attempts
            scored_attempts = self.model.score_attempts(attempts)

            # Check each password until we find the correct one
            for attempt in scored_attempts:
                if self.model.check_password(attempt):
                    return attempt

            return None

        # Run the recovery process
        result = simplified_recovery()

        # Assert that the correct password was found
        self.assertIsNotNone(result)
        self.assertEqual(result.password, self.correct_password)

    def test_component_permutations(self):
        """Test that component permutations are generated correctly."""
        # Set up components with predictable values
        components = PasswordComponents(comp1="A", comp2="B", comp3="", comp4="")

        # Generate permutations
        permutations = self.model.generate_component_permutations(components)

        # Expected permutations: A, B, AB, BA
        expected = ["A", "B", "AB", "BA"]

        # Convert PasswordAttempt objects to strings for comparison
        actual = [p.password for p in permutations]

        # Assert that all expected permutations are present
        for exp in expected:
            self.assertIn(exp, actual)

        # Assert that the number of permutations is correct
        self.assertEqual(len(actual), len(expected))


if __name__ == "__main__":
    unittest.main()
