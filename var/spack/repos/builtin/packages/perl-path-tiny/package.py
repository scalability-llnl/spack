# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-0.108.tar.gz"

    license("Apache-2.0")

    version("0.146", sha256="861ef09bca68254e9ab24337bb6ec9d58593a792e9d68a27ee6bec2150f06741")
    version("0.144", sha256="f6ea094ece845c952a02c2789332579354de8d410a707f9b7045bd241206487d")
    version("0.108", sha256="3c49482be2b3eb7ddd7e73a5b90cff648393f5d5de334ff126ce7a3632723ff5")
