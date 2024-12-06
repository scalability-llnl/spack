# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Ampliconnoise(MakefilePackage):
    """AmpliconNoise is a collection of programs for the removal of noise
    from 454 sequenced PCR amplicons."""

    homepage = "https://directory.fsf.org/wiki/AmpliconNoise"
    url = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/ampliconnoise/AmpliconNoiseV1.29.tar.gz"

    version("1.29", sha256="0bf946806d77ecaf0994ad8ebf9a5e98ad33c809f6def5c9340a16c367918167")

    depends_on("c", type="build")  # generated

    depends_on("mpi@2:")
    depends_on("gsl")

    patch("Fix-return-type.patch")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.Scripts)
        env.set("PYRO_LOOKUP_FILE", os.path.join(self.prefix, "Data", "LookUp_E123.dat"))
        env.set("SEQ_LOOKUP_FILE", os.path.join(self.prefix, "Data", "Tran.dat"))

    def install(self, spec, prefix):
        make("install")
        install_tree("bin", prefix.bin)
        install_tree("Data", prefix.Data)
        install_tree("FastaUnique", prefix.FastaUnique)
        install_tree("FCluster", prefix.FCluster)
        install_tree("NDist", prefix.NDist)
        install_tree("Perseus", prefix.Perseus)
        install_tree("PerseusD", prefix.PerseusD)
        install_tree("PyroDist", prefix.PyroDist)
        install_tree("PyroNoise", prefix.PyroNoise)
        install_tree("PyroNoiseM", prefix.PyroNoiseM)
        install_tree("Scripts", prefix.Scripts)
        install_tree("SeqDist", prefix.SeqDist)
        install_tree("SeqNoise", prefix.SeqNoise)
        install_tree("SplitClusterClust", prefix.SplitClusterClust)
        install_tree("SplitClusterEven", prefix.SplitClusterEven)
        install_tree("Test", prefix.Test)
        install_tree("TestFLX", prefix.TestFLX)
        install_tree("TestTitanium", prefix.TestTitanium)
        install_tree("TestTitaniumFast", prefix.TestTitaniumFast)
