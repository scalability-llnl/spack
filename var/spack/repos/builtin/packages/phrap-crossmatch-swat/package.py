# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PhrapCrossmatchSwat(MakefilePackage):
    """phrap is a program for assembling shotgun DNA sequence data.
    cross_match is a general purpose utility for comparing any two DNA
    sequence sets using a 'banded' version of swat.
    swat is a program for searching one or more DNA or protein query
    sequences, or a query profile, against a sequence database"""

    homepage = "http://www.phrap.org/phredphrapconsed.html"
    url = "file://{0}/phrap-crossmatch-swat-1.090518.tar.gz".format(os.getcwd())
    manual_download = True

    version("1.090518", sha256="81f50c4410e8604cdefcc34ef6dc7b037be3bb45b94c439611a5590c1cf83665")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for b in ["phrap", "cross_match", "swat"]:
            install(b, prefix.bin)
