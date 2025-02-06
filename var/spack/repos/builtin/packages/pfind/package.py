# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pfind(Package):
    """
    The tool provides parallel access to a single directory. However, this
    feature depends on the distribution of the "cookie" returned by telldir().
    Depending on the system, it may work.
    """

    homepage = "https://github.com/VI4IO/pfind"
    git = "https://github.com/VI4IO/pfind.git"

    version("main", branch="master")

    depends_on("mpi")

    def setup_build_environment(self, env):
        env.set("CC", self.spec["mpi"].mpicc, force=True)
        env.set("CXX", self.spec["mpi"].mpicxx, force=True)

    def install(self, spec, prefix):

        for installer_path in ["./prepare.sh", "./compile.sh"]:
            set_executable(installer_path)
            installer = Executable(installer_path)
            installer()

        mkdirp(prefix.bin)
        install("pfind", prefix.bin)
