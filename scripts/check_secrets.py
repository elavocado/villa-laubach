"""Reject common captured credentials without printing their values."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'Google API key': re.compile(r'AIza[0-9A-Za-z_-]{35}'),
    'GitHub token': re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})'),
    'AWS access key': re.compile(r'(?:AKIA|ASIA)[A-Z0-9]{16}'),
    'Slack token': re.compile(r'xox[baprs]-[A-Za-z0-9-]{20,}'),
    'Private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
}
paths = subprocess.check_output(
    ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT
).decode('utf-8').split('\0')
failures = []
for name in set(paths):
    path = ROOT / name
    if not name or not path.is_file():
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for kind, pattern in PATTERNS.items():
        if pattern.search(text):
            failures.append(f'{name}: {kind}')
if failures:
    raise SystemExit('Potential secrets detected (values hidden):\n' + '\n'.join(failures))
print('Credential-pattern check passed. This is a safeguard, not a complete security audit.')
