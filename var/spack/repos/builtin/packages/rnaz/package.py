# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rnaz(AutotoolsPackage):
    """RNAz - predicting structural noncoding RNAs."""

    homepage = "https://www.tbi.univie.ac.at/software/RNAz"
    url      = "https://www.tbi.univie.ac.at/software/RNAz/RNAz-2.1.tar.gz"

    version('2.1', sha256='b32ec0361889319f2058f224d6c456c853dbc30dff4dba90c53a8f9fd7b83be5')
