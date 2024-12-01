# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hdf5VolLog(AutotoolsPackage):
    """Log-based VOL - an HDF5 VOL Plugin that stores HDF5 datasets in a log-based
    storage layout."""

    homepage = "https://github.com/DataLib-ECP/vol-log-based"
    url = "https://github.com/DataLib-ECP/vol-log-based"
    git = "https://github.com/DataLib-ECP/vol-log-based.git"
    maintainers("hyoklee", "lrknox")

    version("master-1.1", branch="master")

    version("1.4.0", tag="logvol.1.4.0", commit="786d2cc4da8b4a0827ee00b1b0ab3968ef942f99")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("hdf5@1.14.0:", when="@1.4.0:")
    depends_on("mpi")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)

    def configure_args(self):
        return [
            "--enable-shared",
            "--enable-zlib",
            "--with-mpi={}".format(self.spec["mpi"].prefix),
        ]
