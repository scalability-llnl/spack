# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ph5concat(AutotoolsPackage):
    """Parallel Data Concatenation for High Energy Physics Data Analysis"""

    homepage = "https://github.com/NU-CUCIS/ph5concat"
    url = "https://github.com/NU-CUCIS/ph5concat/archive/v1.1.0.tar.gz"

    maintainers("vhewes")

    version("1.1.0", sha256="cecc22325a56771cda1fc186e6bd1f9bde2957beca3fa9a387d55462efd5254f")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("zlib")
    depends_on("hdf5+hl+mpi@1.10.4:1.12")
    depends_on("mpich")

    variant("profiling", default=False, description="Enable profiling support")

    def setup_build_environment(self, env):
        env.set("LIBS", "-ldl -lz")

    def configure_args(self):
        args = [f"--with-{pkg}={self.spec[pkg].prefix}" for pkg in ("hdf5", "mpich")]
        args.extend(self.enable_or_disable("profiling"))
        return args
