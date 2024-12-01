# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Librom(AutotoolsPackage):
    """libROM: library for computing large-scale reduced order models"""

    homepage = "https://github.com/LLNL/libROM"
    git = "https://github.com/LLNL/libROM.git"

    license("Apache-2.0")

    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("lapack")
    depends_on("mpi")
    depends_on("zlib-api")
    depends_on("libszip")
    depends_on("hdf5")
    depends_on("perl")
    depends_on("graphviz")
    depends_on("doxygen")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-lapack={0}".format(spec["lapack"].prefix),
            "--with-lapack-libs={0}".format(spec["lapack"].libs.ld_flags),
            "--with-zlib={0}".format(spec["zlib-api"].prefix),
            "--with-szlib={0}".format(spec["libszip"].prefix),
            "--with-hdf5={0}".format(spec["hdf5"].prefix),
            "--with-MPICC={0}".format(spec["mpi"].mpicc),
            "--with-mpi-include={0}".format(spec["mpi"].prefix.include),
            "--with-mpi-libs={0}".format(spec["mpi"].libs.ld_flags),
            "--with-perl={0}".format(spec["perl"].prefix),
            "--with-doxygen={0}".format(spec["doxygen"].prefix),
        ]
        return args

    # TODO(oxberry1@llnl.gov): Submit PR upstream that implements
    # install phase in autotools
    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install("libROM.a", join_path(prefix.lib, "libROM.a"))

        mkdirp(prefix.include)
        install("*.h", prefix.include)

        mkdirp(prefix.share)
        install(
            "libROM_Design_and_Theory.pdf", join_path(prefix.share, "libROM_Design_and_Theory.pdf")
        )

        install_tree("docs", prefix.share.docs)
