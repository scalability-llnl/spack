# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Cvector(MakefilePackage):
    """CVector -- ANSI C API for Dynamic Arrays"""

    homepage = "https://cvector.sourceforge.net/"

    license("LGPL-2.1-or-later")

    version("1.0.3.1", sha256="6492b2beb26c3179cdd19abc90dc47a685be471c594d5ab664283e1d3586acdc")
    version(
        "1.0.3",
        sha256="d3fa92de3cd5ba8697abdbb52080248b2c252a81cf40a8ec639be301518d0ce3",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("libtool", type="build")

    patch("Makefile.patch", when="@1.0.3.1")

    def url_for_version(self, version):
        pattern = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+")
        full_vers = str(version)
        cropped_vers = pattern.search(full_vers).group()
        return f"https://downloads.sourceforge.net/project/cvector/cvector/CVector-{cropped_vers}/CVector-{full_vers}.tar.gz"

    def edit(self, spec, prefix):
        mf = FileFilter("Makefile")
        mf.filter(r"^CC.+", "CC = {0}".format(spack_cc))
        mf.filter(r"^INSTALL_PREFIX .+", "INSTALL_PREFIX = {0}".format(prefix))

    def build(self, spec, prefix):
        pass
