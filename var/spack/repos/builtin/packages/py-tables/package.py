# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTables(PythonPackage):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""

    homepage = "https://www.pytables.org/"
    pypi = "tables/tables-3.6.1.tar.gz"
    git = "https://github.com/PyTables/PyTables.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("3.9.0", sha256="27c9ca14c359d875caf945a6a527c12690e017650402dd17d8eb8b6caf6687d5")
    version("3.8.0", sha256="34f3fa2366ce20b18f1df573a77c1d27306ce1f2a41d9f9eff621b5192ea8788")
    version("3.7.0", sha256="e92a887ad6f2a983e564a69902de4a7645c30069fc01abd353ec5da255c5e1fe")
    version("3.6.1", sha256="49a972b8a7c27a8a173aeb05f67acb45fe608b64cd8e9fa667c0962a60b71b49")
    version("3.6.0", sha256="db3488214864fb313a611fca68bf1c9019afe4e7877be54d0e61c84416603d4d")
    version("3.5.2", sha256="b220e32262bab320aa41d33125a7851ff898be97c0de30b456247508e2cc33c2")
    version("3.4.4", sha256="bdc5c073712af2a43babd139c4855fc99496bb2c3f3f5d1b4770a985e6f9ce29")
    version("3.3.0", sha256="8383ccf02e041a5d55494a09fc5514140b4653055a2732c981b5fd0f7408822c")
    version("3.2.2", sha256="3564b351a71ec1737b503b001eb7ceae1f65d5d6e3ffe1ea75aafba10f37fa84")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("zlib", default=True, description="Support for zlib compression")
    variant("bzip2", default=False, description="Support for bzip2 compression")
    variant("lzo", default=False, description="Support for lzo compression")

    # pyproject.toml
    depends_on("py-setuptools@61:", when="@3.9:", type="build")
    depends_on("py-setuptools@42:", when="@3.7:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.32:", when="@3.9:", type="build")
    depends_on("py-cython@0.29.21:", when="@3.7:3.8", type=("build", "run"))
    depends_on("py-cython@0.21:", type="build")

    # setup.py
    depends_on("python@3.8:", when="@3.8:", type=("build", "run"))

    # requirements.txt
    depends_on("py-numpy@1.19:", when="@3.8:", type=("build", "run"))
    depends_on("py-numpy@1.9.3:", type=("build", "run"))
    # https://github.com/PyTables/PyTables/issues/1083
    depends_on("py-numpy@:1", type=("build", "run"))
    depends_on("py-numexpr@2.6.2:", type=("build", "run"))
    depends_on("py-packaging", when="@3.7:", type=("build", "run"))
    depends_on("py-py-cpuinfo", when="@3.8:", type=("build", "run"))
    depends_on("py-blosc2@2.2.8:", when="@3.9:", type=("build", "run"))
    depends_on("py-blosc2@2.0", when="@3.8", type=("build", "run"))

    # tables/req_versions.py
    depends_on("hdf5@1.10.5:", when="@3.8:")
    depends_on("hdf5@1.8.4:", when="@3.4:")
    depends_on("hdf5@1.8.4:1.8", when="@:3.3")
    # Versions prior to 3.3 must build with the internal blosc due to a lock
    # problem in a multithreaded environment.
    depends_on("c-blosc@1.11.1:", when="@3.8:")
    depends_on("c-blosc@1.4.1:", when="@3.3:")

    depends_on("zlib-api", when="+zlib")
    depends_on("bzip2", when="+bzip2")
    depends_on("lzo", when="+lzo")

    conflicts("%apple-clang@15:", when="@:3.8")

    # Historical dependencies
    depends_on("py-six@1.9:", when="@:3.5", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("HDF5_DIR", self.spec["hdf5"].prefix)
        if "+bzip2" in self.spec:
            env.set("BZIP2_DIR", self.spec["bzip2"].prefix)
        if "+lzo" in self.spec:
            env.set("LZO_DIR", self.spec["lzo"].prefix)
        if "^c-blosc" in self.spec:
            env.set("BLOSC_DIR", self.spec["c-blosc"].prefix)
