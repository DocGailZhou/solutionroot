#!/usr/bin/env powershell
<#
.SYNOPSIS
    Comprehensive Data Generation Orchestrator
    
.DESCRIPTION
    Interactive data generation workflow that guides you through:
    1. Generates realistic sales data across all product categories  
    2. Auto-scales and generates supply chain data based on sales volume
    3. Integrates sales patterns with inventory management and procurement
    
    Simply run: .\Run-DataGeneration.ps1
    The script will ask for dates and options with sensible defaults.
    
.EXAMPLE
    .\Run-DataGeneration.ps1
    # Interactive mode with guided prompts and smart defaults
    
.NOTES
    Author: GitHub Copilot
    Date: March 6, 2026
    Requires: Python 3.x with required packages (pandas, numpy, matplotlib)
#>

# No parameters needed - fully interactive!
param()

# Script configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = 'Continue'

# Set UTF-8 encoding for better emoji support
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Color functions for better output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success { Write-ColorOutput Green $args }
function Write-Info { Write-ColorOutput Cyan $args }  
function Write-Warning { Write-ColorOutput Yellow $args }
function Write-Error { Write-ColorOutput Red $args }

# Banner
Write-Host @"
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                        🏢 COMPREHENSIVE DATA GENERATION SUITE 🏢                    ║
║                                                                                      ║
║  🏭 Phase 1: Sales Data Generation (All Product Categories)                         ║
║  📦 Phase 2: Supply Chain Automation (Auto-Scaled to Sales Volume)                  ║
║  🔗 Phase 3: Data Integration & Analytics                                           ║
║                                                                                     ║
║  📊 Generates: Sales → Orders → Inventory → Procurement → Supply Chain Events       ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""

# Validate date format function
function Test-DateFormat {
    param([string]$Date)
    try {
        $parsedDate = [DateTime]::ParseExact($Date, "yyyy-MM-dd", $null)
        return $true
    } catch {
        return $false
    }
}

# Calculate smart defaults (15-month business period: full 2025 + Q1 2026)
$DefaultEndDate = "2026-03-31"
$DefaultStartDate = "2025-01-01"

# Interactive configuration with smart defaults
Write-Info "📅 Business Data Generation Configuration"
Write-Host "   Let's set up your business data simulation with smart defaults!" -ForegroundColor Gray
Write-Host ""

Write-Host "   🎯 Recommended: 15-month business analysis period (full 2025 + Q1 2026)" -ForegroundColor Yellow
Write-Host "   📊 Default period spans seasonal patterns and growth trends" -ForegroundColor Gray
Write-Host ""

# Date range input with defaults
Write-Host "📅 Date Range Setup:" -ForegroundColor Cyan
Write-Host "   Default: $DefaultStartDate to $DefaultEndDate (15 months)" -ForegroundColor Green

$UseDefaults = Read-Host "   Use default dates? (Press Enter for YES, or type 'no')"
if ($UseDefaults -eq "" -or $UseDefaults -eq "Y" -or $UseDefaults -eq "y") {
    $StartDate = $DefaultStartDate
    $EndDate = $DefaultEndDate
    Write-Host "   ✅ Using defaults: $StartDate to $EndDate" -ForegroundColor Green
} else {
    Write-Host "   📝 Custom date range:" -ForegroundColor Yellow
    
    # Get start date
    do {
        $StartDate = Read-Host "   Enter start date (YYYY-MM-DD)"
        if (-not (Test-DateFormat $StartDate)) {
            Write-Warning "   ⚠️  Invalid date format. Please use YYYY-MM-DD format."
            $StartDate = $null
        }
    } while (-not $StartDate)
    
    # Get end date  
    do {
        $EndDate = Read-Host "   Enter end date (YYYY-MM-DD)"
        if (-not (Test-DateFormat $EndDate)) {
            Write-Warning "   ⚠️  Invalid date format. Please use YYYY-MM-DD format."
            $EndDate = $null
        } else {
            # Validate end date is after start date
            $startDt = [DateTime]::ParseExact($StartDate, "yyyy-MM-dd", $null)
            $endDt = [DateTime]::ParseExact($EndDate, "yyyy-MM-dd", $null)
            if ($endDt -le $startDt) {
                Write-Warning "   ⚠️  End date must be after start date."
                $EndDate = $null
            }
        }
    } while (-not $EndDate)
}

Write-Host ""

# Feature options with smart defaults
Write-Host "🚀 Generation Features:" -ForegroundColor Cyan

