# topicmaps.tests.test_init
# Testing package for the DDL Logbook project.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Jun 01 21:22:26 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: test_init.py [] benjamin@bengfort.com $

"""
Sanity checking for testing purposes.
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Initialization Tests (for sanity)
##########################################################################

EXPECTED_VERSION = "0.2.2"

class InitializationTests(unittest.TestCase):


    def test_initialization(self):
        """
        Check the test suite runs by affirming 2+3=5
        """
        self.assertEqual(2+3, 5)


    def test_import(self):
        """
        Ensure the test suite can import our module
        """
        try:
            import topicmaps
        except ImportError:
            self.fail("Was not able to import topicmaps")


    def test_expected_version(self):
        """
        Check the expected version matches the actual one
        """
        import topicmaps
        self.assertEqual(topicmaps.__version__, EXPECTED_VERSION)
