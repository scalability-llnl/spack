# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Neartree(MakefilePackage):
    """This is a release of an API for finding nearest neighbors among
    points in spaces of arbitrary dimensions."""

    homepage = "https://neartree.sourceforge.net/"

    license("LGPL-2.1-or-later")

    version("5.1.1", sha256="b951eb23bb4235ada82cef85b9f129bf74a14e45d992097431e7bfb6bdca6642")
    version("3.1", sha256="07b668516f15a7c13c219fd005b14e73bced5dc6b23857edcc24d3e5cf0d3be3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libtool", type="build")
    depends_on("cvector")

    patch("Makefile.patch", when="@5.1.1")
    patch("Makefile-3.1.patch", when="@3.1")

    def url_for_version(self, version):
        pattern = re.compile(r"^[0-9]+\.[0-9]+")
        full_vers = str(version)
        cropped_vers = pattern.search(full_vers).group()
        return f"https://downloads.sourceforge.net/project/neartree/neartree/NearTree-{cropped_vers}/NearTree-{full_vers}.tar.gz"

    def edit(self, spec, prefix):
        mf = FileFilter("Makefile")
        mf.filter(r"^CC.+", "CC = {0}".format(spack_cc))
        mf.filter(r"^INSTALL_PREFIX .+", "INSTALL_PREFIX = {0}".format(prefix))

    def build(self, spec, prefix):
        pass