# Business growth (default: Yes)
$GrowthInput = Read-Host "   Enable business growth patterns? (Press Enter for YES, or type 'no')"
$EnableGrowth = ($GrowthInput -eq "" -or $GrowthInput -eq "Y" -or $GrowthInput -eq "y")

# Analytics graphs (default: Yes)  
$GraphsInput = Read-Host "   Generate analytics graphs? (Press Enter for YES, or type 'no')"
$GenerateGraphs = ($GraphsInput -eq "" -or $GraphsInput -eq "Y" -or $GraphsInput -eq "y")

# Copy data to infra (default: Yes)
$CopyInput = Read-Host "   Copy data to infra/data directory? (Press Enter for YES, or type 'no')"
$CopyData = ($CopyInput -eq "" -or $CopyInput -eq "Y" -or $CopyInput -eq "y" -or $CopyInput -eq "yes")

# Calculate duration
$startDt = [DateTime]::ParseExact($StartDate, "yyyy-MM-dd", $null) 
$endDt = [DateTime]::ParseExact($EndDate, "yyyy-MM-dd", $null)
$duration = ($endDt - $startDt).Days

Write-Host ""
Write-Info "🗓️  Final Configuration:"
Write-Host "   • Start Date: $StartDate" -ForegroundColor White
Write-Host "   • End Date:   $EndDate" -ForegroundColor White  
Write-Host "   • Duration:   $duration days" -ForegroundColor White
Write-Host "   • Growth:     $(if($EnableGrowth) {'Enabled ✅'} else {'Disabled'})" -ForegroundColor White
Write-Host "   • Graphs:     $(if($GenerateGraphs) {'Enabled ✅'} else {'Disabled'})" -ForegroundColor White
Write-Host "   • Copy Data:  $(if($CopyData) {'Enabled ✅'} else {'Disabled'})" -ForegroundColor White
Write-Host ""

Write-Host "🚀 Starting data generation..." -ForegroundColor Green
Write-Host ""

# Change to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

