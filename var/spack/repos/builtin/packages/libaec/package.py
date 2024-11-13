# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libaec(CMakePackage):
    """Libaec provides fast lossless compression of 1 up to 32 bit wide signed
    or unsigned integers (samples). It implements Golomb-Rice compression
    method under the BSD license and includes a free drop-in replacement for
    the SZIP library.
    """

    homepage = "https://gitlab.dkrz.de/k202009/libaec"
    url = "https://gitlab.dkrz.de/api/v4/projects/k202009%2Flibaec/repository/archive.tar.gz?sha=v1.0.2"
    list_url = "https://gitlab.dkrz.de/k202009/libaec/tags"

    provides("szip")

    license("BSD-2-Clause")

    version("1.0.6", sha256="abab8c237d85c982bb4d6bde9b03c1f3d611dcacbd58bca55afac2496d61d4be")
    version("1.0.5", sha256="7bf7be828dc3caefcc968e98a59b997b6b3b06e4123137e9e0b0988dc1be3b2f")
    version("1.0.4", sha256="7456adff4e817f94fc57a3eca824db1c203770ffb7a9253c435093ac5e239e31")
    version("1.0.3", sha256="c28b340b20dcc0ad352970143e01718bd68dd5ef2a07a971736368805972f562")
    version("1.0.2", sha256="b9e5bbbc8bf9cbfd3b9b4ce38b3311f2c88d3d99f476edb35590eb0006aa1fc5")
    version("1.0.1", sha256="3668eb4ed36724441e488a7aadc197426afef4b1e8bd139af6d3e36023906459")
    version("1.0.0", sha256="849f08b08ddaaffe543d06d0ced5e4ee3e526b13a67c5f422d126b1c9cf1b546")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Builds a shared version of the library")

    @property
    def libs(self):
        query = self.spec.last_query
        libraries = ["libaec"]

        if "szip" == query.name or "szip" in query.extra_parameters:
            libraries.insert(0, "libsz")

        shared = "~shared" not in self.spec

        libs = find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

        if not libs:
            msg = "Unable to recursively locate {0} {1} libraries in {2}"
            raise spack.error.NoLibrariesError(
                msg.format("shared" if shared else "static", self.spec.name, self.spec.prefix)
            )
        return libs

    def cmake_args(self):
        return [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
