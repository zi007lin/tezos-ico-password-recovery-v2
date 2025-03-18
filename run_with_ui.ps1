# PowerShell script to run the Password Recovery Tool with UI

# Set parameters
$email = "daniel.silvers@gmail.com"
$mnemonic = "embark bargain mention around employ twist sausage daring parent ribbon switch feature fee despair prefer"
$address = "tz1axXoWqcKhK9C64yvE1Yd2PUPPnWLAQtxh"
$comp1 = ""
$comp2 = ""
$comp3 = ""
$comp4 = ""

# Display parameters
Write-Host "Starting Password Recovery Tool with parameters:"
Write-Host "Email: $email"
Write-Host "Mnemonic: $mnemonic"
Write-Host "Address: $address"
Write-Host "Comp1: $comp1"
Write-Host "Comp2: $comp2"
Write-Host "Comp3: $comp3"
Write-Host "Comp4: $comp4"

# Get the current directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir"

# Correct path to the Python script
$pythonScript = Join-Path -Path $currentDir -ChildPath "src\PassRecoveryMain.py"
Write-Host "Python script path: $pythonScript"

# Check if the Python script exists
if (-not (Test-Path $pythonScript)) {
    Write-Host "Error: Python script not found at $pythonScript" -ForegroundColor Red
    exit 1
}

# Build command arguments
$arguments = @("$pythonScript", "--email", "$email", "--mnemonic", "$mnemonic", "--address", "$address")

# Only add comp parameters if they have values
if ($comp1) { $arguments += "--comp1"; $arguments += "$comp1" }
if ($comp2) { $arguments += "--comp2"; $arguments += "$comp2" }
if ($comp3) { $arguments += "--comp3"; $arguments += "$comp3" }
if ($comp4) { $arguments += "--comp4"; $arguments += "$comp4" }

# Run the Python script with parameters
Write-Host "Running command: python $arguments"
python $arguments 