param(
    [string]$Path = (Get-Location)
)

# Function to activate a virtual environment
function Activate-Venv {
    param([string]$VenvPath)

    if (Test-Path "$VenvPath\Scripts\Activate.ps1") {
        Write-Host "Activating virtual environment at: $VenvPath"
        & "$VenvPath\Scripts\Activate.ps1"
    } else {
        Write-Host "No virtual environment found at: $VenvPath"
    }
}

# Check if the given path contains .venv
$venvPath = Join-Path $Path ".venv"

if (Test-Path $venvPath) {
    Activate-Venv $venvPath
} else {
    # Look for requirements.txt in the current directory
    $requirementsPath = Join-Path $Path "requirements.txt"
    if (Test-Path $requirementsPath) {
        $dirName = (Get-Item $Path).Name
        $newVenvPath = Join-Path $Path $dirName

        Write-Host "Creating new virtual environment named '$dirName'..."

        # Create a virtual environment
        python -m venv $newVenvPath
        Write-Host "New virtual environment created at: $newVenvPath"

        # Install dependencies from requirements.txt
        & "$newVenvPath\Scripts\Activate.ps1" 
        pip install -r $requirementsPath

        Write-Host "Dependencies installed successfully!"
    } else {
        Write-Host "Error: No .venv or requirements.txt found in the specified directory."
    }
}
