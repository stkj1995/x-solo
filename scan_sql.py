import re

# Path to your app.py file
file_path = "app.py"

# Regex patterns for truly unsafe SQL
unsafe_patterns = [
    r'f["\'].*(SELECT|INSERT|UPDATE|DELETE).*{.*}.*["\']',  # f-strings with variables
    r'["\'].*(SELECT|INSERT|UPDATE|DELETE).*["\']\s*\+\s*.*' # string concatenation
]

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Scanning for truly unsafe SQL queries...\n")

found = False
for i, line in enumerate(lines, start=1):
    for pattern in unsafe_patterns:
        if re.search(pattern, line):
            print(f"⚠️ Unsafe SQL found at line {i}: {line.strip()}")
            found = True

if not found:
    print("✅ No unsafe SQL detected! All queries use placeholders or safe methods.")
