# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextSimpletable(PerlPackage):
    """Simple Eyecandy ASCII Tables"""

    homepage = "http://search.cpan.org/~mramberg/Text-SimpleTable/lib/Text/SimpleTable.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MR/MRAMBERG/Text-SimpleTable-2.04.tar.gz"

    version('2.04', sha256='8d82f3140b1453b962956b7855ba288d435e7f656c3c40ced4e3e8e359ab5293')
