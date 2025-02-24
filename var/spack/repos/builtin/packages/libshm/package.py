# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libshm(Package):
    """Libshm is a header library
    making an easy C++11 access to a shared memory."""

    homepage = "https://github.com/afeldman/libshm"
    git = "https://github.com/afeldman/libshm.git"

    license("MIT")

    version("master")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
