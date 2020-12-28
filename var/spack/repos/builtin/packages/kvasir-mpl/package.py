# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class KvasirMpl(Package):
    """Kvasir metaprogramming library"""

    homepage = "https://github.com/kvasir-io/mpl"
    git      = "https://github.com/kvasir-io/mpl.git"

    version('develop', branch='development')

    def install(self, spec, prefix):
        install_tree('src', prefix.include)
