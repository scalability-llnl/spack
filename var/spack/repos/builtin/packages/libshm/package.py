# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libshm(Package):
    """Libshm is a header library
    making an easy C++11 access to a shared memory."""

    homepage = "https://github.com/afeldman/libshm"
    git      = "https://github.com/afeldman/libshm.git"

    version('master')

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
