# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Neartree(MakefilePackage):
    """This is a release of an API for finding nearest neighbors among
    points in spaces of arbitrary dimensions."""

    homepage = "https://neartree.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/neartree/neartree/NearTree-3.1/NearTree-3.1.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.1", sha256="07b668516f15a7c13c219fd005b14e73bced5dc6b23857edcc24d3e5cf0d3be3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libtool", type="build")
    depends_on("cvector")

    def edit(self, spec, prefix):
        mf = FileFilter("Makefile")
        mf.filter(r"^CC.+", "CC = {0}".format(spack_cc))
        mf.filter(r"^INSTALL_PREFIX .+", "INSTALL_PREFIX = {0}".format(prefix))

    def build(self, spec, prefix):
        pass
