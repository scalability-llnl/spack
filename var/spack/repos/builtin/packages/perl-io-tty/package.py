# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoTty(PerlPackage):
    """IO::Tty is used internally by IO::Pty to create a pseudo-tty. You
    wouldn't want to use it directly except to import constants, use IO::Pty.
    For a list of importable constants, see IO::Tty::Constant."""

    homepage = "https://metacpan.org/pod/IO::Tty"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/IO-Tty-1.13_01.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.20", sha256="b15309fc85623893289cb9b2b88dfa9ed1e69156b75f29938553a45be6d730af")
    version("1.17", sha256="a5f1a83020bc5b5dd6c1b570f48c7546e0a8f7fac10a068740b03925ad9e14e8")
    version("1.13_01", sha256="89798eba7c31d9c169ef2f38ff49490aa769b1d9a68033de365595cfaf9cc258")
