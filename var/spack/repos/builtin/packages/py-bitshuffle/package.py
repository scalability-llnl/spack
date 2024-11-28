# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBitshuffle(PythonPackage):
    """Filter for improving compression of typed binary data."""

    homepage = "https://github.com/kiyo-masui/bitshuffle"
    pypi = "bitshuffle/bitshuffle-0.4.2.tar.gz"

    license("MIT")

    version("0.4.2", sha256="df7d7dc0add8a37f0c5f4704475db60a3c843171a49aa4e3301d1d7e827b2536")

    depends_on("c", type="build")  # generated

    depends_on("py-cython@0.19:", type="build")
    depends_on("py-setuptools@0.7:", type="build")
    depends_on("py-numpy@1.6.1:", type=("build", "run"))
    depends_on("py-h5py@2.4.0:", type=("build", "run"))
    # setup.py:220
    depends_on("hdf5@1.8.11:~mpi")

    def setup_build_environment(self, env):
        env.set("HDF5_DIR", self.spec["hdf5"].prefix)
