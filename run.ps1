# Launch Focus: .\focus_agent\run.ps1 (works from any directory).
$pkg = Split-Path $PSScriptRoot -Leaf
$root = Split-Path $PSScriptRoot -Parent

# Python: $env:FOCUS_PYTHON, else the signed python.org 3.14 install (Smart App Control blocks
# unsigned venv interpreters), else whatever `python` is on PATH.
$signed = "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe"
$py = if ($env:FOCUS_PYTHON) { $env:FOCUS_PYTHON } elseif (Test-Path $signed) { $signed } else { "python" }

# Optional extra site-packages (default: a .venv next to the package). Added with site.addsitedir,
# not PYTHONPATH, so its .pth files run; the SDK's pywin32 dependency needs them.
$site = if ($env:FOCUS_SITE_PACKAGES) { $env:FOCUS_SITE_PACKAGES } else { Join-Path $root ".venv\Lib\site-packages" }

Set-Location $root
& $py -c "import os, runpy, site, sys; os.path.isdir(sys.argv[1]) and site.addsitedir(sys.argv[1]); runpy.run_module(sys.argv[2], run_name='__main__', alter_sys=True)" $site $pkg
