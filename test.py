import unittest
from unittest.mock import patch
import argparse
import os
import sys
from io import StringIO

from jemma.main import main

class TestJemmaCommands(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, stdout):
        # Execute jemma with no arguments to trigger the help message
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        # Check that the help message is printed
        self.assertIn('usage: jemma', stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
