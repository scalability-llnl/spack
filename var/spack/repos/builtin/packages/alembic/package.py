# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Alembic(CMakePackage):
    """Alembic is an open computer graphics interchange
    framework. Alembic distills complex, animated scenes into a
    non-procedural, application-independent set of baked
    geometric results."""

    homepage = "https://www.alembic.io"
    url = "https://github.com/alembic/alembic/archive/1.7.16.tar.gz"

    license("BSD-3-Clause")

    version("1.8.6", sha256="c572ebdea3a5f0ce13774dd1fceb5b5815265cd1b29d142cf8c144b03c131c8c")
    version("1.8.5", sha256="180a12f08d391cd89f021f279dbe3b5423b1db751a9898540c8059a45825c2e9")
    version("1.7.16", sha256="2529586c89459af34d27a36ab114ad1d43dafd44061e65cfcfc73b7457379e7c")

    depends_on("cxx", type="build")  # generated

    variant("python", default=False, description="Python support")
    variant("hdf5", default=False, description="HDF5 support")

    depends_on("cmake@2.8.11:", type="build")
    depends_on("openexr@2.2.0:")
    depends_on("hdf5@1.8.9:", when="+hdf5")
    depends_on("boost@1.55:")
    depends_on("zlib-api")
    depends_on("py-ilmbase", when="+python")

    def cmake_args(self):
        args = [self.define_from_variant("USE_HDF5", "hdf5")]

        if self.spec.satisfies("+python") and self.spec["python"].satisfies("@3:"):
            args.append("-DPython_ADDITIONAL_VERSIONS=3")

        return args
