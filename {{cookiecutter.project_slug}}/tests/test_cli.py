#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: Geo-Comm Developer <coders@geo-comm.com>

This is the test module for the project's command-line interface (CLI)
module.
"""
import logging
import unittest
from click.testing import CliRunner, Result
import {{cookiecutter.package_name}}.cli as cli
from {{cookiecutter.package_name}} import __version__

# To learn more about testing Click applications, visit the link below.
# http://click.pocoo.org/5/testing/

class TestCommonCliCase(unittest.TestCase):
    """
    This case contains tests of the command-line interface (CLI).
    """
    def test_version_displaysLibraryVersion(self):
        """
        Arrange/Act: Run the `version` subcommand.
        Assert: The output matches the library version.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ['version'])
        self.assertIn(__version__, result.output.strip(),
                      msg='Version number should match library version.')

    def test_verbose_outputVerbose(self):
        """
        Arrange/Act: Run the `version` subcommand with the '-v' flag.
        Assert: The output indicates verbose logging is enabled.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ['-v', 'version'])
        self.assertIn('Verbose', result.output.strip(),
                      msg='Verbose logging should be indicated in output.')


if __name__ == '__main__':
    unittest.main()
