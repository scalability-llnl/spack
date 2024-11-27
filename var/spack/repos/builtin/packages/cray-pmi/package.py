# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CrayPmi(Package):
    """Cray's Process Management Interface library"""

    homepage = "https://docs.nersc.gov/development/compilers/wrappers/"
    has_code = False  # Skip attempts to fetch source that is not available

    maintainers("haampie")

    version("5.0.17")
    version("5.0.16")
    version("5.0.11")

    @property
    def headers(self):
        return find_headers("pmi", self.prefix.include, recursive=True)

    @property
    def libs(self):
        return find_libraries(["libpmi"], root=self.prefix, recursive=True)
