# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Phred(MakefilePackage):
    """The phred software reads DNA sequencing trace files, calls bases,
    and assigns a quality value to each called base."""

    homepage = "http://www.phrap.org/phredphrapconsed.html"
    url = "file://{0}/phred.tar.gz".format(os.getcwd())
    manual_download = True

    version("071220", sha256="26212f13fa906c1ca0af61f48d52a5f2c1aacba802bf729ba65ca5222463abce")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("phred", prefix.bin)
