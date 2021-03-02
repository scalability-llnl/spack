# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import spack.config
from spack.main import SpackCommand

config_cmd = SpackCommand('config')


def get_config_line(pattern, lines):
    """Get a configuration line that matches a particular pattern."""
    line = next((x for x in lines if re.search(pattern, x)), None)
    assert line is not None, 'no such line!'
    return line


def check_blame(element, file_name, line=None):
    """Check that `config blame config` gets right file/line for an element.

    This runs `spack config blame config` and scrapes the output for a
    particular YAML key. It thne checks that the requested file/line info
    is also on that line.

    Line is optional; if it is ``None`` we just check for the
    ``file_name``, which may just be a name for a special config scope
    like ``_builtin`` or ``command_line``.
    """
    output = config_cmd('blame', 'config')

    blame_lines = output.rstrip().split('\n')
    element_line = get_config_line(element + ':', blame_lines)

    annotation = file_name
    if line is not None:
        annotation += ':%d' % line

    assert file_name in element_line


def test_config_blame(config):
    """check blame info for elements in mock configuration."""
    config_file = config.get_config_filename('site', 'config')

    check_blame('install_trees', config_file, 2)
    check_blame('source_cache', config_file, 11)
    check_blame('misc_cache', config_file, 12)
    check_blame('verify_ssl', config_file, 13)
    check_blame('checksum', config_file, 14)
    check_blame('dirty', config_file, 15)


def test_config_blame_with_override(config):
    """check blame for an element from an override scope"""
    config_file = config.get_config_filename('site', 'config')

    with spack.config.override('config:install_trees', {'root': 'foobar'}):
        check_blame('install_trees', 'overrides')

        check_blame('source_cache', config_file, 11)
        check_blame('misc_cache', config_file, 12)
        check_blame('verify_ssl', config_file, 13)
        check_blame('checksum', config_file, 14)
        check_blame('dirty', config_file, 15)
