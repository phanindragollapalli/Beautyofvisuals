param(
    [string]$Project = "MOI",

    [string]$Scene = "SpinnerIntuition",

    [ValidateSet("l", "m", "h")]
    [string]$Quality = "h",

    [switch]$Preview
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Join-Path $scriptDir $Project
$projectScript = Join-Path $projectDir "render.ps1"
$projectMain = Join-Path $projectDir "main.py"

if (-not (Test-Path $projectDir)) {
    throw "Project folder not found: $projectDir"
}

if (Test-Path $projectScript) {
    $args = @(
        "-ExecutionPolicy", "Bypass",
        "-File", $projectScript,
        "-Scene", $Scene,
        "-Quality", $Quality
    )

    if ($Preview) {
        $args += "-Preview"
    }

    & powershell @args
    return
}

if (-not (Test-Path $projectMain)) {
    throw "No render.ps1 or main.py found in project folder: $projectDir"
}

$projectRenderArgs = @("-m", "manim")
if ($Preview) {
    $projectRenderArgs += "-p"
}
$projectRenderArgs += "-q$Quality"

Push-Location $projectDir
try {
    if ($Scene -eq "all") {
        & python @projectRenderArgs "-a" "main.py"
    } else {
        & python @projectRenderArgs "main.py" $Scene
    }
} finally {
    Pop-Location
}
