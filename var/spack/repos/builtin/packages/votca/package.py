# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Votca(CMakePackage):
    """VOTCA is a software package which focuses on the analysis of molecular
    dynamics data, the development of systematic coarse-graining techniques
    as well as methods used for simulating microscopic charge (and exciton)
    transport in disordered semiconductors.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/votca/tarball/v2022-rc.1"
    git = "https://github.com/votca/votca.git"
    maintainers("junghans")

    version("master", branch="master")
    version("2024.2", sha256="aa9ea3ad54dae31d3f68685d12f3bad4910ef3034a7f51c9ddd573b3856f4bc8")
    version("2024.1", sha256="68669a7d09020f780d2633eb865c6c53e5fb38d155f80c9670ebf9d10d10bee6")
    version("2024", sha256="7f342e857f4a6ba6d25937f63830afa3c32cbd906255c8d78aa6c500cfd418c8")
    version("2023", sha256="6150a38c77379d05592a56ae4392a00c4636d02198bb06108a3dc739a45115f8")
    version("2022.1", sha256="358119b2645fe60f88ca621aed508c49fb61f88d29d3e3fa24b5b831ed4a66ec")
    version("2022", sha256="7991137098ff4511f4ca2c6f1b6c45f53d92d9f84e5c0d0e32fbc31768f73a83")

    depends_on("cxx", type="build")  # generated

    variant("mkl", default=False, description="Build with MKL support")
    variant(
        "new-gmx", default=False, description="Build against gromacs>2019 - no tabulated kernels"
    )
    variant("xtp", default=True, description="Build xtp parts of votca")

    conflicts("votca-tools")
    conflicts("votca-csg")
    conflicts("votca-xtp")

    depends_on("cmake@3.13:", type="build")
    depends_on("expat")
    depends_on("fftw-api@3")
    depends_on("eigen@3.3:")
    depends_on("boost+filesystem+system+regex+timer")
    depends_on("boost@1.71:")
    depends_on("boost@1.71:1.84", when="@=2024")
    depends_on("boost@1.71:1.82", when="@:2023")
    depends_on("mkl", when="+mkl")
    depends_on("hdf5+cxx~mpi")
    depends_on("gromacs~mpi@5.1:")
    depends_on("gromacs~mpi@5.1:2019", when="~new-gmx")

    with when("+xtp"):
        depends_on("libxc")
        depends_on("libint@2.6.0:")
        depends_on("libecpint")
        depends_on("py-h5py")
        depends_on("py-lxml")

    depends_on("lammps", type="test")
    depends_on("py-espresso", type="test")
    depends_on("py-pytest", type="test")

    def cmake_args(self):
        args = [
            "-DINSTALL_RC_FILES=OFF",
            self.define_from_variant("BUILD_XTP", "xtp"),
            "-DBUILD_CSGAPPS=ON",
        ]

        if "~mkl" in self.spec:
            args.append("-DCMAKE_DISABLE_FIND_PACKAGE_MKL=ON")

        if self.run_tests:
            args.append("-DENABLE_TESTING=ON")
            args.append("-DENABLE_REGRESSION_TESTING=ON")

        return args
