# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Examinimd(MakefilePackage):
    """ExaMiniMD is a proxy application and research vehicle for particle codes,
    in particular Molecular Dynamics (MD). Compared to previous MD proxy apps
    (MiniMD, COMD), its design is significantly more modular in order to allow
    independent investigation of different aspects. To achieve that the main
    components such as force calculation, communication, neighbor list
    construction and binning are derived classes whose main functionality is
    accessed via virtual functions. This allows a developer to write a new
    derived class and drop it into the code without touching much of the
    rest of the application."""

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://github.com/ECP-copa/ExaMiniMD"
    url = "https://github.com/ECP-copa/ExaMiniMD/archive/1.0.zip"
    git = "https://github.com/ECP-copa/ExaMiniMD.git"

    version("develop", branch="master")
    version("1.0", sha256="d5f884ecc3a5f9723cc57a4c188da926b392605650606c1c8c34f2d1953f2534")

    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("pthreads", default=False, description="Build with POSIX Threads support")
    # TODO: Set up cuda variant when test machine available

    conflicts("+openmp", when="+pthreads")

    depends_on("kokkos-legacy")
    depends_on("mpi", when="+mpi")

    @property
    def build_targets(self):
        targets = []
        # Append Kokkos
        targets.append("KOKKOS_PATH={0}".format(self.spec["kokkos-legacy"].prefix))
        # Set kokkos device
        if self.spec.satisfies("openmp"):
            targets.append("KOKKOS_DEVICES=OpenMP")
        elif self.spec.satisfies("pthreads"):
            targets.append("KOKKOS_DEVICES=Pthread")
        else:
            targets.append("KOKKOS_DEVICES=Serial")
        # Set MPI as needed
        if self.spec.satisfies("+mpi"):
            targets.append("MPI=1")
            targets.append("CXX = {0}".format(self.spec["mpi"].mpicxx))
        else:
            targets.append("MPI=0")
            targets.append("CXX = {0}".format(spack_cxx))
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("src/ExaMiniMD", prefix.bin)
        install_tree("input", prefix.input)
        mkdirp(prefix.docs)
        install("README.md", prefix.docs)
        install("LICENSE", prefix.docs)
