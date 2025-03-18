import unicodedata
import bitcoin
import pysodium
from hashlib import blake2b
import itertools
import time
import re
import os
from hashlib import pbkdf2_hmac
import logging
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

# Set up logging
logger = logging.getLogger("TezosPasswordFinder")
logger.setLevel(logging.INFO)


def saltmixer(var, salt_num, salt_n, salt_char_multi):
    import itertools

    salt_list = []
    salt = int(salt_num)
    output1 = ""
    z = 0

    if salt_n == True:
        salt_list.append("")
    for z in 1, 2:
        for subset in itertools.product(var):
            for x in subset:
                output1 = output1 + x
            salt_list.append(output1)
            output1 = ""
        z = z + 1
        if z > salt:
            break
        for subset in itertools.product(var, var):
            for x in subset:
                output1 = output1 + x
            if salt_char_multi == False:
                if len(output1) != len(set(output1)):
                    output1 = ""
                    continue
            salt_list.append(output1)
            output1 = ""
        z = z + 1
        if z > salt:
            break
        for subset in itertools.product(var, var, var):
            for x in subset:
                output1 = output1 + x
            if salt_char_multi == False:
                if len(output1) != len(set(output1)):
                    output1 = ""
                    continue
            salt_list.append(output1)
            output1 = ""
        z = z + 1
        if z > salt:
            break
        for subset in itertools.product(var, var, var, var):
            for x in subset:
                output1 = output1 + x
            if salt_char_multi == False:
                if len(output1) != len(set(output1)):
                    output1 = ""
                    continue
            salt_list.append(output1)
            output1 = ""
        z = z + 1
        if z > salt:
            break

    return salt_list


