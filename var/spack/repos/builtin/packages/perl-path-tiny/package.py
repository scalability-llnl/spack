# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPathTiny(PerlPackage):
    """This module provides a small, fast utility for working with file paths.
    It is friendlier to use than File::Spec and provides easy access to
    functions from several other core file handling modules. It aims to be
    smaller and faster than many alternatives on CPAN, while helping people do
    many common things in consistent and less error-prone ways."""

    homepage = "https://metacpan.org/pod/Path::Tiny"
    url      = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-0.108.tar.gz"

    version('0.108', sha256='3c49482be2b3eb7ddd7e73a5b90cff648393f5d5de334ff126ce7a3632723ff5')
