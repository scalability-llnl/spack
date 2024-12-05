# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileChdir(PerlPackage):
    """Perl's chdir() has the unfortunate problem of being very, very, very
    global. If any part of your program calls chdir() or if any library you use
    calls chdir(), it changes the current working directory for the *whole*
    program.

    This sucks.

    File::chdir gives you an alternative, $CWD and @CWD. These two variables
    combine all the power of chdir(), File::Spec and Cwd."""

    homepage = "https://metacpan.org/pod/File::chdir"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/File-chdir-0.1011.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.1011", sha256="31ebf912df48d5d681def74b9880d78b1f3aca4351a0ed1fe3570b8e03af6c79")
