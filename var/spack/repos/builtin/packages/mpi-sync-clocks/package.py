# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MpiSyncClocks(AutotoolsPackage):
    """MPI Sync Clocks.

    MPI Sync Clocks is an implementation of synchronized clocks using MPI.
    """

    homepage = "https://pm2.gitlabpages.inria.fr/"
    url = "https://pm2.gitlabpages.inria.fr/releases/mpi_sync_clocks-1.0.tar.gz"
    git = "https://gitlab.inria.fr/pm2/pm2.git"

    build_directory = "build"

    maintainers("a-denis")
    license("LGPL-2.1-or-later", checked_by="a-denis")

    version("master", branch="master")
    version("1.0", sha256="06c63adc2f3ae7d00e3bdbbe62ee6800660fde320a3d36a232799e015165a1ff")

    depends_on("c", type="build")
    depends_on("autoconf@2.69:", type="build")
    depends_on("mpi", type=("build", "link", "run"))

    @property
    def configure_directory(self) -> str:
        if "@master" in self.spec:
            return "mpi_sync_clocks"
        else:
            return super().configure_directory

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            Executable("./autogen.sh")()