def sequenzerwithvsalt(L, V, W, X, Y, Z, E):
    import itertools

    sequ = []
    output1 = ""
    comp_count = V + W + X + Y + Z
    sequ_count = 0

    if L == 1:
        output1 = "LV"
    else:
        output1 = "V"
    if comp_count == 5:
        for subset in itertools.product("WXYZ", "WXYZ", "WXYZ", "WXYZ"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"
            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""
    elif comp_count == 4:
        for subset in itertools.product("WXZ", "WXZ", "WXZ"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"
            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""
    elif comp_count == 3:
        for subset in itertools.product("WZ", "WZ"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"
            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""
    else:
        for subset in itertools.product("Z"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"
            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""
    sequ_with_vsalt = sequ

    return sequ_with_vsalt


def sequenzernovsalt(L, V, W, X, Y, E):

    sequ = []
    output1 = ""
    comp_count = V + W + X + Y
    sequ_count = 0

    if L == 1:
        output1 = "L"
    else:
        output1 = ""
    if comp_count == 4:
        for subset in itertools.product("WXY", "WXY", "WXY"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"
            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                output1 = ""
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""
    elif comp_count == 3:
        for subset in itertools.product("WX", "WX"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"

            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                output1 = ""
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""

    elif comp_count == 2:
        for subset in itertools.product("W"):
            if L == 0:
                output1 = "V"
            else:
                output1 = "LV"
            for p in subset:
                output1 = output1 + p
            if len(output1) != len(set(output1)):
                output1 = ""
                continue
            if E == 1:
                output1 = output1 + "E"
            sequ.append(output1)
            sequ_count += 1
            output1 = ""

    else:
        if L == 0:
            output1 = "V"
        else:
            output1 = "LV"

        if E == 1:
            output1 = output1 + "E"
        sequ.append(output1)
        sequ_count += 1
        output1 = ""

    sequ_no_vsalt = sequ
    return sequ_no_vsalt


def component_mixer(
    parts, min_char_num, max_char_num, candidate_count, candidate_used, window, pwd_list
):

    for subset in itertools.product(*parts):

        pwd_candidate = ""
        candidate_count += 1
        for x in subset:
            pwd_candidate = pwd_candidate + x
        if len(pwd_candidate) < min_char_num or len(pwd_candidate) > max_char_num:
            continue

        candidate_used += 1
        pwd_list.append(pwd_candidate)
        # window.ui.lcdNumber_used.display(candidate_used)
        # window.ui.lcdNumber.display(candidate_count)

    return candidate_count, candidate_used, pwd_list


def calculate_weighted_distance(generated: str, target: str) -> float:
    """
    Calculate weighted Levenshtein distance between generated and target addresses.
    Gives more weight to:
    1. Matching characters at the start (more likely to be correct)
    2. Matching numbers (less common in addresses)
    3. Matching case (uppercase/lowercase differences are significant)
    """
    if not generated or not target:
        return float("inf")

    total_weight = 0
    max_length = max(len(generated), len(target))

    # Store detailed distance info for logging
    distance_details = []

    # Compare characters with position-based weights
    for i in range(max_length):
        if i >= len(generated) or i >= len(target):
            # Missing character penalty
            total_weight += 1.0
            distance_details.append(f"Pos {i}: Missing char (+1.0)")
            continue

        if generated[i] != target[i]:
            # Position-based weights (earlier positions matter more)
            position_weight = 1.0 - (i / max_length) * 0.5

            # Character type weights
            if generated[i].isdigit() or target[i].isdigit():
                # Numbers are less common, so mismatches are more significant
                char_weight = 1.5
            elif generated[i].isupper() or target[i].isupper():
                # Case differences are significant
                char_weight = 1.2
            else:
                char_weight = 1.0

            weight = position_weight * char_weight
            total_weight += weight
            distance_details.append(
                f"Pos {i}: '{generated[i]}' ≠ '{target[i]}' "
                f"(pos_weight={position_weight:.2f}, char_weight={char_weight:.1f}, total={weight:.2f})"
            )
        else:
            distance_details.append(
                f"Pos {i}: '{generated[i]}' = '{target[i]}' (match)"
            )

    return round(total_weight, 2), distance_details


def calculate_char_distance(generated: str, target: str) -> float:
    """Calculate distance between two Base58 characters"""
    BASE58_CHARS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    try:
        pos1 = BASE58_CHARS.index(generated)
        pos2 = BASE58_CHARS.index(target)
        direct_distance = abs(pos1 - pos2)
        wrap_distance = 58 - direct_distance
        return min(direct_distance, wrap_distance) / 58.0
    except ValueError:
        return 1.0


def check(password, email, mnemonic, address, iters=2048):
    try:
        # Log all components with debug info
        logger.info("\nTrying password combination:")
        logger.info(f"Full password: '{password}'")

        # Convert mnemonic to bytes if it's a string
        mnemonic_bytes = mnemonic.encode("utf8")

        # Normalize inputs
        salt = unicodedata.normalize("NFKD", (email + password)).encode("utf8")

        # Generate seed using PBKDF2
        seed = pbkdf2_hmac(
            hash_name="sha512",
            password=mnemonic_bytes,
            salt=b"mnemonic" + salt,
            iterations=iters,
        )

        # Generate Ed25519 key pair
        pk, sk = pysodium.crypto_sign_seed_keypair(seed[0:32])

        # Generate public key hash using BLAKE2b
        h = blake2b(digest_size=20)
        h.update(pk)
        pkh = h.digest()

        # Generate Tezos address
        quick_address = bitcoin.bin_to_b58check(pkh, magicbyte=0)
        quick_address = "tz1" + quick_address[1:]

        # Find matching prefix (frozen characters)
        start_pos = 3  # Skip "tz1"
        match_length = 0

        for i in range(start_pos, min(len(quick_address), len(address))):
            if quick_address[i] == address[i]:
                match_length += 1
            else:
                break

        # Calculate weighted distance for non-frozen part
        current_distance = 0
        for i in range(start_pos + match_length, len(address)):
            position_weight = (
                1.0
                - (
                    (i - start_pos - match_length)
                    / (len(address) - start_pos - match_length)
                )
                * 0.5
            )
            char_distance = calculate_char_distance(quick_address[i], address[i])
            current_distance += char_distance * position_weight

        # Store best distance if not exists
        if not hasattr(check, "best_distance"):
            check.best_distance = float("inf")
            check.best_password = None

        # Update best distance if better
        if current_distance < check.best_distance:
            check.best_distance = current_distance
            check.best_password = password
            print(f"\nImprovement found!")
            print(f"Last tried: {password}")
            print(f"Frozen prefix: {address[:start_pos + match_length]}")
            print(f"Next target: '{address[start_pos + match_length]}'")
            print(f"Current distance: {current_distance:.4f}")
            print(f"Best distance: {check.best_distance:.4f}")
            if check.best_password:
                print(f"Best password: {check.best_password}")
            print("-" * 40)

        if address == quick_address:
            found_it = "True"
            print("\nFOUND IT!")
            print(f"Password: {password}")
            with open("password.lst", "a") as z:
                z.write(password + "\n")
        else:
            found_it = "False"

        # Return tuple with all necessary info
        return (
            found_it,
            password,
            current_distance,
            check.best_distance,
            check.best_password,
        )

    except Exception as e:
        logger.error(f"Error in check function: {str(e)}")
        return ("False", "", float("inf"), float("inf"), None)


def pwd_len(
    lsalt_lst,
    esalt_lst,
    vsalt_lst,
    comp1_list,
    comp2_list,
    comp3_list,
    comp4_list,
    window,
    W,
    X,
    Y,
    Z,
):
    lls = len(lsalt_lst)
    if lls == 0:
        lls = 1
    les = len(esalt_lst)
    if les == 0:
        les = 1
    lvs = len(vsalt_lst)
    if lvs == 0:
        lvs = 1
    lc1 = len(comp1_list)
    if lc1 == 0:
        lc1 = 1
    lc2 = len(comp2_list)
    if lc2 == 0:
        lc2 = 1
    lc3 = len(comp3_list)
    if lc3 == 0:
        lc3 = 1
    lc4 = len(comp4_list)
    if lc4 == 0:
        lc4 = 1

    var_part = W + X + Y + Z
    var_multi = 1
    i = 1
    while i <= var_part:
        var_multi = var_multi * i
        i += 1

    total_passwords = lls * lc1 * var_multi * lc2 * lc3 * lc4 * lvs * les
    return total_passwords


def comp_create(
    chars,
    capitalize_first,
    capitalize_each,
    capitalize_all,
    comp_min_char,
    comp_max_char,
    comp_repeat_char,
):
    count = 0
    char_len = int(comp_max_char)
    comp_min_char = int(comp_min_char)
    comp_repeat_char = int(comp_repeat_char)
    chunk_size = 1024 * 1024 * 256

    comp_part_lst = []
    if char_len >= len(chars):
        char_len = len(chars)

    for i in range(1, char_len + 1):
        for comp in itertools.product(chars, repeat=i):
            comp = "".join(comp)
            length = len(comp)
            word = [item[0] for item in re.findall(r"((\w)\2*)", comp)]

            valid_word = True
            letter_count = 0
            for letters in word:
                letter_count += 1
                if len(letters) > comp_repeat_char:
                    valid_word = False
                    break
            if letter_count <= (length / 2) and valid_word == True:
                valid_word = False

            if valid_word == True and length >= comp_min_char:
                count = count + 1
                comp_part_lst.append(comp)

                if (
                    valid_word == True
                    and capitalize_first == True
                    and capitalize_each == False
                ):
                    count += 1
                    comp_part_lst.append(comp.title())

                if valid_word == True and capitalize_each == True:
                    for n in range(1, len(comp)):
                        count += 1
                        y = "".join([comp[:n], comp[n].upper(), comp[n + 1 :]])
                        comp_part_lst.append(y)

                if valid_word == True and capitalize_all == True:
                    count += 1
                    comp_part_lst.append(comp.upper())

    return comp_part_lst


class PassRecoveryWindow(QtWidgets.QMainWindow):
    addressGenerated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.addressGenerated.connect(self.updateGeneratedAddressLabel)

    def setup_ui(self):
        self.generatedAddressLabel = QtWidgets.QLabel("Generated Address: None")
        # Add the label to your layout
        # self.layout.addWidget(self.generatedAddressLabel)

    def updateGeneratedAddressLabel(self, address):
        self.generatedAddressLabel.setText(f"Generated Address: {address}")

    def some_method(self):
        # Emit the signal with the generated address
        quick_address = "some_generated_address"
        self.addressGenerated.emit(quick_address)
