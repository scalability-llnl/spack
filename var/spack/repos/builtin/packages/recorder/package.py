# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Recorder(AutotoolsPackage):
    """A multi-level library for understanding I/O
    activity in HPC applications."""

    homepage = "https://github.com/uiuc-hpc/Recorder"
    url = "https://github.com/uiuc-hpc/Recorder/archive/v2.1.4.tar.gz"
    git = "https://github.com/uiuc-hpc/Recorder.git"

    maintainers("wangvsa")

    version("master", branch="master")
    version("pilgrim", branch="pilgrim")
    version("2.2.1", sha256="90634a580f075e9773cab4e46eb56459e917df1676b01655dec5f61e9d6b9bea")
    version("2.2.0", sha256="b47c208c18e615e0087486cc448f904d8ce7dbcc2535d06e185b5d28ad6e80f8")
    version("2.1.6", sha256="35985a0cb456d806952bf68f05127026f0dd8e26f70d725ae5cc37f109600889")
    version("2.1.5", sha256="6d2f8b942f61da498e25327e79c1a25b2244f4f78a9cf5482fb4aaa32d7332a1")
    version("2.1.4", sha256="f66756595a7f310929c247ae03fd08a18d9843f578fffa1e3072f557bf5a158e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("posix", default=True, description="Enable POSIX level tracing.")
    variant(
        "mpi",
        default=True,
        description="Enable MPI level tracing. MPI is required even with this option disabled.",
    )
    variant(
        "hdf5",
        default=True,
        description="Enable HDF5 level tracing. HDF5 is required even with this option disabled.",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mpi")
    depends_on("hdf5")

    def configure_args(self):
        args = []
        if "+posix" not in self.spec:
            args += ["--disable-posix"]
        if "+mpi" not in self.spec:
            args += ["--disable-mpi"]
        if "+hdf5" not in self.spec:
            args += ["--disable-hdf5"]

        return args
