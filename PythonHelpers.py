
#!/usr/bin/env python
import PythonHelpers
import argparse
from PythonHelpers import version

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "TODO")
	parser.add_argument('-V', '--version', action='version', version = '%(prog)s {}'.format(version))
	args = parser.parse_args()
