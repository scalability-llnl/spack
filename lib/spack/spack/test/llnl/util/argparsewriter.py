# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``llnl/util/argparsewriter.py``

These tests are fairly minimal, and ArgparseWriter is more extensively
tested in ``cmd/commands.py``.
"""

import pytest

import llnl.util.argparsewriter as aw

import spack.main

parser = spack.main.make_argument_parser()
spack.main.add_all_commands(parser)


def test_format_not_overridden():
    with pytest.raises(TypeError):
        aw.ArgparseWriter("spack")
