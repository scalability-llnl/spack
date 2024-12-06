# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.main import SpackCommand


def test_reuse_after_help():
    """Test `spack help` can be called twice with the same SpackCommand."""
    help_cmd = SpackCommand("help", subprocess=True)
    help_cmd()
    help_cmd()


def test_help():
    """Sanity check the help command to make sure it works."""
    help_cmd = SpackCommand("help", subprocess=True)
    out = help_cmd()
    assert "These are common spack commands:" in out


def test_help_all():
    """Test the spack help --all flag"""
    help_cmd = SpackCommand("help", subprocess=True)
    out = help_cmd("--all")
    assert "Complete list of spack commands:" in out


def test_help_spec():
    """Test the spack help --spec flag"""
    help_cmd = SpackCommand("help")
    out = help_cmd("--spec")
    assert "spec expression syntax:" in out


def test_help_subcommand():
    """Test the spack help subcommand argument"""
    help_cmd = SpackCommand("help")
    out = help_cmd("help")
    assert "get help on spack and its commands" in out
