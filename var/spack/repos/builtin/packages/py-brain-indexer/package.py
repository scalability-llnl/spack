# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyBrainIndexer(PythonPackage):
    """Spatial indexer for geometries and morphologies"""

    homepage = "https://github.com/BlueBrain/brain-indexer"
    pypi = "brain-indexer/brain_indexer-3.0.0.tar.gz"

    license("Apache-2.0", checked_by="matz-e")

    maintainers("matz-e")

    version("3.0.0", sha256="23947519df5f87c65781d1776f02e8e17798c40c617399b02e6ecae8e09a0a72")

    variant("mpi", default=True, description="Enable MPI parallelism")

    depends_on("py-scikit-build-core+pyproject@:0.7", type="build")
    depends_on("py-setuptools-scm@8.0:", type="build")
    depends_on("cmake@3.5:")
    depends_on("boost@1.79.0: +filesystem+serialization")
    depends_on("py-docopt-ng", type=("build", "run"))
    depends_on("py-libsonata", type=("build", "run"))
    depends_on("py-morphio", type=("build", "run"))
    depends_on("py-numpy-quaternion", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))

    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", type=("build", "run"), when="+mpi")

    def config_settings(self, spec, prefix):
        return {"cmake.define.CMAKE_INSTALL_RPATH_USE_LINK_PATH": "ON"}
