# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoTty(PerlPackage):
    """IO::Tty is used internally by IO::Pty to create a pseudo-tty. You
    wouldn't want to use it directly except to import constants, use IO::Pty.
    For a list of importable constants, see IO::Tty::Constant."""

    homepage = "https://metacpan.org/pod/IO::Tty"
    url      = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/IO-Tty-1.13_01.tar.gz"

    version('1.13_01', sha256='89798eba7c31d9c169ef2f38ff49490aa769b1d9a68033de365595cfaf9cc258')
