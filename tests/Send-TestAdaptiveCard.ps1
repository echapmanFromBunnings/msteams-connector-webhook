<#
.SYNOPSIS
    Sends a test Adaptive Card to a real Microsoft Teams / Power Automate webhook.

.DESCRIPTION
    Uses send_adaptive_card.py to post a test card. Useful for validating that
    your Power Automate workflow URL and permissions are configured correctly.

.PARAMETER WebhookUrl
    The IncomingWebhook URL from your Power Automate "Post card in a chat or channel" workflow.

.PARAMETER Title
    Title for the test card.

.PARAMETER Message
    Message body for the test card.
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$WebhookUrl,

    [string]$Title = "Test Adaptive Card",

    [string]$Message = "This is a test message from the msteams-connector-webhook validation script."
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $repoRoot "send_adaptive_card.py"

if (-not (Test-Path $scriptPath)) {
    throw "send_adaptive_card.py not found at $scriptPath"
}

if ($WebhookUrl -notmatch "https?://") {
    throw "WebhookUrl must be a valid HTTPS URL"
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw "Python is required to send the test card."
}

if ($PSCmdlet.ShouldProcess($WebhookUrl, "Send test Adaptive Card")) {
    Write-Host "Sending test card to $WebhookUrl ..."
    & $python.Source $scriptPath $WebhookUrl $Title $Message
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to send test card (exit code $LASTEXITCODE)"
    }
    Write-Host "Test card sent successfully." -ForegroundColor Green
}
