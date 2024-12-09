# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pfapack(MakefilePackage):
    """A library for numerically computing the Pfaffian of
    a real or complex skew-symmetric matrix. This is based on
    computing the tridiagonal form of the matrix under
    unitary congruence transformations."""

    homepage = "https://michaelwimmer.org/downloads.html"
    url = "https://michaelwimmer.org/pfapack.tgz"

    version(
        "2014-09-17", sha256="b68fc35dda23ee24c358641b1a92ef701c4ffa0b3f0b0808b24e68afeb58ef07"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    parallel = False

    depends_on("lapack")
    depends_on("blas")
    depends_on("python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

    def edit(self, spec, prefix):
        filter_file("FORT =.*", "FORT = {0}".format(spack_fc), join_path("fortran", "makefile"))
        filter_file("CC =.*", "CC = {0}".format(spack_cc), join_path("c_interface", "makefile"))

    def build(self, spec, prefix):
        source_directory = self.stage.source_path
        with working_dir(join_path(source_directory, "fortran")):
            make()
        with working_dir(join_path(source_directory, "c_interface")):
            make()

    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        mkdirp(prefix.fortran)
        install(join_path(source_directory, "fortran", "libpfapack.a"), prefix.fortran)
        install(join_path(source_directory, "fortran", "*.mod"), prefix.fortran)
        install_tree(join_path(source_directory, "fortran", "EXAMPLES"), prefix.fortran.EXAMPLES)
        install_tree(join_path(source_directory, "fortran", "TESTING"), prefix.fortran.TESTING)
        mkdirp(prefix.c_interface)
        install(join_path(source_directory, "c_interface", "libcpfapack.a"), prefix.c_interface)
        install(join_path(source_directory, "c_interface", "fortran.h"), prefix.c_interface)
        install(
            join_path(source_directory, "c_interface", "fortran_pfapack.h"), prefix.c_interface
        )
        install(join_path(source_directory, "c_interface", "pfapack.h"), prefix.c_interface)
        install_tree(
            join_path(source_directory, "c_interface", "EXAMPLES"), prefix.c_interface.EXAMPLES
        )
        install_tree(
            join_path(source_directory, "c_interface", "TESTING"), prefix.c_interface.TESTING
        )
        install_tree(join_path(source_directory, "python"), prefix.python)
