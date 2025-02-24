# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class KvasirMpl(Package):
    """Kvasir metaprogramming library"""

    homepage = "https://github.com/kvasir-io/mpl"
    git = "https://github.com/kvasir-io/mpl.git"

    license("BSL-1.0")

    version("develop", branch="development")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree("src", prefix.include)
