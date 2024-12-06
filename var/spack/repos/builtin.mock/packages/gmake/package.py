# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmake(Package):
    """Dummy GMake Package"""

    homepage = "https://www.gnu.org/software/make"
    url = "https://ftpmirror.gnu.org/make/make-4.4.tar.gz"

    version("4.4", sha256="ce35865411f0490368a8fc383f29071de6690cbadc27704734978221f25e2bed")
    version("3.0", sha256="ce35865411f0490368a8fc383f29071de6690cbadc27704734978221f25e2bed")

    def do_stage(self):
        mkdirp(self.stage.source_path)
