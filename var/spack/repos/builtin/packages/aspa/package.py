# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Aspa(MakefilePackage):
    """A fundamental premise in ExMatEx is that scale-bridging performed in
    heterogeneous MPMD materials science simulations will place important
    demands upon the exascale ecosystem that need to be identified and
    quantified.
    """

    homepage = "http://www.exmatex.org/aspa.html"
    git = "https://github.com/exmatex/ASPA.git"

    tags = ["proxy-app"]

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI Support")

    depends_on("lapack")
    depends_on("blas")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5")

    patch("fix_common_errors.patch")

    @property
    def build_targets(self):
        targets = [
            "--directory=exec",
            "--file=Makefile",
            "LIBS={} {} {}".format(
                self.spec["lapack"].libs.ld_flags,
                self.spec["blas"].libs.ld_flags,
                self.spec["hdf5"].libs.ld_flags,
            ),
            f"CXX={self.spec['mpi'].mpicxx}",
        ]
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)
        mkdirp(prefix.input)
        install("exec/aspa", prefix.bin)
        install("exec/README", prefix.doc)
        install("exec/aspa.inp", prefix.input)
        install("exec/kriging_model_centers.txt", prefix.input)
        install("exec/point_data.txt", prefix.input)
        install("exec/value_data.txt", prefix.input)
        install("doc/*.*", prefix.doc)
