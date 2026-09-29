"""Fork-only audit: Python 2.7 package import fails in the unchanged baseline."""

import imp
import subprocess
import sys


for directory in ('baseline', '.'):
    process = subprocess.Popen(
        [sys.executable, '-c', 'import pytimeparse'], cwd=directory,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert process.returncode != 0, (directory, stdout, stderr)
    assert "'encoding' is an invalid keyword argument" in stderr, stderr
    print('Confirmed existing package import blocker: ' + directory)

parser = imp.load_source('parser_only', 'pytimeparse/timeparse.py').timeparse
baseline = imp.load_source('baseline_parser', 'baseline/pytimeparse/timeparse.py').timeparse
assert baseline('1-04:18:35') is None
for text, expected in (
        ('1-04:18:35', 101915), ('0-00:00:00', 0),
        ('12-04:18:35', 1052315), ('-1-04:18:35', -101915),
        ('+1-04:18:35', 101915), ('1-04:18:35.25', 101915.25),
        ('-1-04:18:35.25', -101915.25), ('1:04:18:35', 101915)):
    result = parser(text)
    assert result == expected, (text, result)
    assert type(result) is type(expected), (text, type(result))
for text in ('1--04:18:35', '1-4:18:35', '1-04:18', '1.5-04:18:35'):
    assert parser(text) is None, text
assert parser('1-04:18:35', granularity='minutes') == 101915
print('Python 2.7 parser-only checks passed; package/suite compatibility NOT established.')