try {
    # Phase 1: Sales Data Generation
    Write-Host "🏭 PHASE 1: SALES DATA GENERATION" -ForegroundColor Green -BackgroundColor Black
    Write-Host "═" * 80 -ForegroundColor Green
    
    Write-Info "   Generating comprehensive sales data for all product categories..."
    Write-Info "   • 🏕️  Camping products (Microsoft Fabric channel)"
    Write-Info "   • 🍳 Kitchen products (Azure Databricks channel)"  
    Write-Info "   • ⛷️  Ski products (Winter Sports channel)"
    Write-Host ""
    
    # Build sales command
    $SalesArgs = @(
        "main_generate_sales.py"
        "-s", $StartDate
        "-e", $EndDate
    )
    
    if ($EnableGrowth) { $SalesArgs += "--enable-growth" }
    if ($GenerateGraphs) { 
        $SalesArgs += "--graph"
        $SalesArgs += "--no-display"  # Prevent GUI windows in automation
    }
    if ($CopyData) { $SalesArgs += "--copydata" }
    
    Write-Host "   Executing: python $($SalesArgs -join ' ')" -ForegroundColor Gray
    Write-Host ""
    
    # Set UTF-8 encoding for Python output
    $env:PYTHONIOENCODING = "utf-8"
    
    # Execute sales generation
    $SalesResult = & python @SalesArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Sales data generation failed with exit code $LASTEXITCODE"
    }
    
    Write-Host ""
    Write-Success "✅ Phase 1 completed successfully!"
    Write-Host ""
    
    # Phase 2: Supply Chain Data Generation  
    Write-Host "📦 PHASE 2: SUPPLY CHAIN DATA GENERATION (AUTO-SCALED)" -ForegroundColor Blue -BackgroundColor Black
    Write-Host "═" * 80 -ForegroundColor Blue
    
    Write-Info "   Auto-scaling supply chain parameters based on sales volume..."
    Write-Info "   • 🏭 Suppliers & product-supplier relationships"
    Write-Info "   • 📦 Inventory levels based on sales velocity"
    Write-Info "   • 📋 Purchase orders scaled to sales demand"
    Write-Info "   • 🔄 Inventory transactions (2-3x sales volume)"
    Write-Info "   • 🚨 Supply chain risk events & scenarios"
    Write-Host ""
    
    # Build supply chain command with auto-scale
    $SupplyArgs = @(
        "main_generate_supplychain.py"
        "-s", $StartDate
        "-e", $EndDate
        "--auto-scale"
    )
    
    if ($GenerateGraphs) { 
        $SupplyArgs += "--graph"
        $SupplyArgs += "--no-display"  # Prevent GUI windows in automation
    }
    if ($CopyData) { $SupplyArgs += "--copydata" }
    
    Write-Host "   Executing: python $($SupplyArgs -join ' ')" -ForegroundColor Gray
    Write-Host ""
    
    # Ensure UTF-8 encoding for supply chain generation
    $env:PYTHONIOENCODING = "utf-8"
    
    # Execute supply chain generation
    $SupplyResult = & python @SupplyArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Supply chain data generation failed with exit code $LASTEXITCODE"
    }
    
    Write-Host ""
    Write-Success "✅ Phase 2 completed successfully!"
    Write-Host ""
    
    # Phase 3: Integration Summary
    Write-Host "🔗 PHASE 3: DATA INTEGRATION SUMMARY" -ForegroundColor Magenta -BackgroundColor Black  
    Write-Host "═" * 80 -ForegroundColor Magenta
    
    # Display summary information
    Write-Info "   📊 Generated comprehensive business dataset:"
    Write-Host ""
    
    # Check if summary files exist and display key metrics
    $SalesSummary = "output\sample_sales_data_summary.md"
    $SupplySummary = "output\sample_supplychain_data_summary.md" 
    
    if (Test-Path $SalesSummary) {
        $SalesContent = Get-Content $SalesSummary -Raw
        if ($SalesContent -match "Total Orders.*?(\d{1,3}(?:,\d{3})*)" ) {
            Write-Host "   🛒 Total Sales Orders: $($Matches[1])" -ForegroundColor White
        }
        if ($SalesContent -match "Order Lines.*?(\d{1,3}(?:,\d{3})*)" ) {
            Write-Host "   📝 Total Line Items: $($Matches[1])" -ForegroundColor White
        }
        if ($SalesContent -match "Total Sales Value.*?\`$(\d+(?:,\d{3})*(?:\.\d{2})?)" ) {
            Write-Host "   💰 Total Sales Value: `$$($Matches[1])" -ForegroundColor White
        }
    }
    
    if (Test-Path $SupplySummary) {
        $SupplyContent = Get-Content $SupplySummary -Raw  
        if ($SupplyContent -match "Purchase Orders.*?(\d+)" ) {
            Write-Host "   📋 Purchase Orders: $($Matches[1])" -ForegroundColor White
        }
        if ($SupplyContent -match "Inventory Transactions.*?(\d{1,3}(?:,\d{3})*)" ) {
            Write-Host "   🔄 Inventory Transactions: $($Matches[1])" -ForegroundColor White
        }
        if ($SupplyContent -match "Suppliers.*?(\d+)" ) {
            Write-Host "   🏭 Suppliers: $($Matches[1])" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Info "   📁 Output locations:"
    Write-Host "     • Sales data: output/[camping|kitchen|ski]/" -ForegroundColor Gray
    Write-Host "     • Supply chain: output/[supplychain|inventory]/" -ForegroundColor Gray  
    Write-Host "     • Summary reports: output/sample_*_summary.md" -ForegroundColor Gray
    
    if ($GenerateGraphs) {
        Write-Host "     • Analytics graphs: output/*.png" -ForegroundColor Gray
    }
    
    if ($CopyData) {
        Write-Host "     • Copied to: ../infra/data/" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "🎉 DATA GENERATION COMPLETED SUCCESSFULLY!" -ForegroundColor Green -BackgroundColor Black
    Write-Host "═" * 80 -ForegroundColor Green
    Write-Host ""
    Write-Success "✨ Your integrated business dataset is ready for analysis!"
    Write-Host "   Duration: $duration days | Sales → Supply Chain → Analytics" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR DURING GENERATION" -ForegroundColor Red -BackgroundColor Black  
    Write-Host "═" * 80 -ForegroundColor Red
    Write-Error "   $($_.Exception.Message)"
    Write-Host ""
    Write-Warning "💡 Troubleshooting tips:"
    Write-Host "   • Ensure Python 3.x is installed and in PATH"
    Write-Host "   • Install required packages: pip install pandas numpy matplotlib" 
    Write-Host "   • Check input files exist in input/ directory"
    Write-Host "   • Verify date format (YYYY-MM-DD)"
    Write-Host ""
    exit 1
}