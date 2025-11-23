import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    import requests
    print("✓ requests is installed")
except ImportError:
    print("✗ requests is NOT installed")

try:
    from bs4 import BeautifulSoup
    print("✓ BeautifulSoup is installed")
except ImportError:
    print("✗ BeautifulSoup is NOT installed")

print("\nIf packages are not installed, run:")
print("pip install -r requirements.txt")
