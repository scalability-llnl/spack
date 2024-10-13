# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Fenics(CMakePackage):
    """FEniCS is organized as a collection of interoperable components
    that together form the FEniCS Project. These components include
    the problem-solving environment DOLFIN, the form compiler FFC, the
    finite element tabulator FIAT, the just-in-time compiler Instant / Dijitso,
    the code generation interface UFC, the form language UFL and a range of
    additional components."""

    homepage = "https://fenicsproject.org/"
    git = "https://bitbucket.org/fenics-project/dolfin.git"
    url = "https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-2019.1.0.post0.tar.gz"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-only")
    version("master", branch="master")
    version(
        "2019.1.0.post0", sha256="61abdcdb13684ba2a3ba4afb7ea6c7907aa0896a46439d3af7e8848483d4392f"
    )
    version(
        "2018.1.0.post1", sha256="425cc49b90e0f5c2ebdd765ba9934b1ada97e2ac2710d982d6d267a5e2c5982d"
    )
    # Pre 2018.1.0 versions are deprecated due to expected compatibility issues
    version(
        "2017.2.0.post0",
        sha256="d3c40cd8c1c882f517999c25ea4220adcd01dbb1d829406fce99b1fc40184c82",
        deprecated=True,
    )
    version(
        "2016.2.0",
        sha256="c6760996660a476f77889e11e4a0bc117cc774be0eec777b02a7f01d9ce7f43d",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    dolfin_versions = ["2019.1.0", "2018.1.0", "2017.2.0", "2016.2.0"]

    variant("python", default=True, description="Compile with Python interface")
    variant("hdf5", default=True, description="Compile with HDF5")
    variant("parmetis", default=True, description="Compile with ParMETIS")
    variant("scotch", default=True, description="Compile with Scotch")
    variant("petsc", default=True, description="Compile with PETSc")
    variant("slepc", default=True, description="Compile with SLEPc")
    variant("petsc4py", default=True, description="Use PETSC4py")
    variant("slepc4py", default=True, description="Use SLEPc4py")
    variant("trilinos", default=False, description="Compile with Trilinos")
    variant("suite-sparse", default=True, description="Compile with SuiteSparse solvers")
    variant("vtk", default=False, description="Compile with VTK")
    variant("qt", default=False, description="Compile with QT")
    variant("zlib", default=False, description="Compile with ZLIB")
    variant("mpi", default=True, description="Enables the distributed memory support")
    variant("openmp", default=True, description="Enables the shared memory support")
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("doc", default=False, description="Builds the documentation")
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Developer"),
    )

    # Conflics for PETSC4PY / SLEPC4PY
    conflicts("+petsc4py", when="~python")
    conflicts("+petsc4py", when="~petsc")
    conflicts("+slepc4py", when="~python")
    conflicts("+slepc4py", when="~slepc")

    # Patches
    # patch('petsc-3.7.patch', when='petsc@3.7:')

    patch("header_fix.patch", when="@2019.1.0.post0")
    # endian.hpp for byte order detection was removed with Boost 1.73,
    # use __BYTE_ORDER__ instead
    patch(
        "https://bitbucket.org/fenics-project/dolfin/issues/attachments/1116/fenics-project/dolfin/1602778118.04/1116/0001-Use-__BYTE_ORDER__-instead-of-removed-Boost-endian.h.patch",
        sha256="1cc69e612df18feb5ebdc78cd902cfefda5ffc077735f0b67a1dcb1bf82e63c9",
        when="@2019.1.0.post0",
    )
    patch("petsc_3_11.patch", when="@2018.1.0.post1")

    # enable extension support for fenics package
    extends("python", when="+python")

    # fenics python package dependencies
    for ver in dolfin_versions:
        wver = "@" + ver

        depends_on("py-fenics-fiat{0}".format(wver), type=("build", "run"), when=wver + "+python")

        if Version(ver) < Version("2018.1.0"):
            depends_on(
                "py-fenics-instant{0}".format(wver), type=("build", "run"), when=wver + "+python"
            )
        else:
            depends_on(
                "py-fenics-dijitso{0}".format(wver), type=("build", "run"), when=wver + "+python"
            )

        depends_on("py-fenics-ufl{0}".format(wver), type=("build", "run"), when=wver + "+python")
        if ver in ["2019.1.0", "2017.2.0"]:
            wver = "@" + ver + ".post0"
        depends_on("py-fenics-ffc{0}".format(wver), type=("build", "run"), when=wver + "+python")

    # Adding special case for master
    depends_on("py-fenics-fiat@2019.1.0", type=("build", "run"), when="@master+python")
    depends_on("py-fenics-dijitso@master", type=("build", "run"), when="@master+python")
    depends_on("py-fenics-ufl-legacy@main", type=("build", "run"), when="@master+python")
    depends_on("py-fenics-ffc@master", type=("build", "run"), when="@master+python")

    # package dependencies
    depends_on("python@3.5:", type=("build", "run"), when="+python")
    depends_on("eigen@3.2.0:")
    depends_on("pkgconfig", type="build")
    depends_on("zlib-api", when="+zlib")

    depends_on("boost+filesystem+program_options+system+iostreams+timer+regex+chrono")
    depends_on(
        "boost+filesystem+program_options+system+iostreams+timer+regex+chrono@1.68.0",
        when="@:2018",
    )

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    depends_on("mpi", when="+mpi")
    depends_on("hdf5@:1.10+hl+fortran", when="+hdf5+petsc")
    depends_on("hdf5@:1.10+hl", when="+hdf5~petsc")
    depends_on("metis+real64", when="+parmetis")
    depends_on("parmetis", when="+parmetis")
    depends_on("scotch~metis", when="+scotch~mpi")
    depends_on("scotch+mpi~metis", when="+scotch+mpi")
    depends_on("petsc", when="+petsc")
    depends_on("slepc", when="+slepc")
    depends_on("py-petsc4py@3.6:", when="+petsc+python")
    depends_on("trilinos", when="+trilinos")
    depends_on("vtk", when="+vtk")
    depends_on("suite-sparse", when="+suite-sparse")
    depends_on("qt", when="+qt")

    depends_on("py-pybind11@2.2.4", type=("build", "run"))
    depends_on("cmake@3.17.3:", type="build")

    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("py-pkgconfig", type=("build", "run"), when="+python")
    depends_on("py-sphinx@1.0.1:", when="+doc", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("DOLFIN_SKIP_BUILD_TESTS", True),
            self.define_from_variant("DOLFIN_ENABLE_OPENMP", "openmp"),
            self.define_from_variant("DOLFIN_ENABLE_CHOLMOD", "suite-sparse"),
            self.define_from_variant("DOLFIN_ENABLE_HDF5", "hdf5"),
            self.define_from_variant("HDF5_NO_FIND_PACKAGE_CONFIG_FILE", "hdf5"),
            self.define_from_variant("DOLFIN_ENABLE_MPI", "mpi"),
            self.define_from_variant("DOLFIN_ENABLE_PARMETIS", "parmetis"),
            self.define_from_variant("DOLFIN_ENABLE_PETSC", "petsc"),
            self.define_from_variant("DOLFIN_ENABLE_PETSC4PY", "petsc4py"),
            self.define_from_variant("DOLFIN_ENABLE_PYTHON", "python"),
            self.define_from_variant("DOLFIN_ENABLE_QT", "qt"),
            self.define_from_variant("DOLFIN_ENABLE_SCOTCH", "scotch"),
            self.define_from_variant("DOLFIN_ENABLE_SLEPC", "slepc"),
            self.define_from_variant("DOLFIN_ENABLE_SLEPC4PY", "slepc4py"),
            self.define_from_variant("DOLFIN_ENABLE_DOCS", "doc"),
            self.define_from_variant("DOLFIN_ENABLE_SPHINX", "doc"),
            self.define_from_variant("DOLFIN_ENABLE_TRILINOS", "trilinos"),
            self.define_from_variant("DOLFIN_ENABLE_UMFPACK", "suite-sparse"),
            self.define_from_variant("DOLFIN_ENABLE_VTK", "vtk"),
            self.define_from_variant("DOLFIN_ENABLE_ZLIB", "zlib"),
        ]

    # set environment for bulding python interface
    def setup_build_environment(self, env):
        env.set("DOLFIN_DIR", self.prefix)

    def setup_run_environment(self, env):
        env.set("DOLFIN_DIR", self.prefix)

    # build python interface of dolfin
    @run_after("install")
    def install_python_interface(self):
        if self.spec.satisfies("+python"):
            with working_dir("python"):
                args = std_pip_args + ["--prefix=" + self.prefix, "."]
                pip(*args)
