# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Important feature: a version of salome-medcoupling depand on
# a specific version of salome-med package

from spack.package import *


class SalomeMedcoupling(CMakePackage):
    """salome-medcoupling is a part of SALOME platform to manipulate meshes and
    fields in memory, and use salome-med format for files."""

    maintainers("franciskloss")

    homepage = "https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/index.html"
    git = "https://git.salome-platform.org/gitpub/tools/medcoupling.git"

    license("LGPL-2.1-or-later")

    version("9.13.0", tag="V9_13_0", commit="8bea530c92cd907ae859ef11fd95b2db54b2894a")
    version("9.12.0", tag="V9_12_0", commit="28e485bde1c26dc835ec7acf449b1d519997ddce")
    version("9.11.0", tag="V9_11_0", commit="1b5fb5650409b0ad3a61da3215496f2adf2dae02")
    version("9.10.0", tag="V9_10_0", commit="fe2e38d301902c626f644907e00e499552bb2fa5")
    version("9.9.0", tag="V9_9_0", commit="5b2a9cc1cc18fffd5674a589aacf368008983b45")
    version("9.8.0", tag="V9_8_0", commit="8a82259c9a9228c54efeddd52d4afe6c0e397c30")
    version("9.7.0", tag="V9_7_0", commit="773434a7f2a5cbacc2f50e93ea6d6a48a157acd9")
    version("9.6.0", tag="V9_6_0", commit="2c14a65b40252770b3503945405f5bdb2f29f8e2")
    version("9.5.0", tag="V9_5_0", commit="dd75474d950baf8ff862b03cb1685f2a2d562846")
    version("9.4.0", tag="V9_4_0", commit="984fe46c4076f08f42ef43e290e3cd1aea5a8182")
    version("9.3.0", tag="V9_3_0", commit="32521cd6e5c113de5db7953a80149e5ab492120a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("static", default=False, description="Enable static library build")
    variant("mpi", default=False, description="Enable MPI")
    variant("int64", default=False, description="Use 64 bits indices")
    variant("partitioner", default=False, description="Enable partitioner")
    variant("metis", default=False, description="Enable Metis")
    variant("scotch", default=False, description="Enable Scotch")

    depends_on("libxml2@2.9.1:")
    depends_on("libtirpc")
    depends_on("cppunit")
    depends_on("python@3.6.5:")
    depends_on("py-scipy@0.19.1:", type=("build", "run"))
    depends_on("py-numpy@1.15.1:", type=("build", "run"))
    depends_on("boost+python+numpy@1.58.0:")
    depends_on("swig@3.0.12:", type="build")

    depends_on("metis@5.1.0:", when="+metis")
    depends_on("scotch@6.0.4:", when="+scotch")
    depends_on("mpi", when="+mpi")

    for _min_ver in range(3, 14):
        _ver = f"9.{_min_ver}.0"
        depends_on(f"salome-configuration@{_ver}", when=f"@{_ver}")

    for _mpi_variant in ("~mpi", "+mpi"):
        for _static_variant in ("~static", "+static"):
            for _int64_variant in ("~int64", "+int64"):
                depends_on(
                    f"salome-med@4.1.1{_mpi_variant}{_static_variant}{_int64_variant}",
                    when=f"@9.11.0:{_mpi_variant}{_static_variant}{_int64_variant}",
                )
                depends_on(
                    f"salome-med@4.1.0{_mpi_variant}{_static_variant}{_int64_variant}",
                    when=f"@9.5.0:9.10.0{_mpi_variant}{_static_variant}{_int64_variant}",
                )
                depends_on(
                    f"salome-med@4.0.0{_mpi_variant}{_static_variant}{_int64_variant}",
                    when=f"@9.3.0:9.4.0{_mpi_variant}{_static_variant}{_int64_variant}",
                )

    def check(self):
        pass

    def setup_build_environment(self, env):
        if "+metis" in self.spec:
            env.set("METIS_ROOT_DIR", self.spec["metis"].prefix)

        if "+scotch" in self.spec:
            env.set("SCOTCH_ROOT_DIR", self.spec["scotch"].prefix)

    def setup_run_environment(self, env):
        python_ver = self.spec["python"].version.up_to(2)
        env.prepend_path(
            "PYTHONPATH", join_path(self.prefix.lib, f"python{python_ver}", "site-packages")
        )

    def cmake_args(self):
        spec = self.spec
        options = []

        if "+static" in spec:
            options.extend(["-DMEDCOUPLING_BUILD_STATIC=ON"])
        else:
            options.extend(["-DMEDCOUPLING_BUILD_STATIC=OFF"])

        if "+mpi" in spec:
            options.extend(["-DMEDCOUPLING_USE_MPI=ON", "-DSALOME_USE_MPI=ON"])
        else:
            options.extend(["-DMEDCOUPLING_USE_MPI=OFF", "-DSALOME_USE_MPI=OFF"])

        if "+int64" in spec:
            options.extend(["-DMEDCOUPLING_USE_64BIT_IDS=ON"])
        else:
            options.extend(["-DMEDCOUPLING_USE_64BIT_IDS=OFF"])

        if "+partitioner" in spec:
            options.extend(["-DMEDCOUPLING_ENABLE_PARTITIONER=ON"])
        else:
            options.extend(["-DMEDCOUPLING_ENABLE_PARTITIONER=OFF"])

        if "+metis" in spec:
            options.extend(["-DMEDCOUPLING_ENABLE_PARTITIONER=ON"])
            options.extend(["-DMEDCOUPLING_PARTITIONER_METIS=ON"])
        else:
            options.extend(["-DMEDCOUPLING_PARTITIONER_METIS=OFF"])

        if "+scotch" in spec:
            options.extend(["-DMEDCOUPLING_ENABLE_PARTITIONER=ON"])
            options.extend(["-DMEDCOUPLING_PARTITIONER_SCOTCH=ON"])
        else:
            options.extend(["-DMEDCOUPLING_PARTITIONER_SCOTCH=OFF"])

        options.extend(
            [
                "-DMEDCOUPLING_BUILD_DOC=OFF",
                "-DMEDCOUPLING_ENABLE_PYTHON=ON",
                "-DMEDCOUPLING_ENABLE_RENUMBER=OFF",
                "-DMEDCOUPLING_PARTITIONER_PARMETIS=OFF",
                "-DMEDCOUPLING_PARTITIONER_PTSCOTCH=OFF",
                "-DMEDCOUPLING_MICROMED=OFF",
                "-DMEDCOUPLING_BUILD_TESTS=OFF",
            ]
        )

        return options
