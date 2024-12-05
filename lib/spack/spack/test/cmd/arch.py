# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand

arch = SpackCommand("arch")


def test_arch():
    """Sanity check ``spack arch`` to make sure it works."""

    arch()
    arch("-f")
    arch("--frontend")
    arch("-b")
    arch("--backend")


def test_arch_platform():
    """Sanity check ``spack arch --platform`` to make sure it works."""

    arch("-p")
    arch("--platform")
    arch("-f", "-p")
    arch("-b", "-p")


def test_arch_operating_system():
    """Sanity check ``spack arch --operating-system`` to make sure it works."""

    arch("-o")
    arch("--operating-system")
    arch("-f", "-o")
    arch("-b", "-o")


def test_arch_target():
    """Sanity check ``spack arch --target`` to make sure it works."""

    arch("-t")
    arch("--target")
    arch("-f", "-t")
    arch("-b", "-t")


def test_display_targets():
    arch("--known-targets")
