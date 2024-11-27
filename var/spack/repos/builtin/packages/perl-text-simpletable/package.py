# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextSimpletable(PerlPackage):
    """Simple Eyecandy ASCII Tables"""

    homepage = "https://metacpan.org/pod/Text::SimpleTable"
    url = "http://search.cpan.org/CPAN/authors/id/M/MR/MRAMBERG/Text-SimpleTable-2.04.tar.gz"

    license("Artistic-2.0")

    version("2.07", sha256="256d3f38764e96333158b14ab18257b92f3155c60d658cafb80389f72f4619ed")
    version("2.04", sha256="8d82f3140b1453b962956b7855ba288d435e7f656c3c40ced4e3e8e359ab5293")
