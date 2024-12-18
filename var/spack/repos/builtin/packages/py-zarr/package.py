# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZarr(PythonPackage):
    """Zarr is a Python package providing an implementation of chunked,
    compressed, N-dimensional arrays."""

    homepage = "https://zarr.readthedocs.io"
    pypi = "zarr/zarr-2.3.2.tar.gz"

    license("MIT")

    version("2.17.0", sha256="6390a2b8af31babaab4c963efc45bf1da7f9500c9aafac193f84cf019a7c66b0")
    version("2.10.2", sha256="5c6ae914ab9215631bb95c09e76b9b9b4fffa70fec0c7bca26b68387d858ebe2")
    version("2.6.1", sha256="fa7eac1e4ff47ff82d09c42bb4679e18e8a05a73ee81ce59cee6a441a210b2fd")
    version("2.5.0", sha256="d54f060739208392494c3dbcbfdf41c8df9fa23d9a32b91aea0549b4c5e2b77f")
    version("2.4.0", sha256="53aa21b989a47ddc5e916eaff6115b824c0864444b1c6f3aaf4f6cf9a51ed608")
    version("2.3.2", sha256="c62d0158fb287151c978904935a177b3d2d318dea3057cfbeac8541915dfa105")

    depends_on("python@3.9:", type=("build", "run"), when="@2.17:")
    depends_on("python@3.7:3", type=("build", "run"), when="@2.10")
    depends_on("py-setuptools@64:", type="build", when="@2.17:")
    depends_on("py-setuptools@38.6.0:", type="build", when="@2.4.0:")
    depends_on("py-setuptools@18.0:", type="build")
    depends_on("py-setuptools-scm@1.5.5:", type="build")
    depends_on("py-asciitree", type=("build", "run"))
    depends_on("py-numpy@1.21.1:", type=("build", "run"), when="@2.17:")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    # https://github.com/zarr-developers/zarr-python/issues/1818
    depends_on("py-numpy@:1", when="@:2.17", type=("build", "run"))
    depends_on("py-fasteners", type=("build", "run"))
    depends_on("py-numcodecs@0.10:", type=("build", "run"), when="@2.17:")
    depends_on("py-numcodecs@0.6.4:", type=("build", "run"), when="@2.4.0:")
    depends_on("py-numcodecs@0.6.2:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-msgpack", type=("build", "run"), when="@:2.3.2")
