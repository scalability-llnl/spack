# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Raft(CMakePackage):
    """RAFT: Reconstruct Algorithms for Tomography.
    Toolbox under development at Brazilian Synchrotron Light Source."""

    homepage = "https://bitbucket.org/gill_martinez/raft_aps"
    url = "https://bitbucket.org/gill_martinez/raft_aps/get/1.2.3.tar.gz"
    git = "https://bitbucket.org/gill_martinez/raft_aps.git"

    version("develop", branch="master")
    version("1.2.3", sha256="c41630e74491c8db272dcf4707e9b11cdcb226c0b7e978ca6eba8006f47bdae6")

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("cmake", type="build")
    depends_on("hdf5")
    depends_on("fftw")
    depends_on("cuda")

    def install(self, spec, prefix):
        """RAFT lacks an install in its CMakeList"""

        with working_dir(self.stage.source_path):
            mkdirp(prefix)

            # We only care about the binary
            install_tree("bin", prefix.bin)
