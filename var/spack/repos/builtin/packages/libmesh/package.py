# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Libmesh(AutotoolsPackage):
    """The libMesh library provides a framework for the numerical simulation of
    partial differential equations using arbitrary unstructured
    discretizations on serial and parallel platforms."""

    homepage = "https://libmesh.github.io/"
    url = "https://github.com/libMesh/libmesh/releases/download/v1.0.0/libmesh-1.0.0.tar.bz2"
    git = "https://github.com/libMesh/libmesh.git"

    license("LGPL-2.1-or-later")

    version("master", branch="master", submodules=True)

    version("1.7.1", sha256="0387d62773cf92356eb128ba92f767e56c298d78f4b97446e68bf288da1eb6b4")
    version("1.4.1", sha256="67eb7d5a9c954d891ca1386b70f138333a87a141d9c44213449ca6be69a66414")
    version("1.4.0", sha256="62d7fce89096c950d1b38908484856ea63df57754b64cde6582e7ac407c8c81d")
    version("1.3.1", sha256="638cf30d05c249315760f16cbae4804964db8857a04d5e640f37617bef17ab0f")
    version("1.3.0", sha256="a8cc2cd44f42b960989dba10fa438b04af5798c46db0b4ec3ed29591b8359786")
    version("1.2.1", sha256="11c22c7d96874a17de6b8c74caa45d6745d40bf3610e88b2bd28fd3381f5ba70")
    version("1.0.0", sha256="8909b0354e147fa50d176caa63ef22b02326d49250e964be23532d89432e727f")

    # support for libraries that are only available through the bundled copies:
    # TODO libMesh 1.2.1 gained the ability to specify a path to capnproto
    variant(
        "capnproto",
        default=False,
        description="Compile with the bundled capnproto serialization library",
    )
    variant(
        "exodusii", default=False, description="Compile with the bundled ExodusII output library"
    )
    variant("vtk", default=False, description="Compile with  VTK input/output library")
    variant(
        "fparser",
        default=False,
        description="Compile with the bundled fparser function parser library",
    )
    variant("gmv", default=False, description="Compile with the bundled gmv format IO library")
    variant(
        "laspack",
        default=False,
        description="Compile with the bundled laspack interative solver library",
    )
    variant(
        "libhilbert",
        default=False,
        description="Compile with the bundled libHilbert partitioning library",
    )
    variant(
        "metaphysicl", default=False, description="Compile with the bundled metaphysicl AD library"
    )
    variant("perflog", default=False, description="Compile with performance logging support")
    variant("blocked", default=False, description="Compile with support for blocked storage")
    variant(
        "metis",
        default=False,
        description="Compile with the bundled METIS graph partitioning library",
    )
    variant(
        "nanoflann", default=False, description="Compile with the bundled nanoflann graph library"
    )
    variant("nemesis", default=False, description="Compile with the bundled nemesis IO library")
    variant("netcdf", default=False, description="Compile with the bundled NETCDF IO library")
    # TODO the copy of parmetis bundled with libMesh assumes that we use the
    # bundled copy of metis, but previous versions of this build script use an
    # external metis installation. Be conservative and completely disable
    # parmetis support to preserve the old behavior (and to prevent compiling
    # with two different copies of metis).
    #
    # variant('parmetis', default=False,
    #         description='Compile with the bundled PARMETIS graph library')
    variant(
        "qhull",
        default=False,
        description="Compile with the bundled qhull mesh generation library",
    )
    variant(
        "sfc", default=False, description="Compile with the bundled sfcurves partitioning library"
    )
    variant(
        "tetgen",
        default=False,
        description="Compile with the bundled tetgen mesh generation library",
    )
    variant(
        "triangle",
        default=False,
        description="Compile with the bundled Triangle mesh generation library",
    )

    # support for libraries that may be externally installed:
    variant("boost", default=False, description="Compile with components dependent on boost")
    variant("eigen", default=False, description="support for dense linear algebra with Eigen")
    variant("hdf5", default=False, description="Compile with support for HDF5 files")
    variant("slepc", default=False, description="Compile with support for the SLEPc eigensolver")
    variant("petsc", default=False, description="Compile with support for the PETSc")

    # other features:
    variant("debug", default=False, description="Compile with support for debugging")
    variant("mpi", default=True, description="Enables MPI parallelism")
    # While it is possible to configure libMesh to use openMP with neither
    # pthreads nor TBB, no openMP code can actually be reached without enabling
    # pthreads as well. Hence, since enabling openMP while disabling pthreads
    # is not useful, we include openMP in the same variant to make it clear
    # which scheduler is ultimately used.
    variant(
        "threads",
        default="none",
        description="Enable threading support (with a particular "
        "scheduler, in the case of openmp and tbb)",
        values=("none", "pthreads", "tbb", "openmp"),
        multi=False,
    )
    variant("shared", default=True, description="Enables the build of shared libraries")

    conflicts(
        "+metaphysicl",
        when="@:1.2",
        msg="The interface to metaphysicl is not available in libMesh "
        "versions older than 1.3.0. Please explicitly disable this "
        "variant.",
    )

    depends_on("boost", when="+boost")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+boost")
    depends_on("eigen", when="+eigen")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+slepc")
    # compilation dependencies depend on perl
    depends_on("perl")
    depends_on("petsc+mpi", when="+petsc+mpi")
    depends_on("petsc+metis", when="+petsc+metis")
    depends_on("slepc", when="+slepc")
    depends_on("petsc", when="+petsc")
    depends_on("tbb", when="threads=tbb")
    depends_on("vtk", when="+vtk")

    def configure_args(self):
        options = []

        if self.spec.satisfies("+shared"):
            options.extend(["--enable-shared", "--disable-static"])
        else:
            options.extend(["--disable-shared", "--enable-static"])

        # GLIBCXX debugging is not, by default, supported by other libraries,
        # so unconditionally disable it for libmesh
        options.append("--enable-glibcxx-debugging=no")

        # All bundled dependencies are explicitly disabled, so we do not need
        # to perform this check:
        options.append("--disable-strict-lgpl")

        # The Hinnant unique pointer implementation is incompatible with boost
        # (and not necessary with C++11 support), so unconditionally disable
        # it:
        options.append("--disable-hinnant-unique-ptr")
        # libMesh does not allow for us to specify an installation location for
        # zlib, an undocumented dependency of gzstreams: hence we must
        # unconditionally disable gzstreams.
        options.append("--enable-gzstreams=no")
        # Similarly, since we cannot specify a location for bzip2 or xz, so
        # disable them to avoid picking up system installations:
        options.append("--disable-bzip2")
        options.append("--disable-xz")
        # TODO enable GDB backtracing. Disable for now to avoid picking up the
        # system gdb installation:
        options.append("--without-gdb-command")

        # TODO add X11 as a dependency to get tecplot working
        options.append("--enable-tecio=no")
        options.append("--enable-tecplot=no")

        # handle the bundled libraries that are not themselves dependencies of
        # other bundled libaries:
        for bundled_library in [
            "capnproto",
            "exodusii",
            "fparser",
            "gmv",
            "laspack",
            "libHilbert",
            "metaphysicl",
            "nanoflann",
            "nemesis",
            "parmetis",
            "qhull",
            "sfc",
            "tetgen",
            "triangle",
        ]:
            if "+" + bundled_library.lower() in self.spec:
                options.append("--enable-" + bundled_library + "=yes")
            else:
                options.append("--enable-" + bundled_library + "=no")

        # and the ones which are dependencies of other bundled libraries:
        if self.spec.satisfies("+exodusii") or self.spec.satisfies("+netcdf"):
            options.append("--enable-netcdf=yes")
        else:
            options.append("--enable-netcdf=no")

        if self.spec.satisfies("+vtk"):
            options.append("--enable-vtk")
            options.append("--with-vtk=%s" % self.spec["vtk"].prefix)
        else:
            options.append("--disable-vtk")

        # handle external library dependencies:
        if self.spec.satisfies("+boost"):
            options.append("--with-boost=%s" % self.spec["boost"].prefix)
        else:
            options.append("--enable-boost=no")

        if self.spec.satisfies("+eigen"):
            options.append("--with-eigen=%s" % self.spec["eigen"].prefix)
        else:
            options.append("--enable-eigen=no")

        if self.spec.satisfies("+metaphysicl"):
            options.append("--enable-metaphysicl")
        else:
            options.append("--disable-metaphysicl")

        if self.spec.satisfies("+perflog"):
            options.append("--enable-perflog")
        else:
            options.append("--disable-perflog")

        if self.spec.satisfies("+blocked"):
            options.append("--enable-blocked-storage")
        else:
            options.append("--disable-blocked-storage")

        if self.spec.satisfies("+hdf5"):
            options.append("--with-hdf5=%s" % self.spec["hdf5"].prefix)
        else:
            options.append("--enable-hdf5=no")
            # This is necessary with libMesh 1.2.1 to prevent a configure
            # error:
            if "+netcdf" not in self.spec:
                options.append("--disable-netcdf-4")

        if self.spec.satisfies("+metis"):
            options.append("--enable-metis")
            options.append("--enable-parmetis")
            if self.spec.satisfies("+petsc"):
                options.append("--with-metis=PETSc")
                options.append("--with-parmetis=PETSc")
        else:
            options.append("--disable-metis")

        if self.spec.satisfies("+petsc") or self.spec.satisfies("+slepc"):
            options.append("--enable-petsc=yes")
            options.append("PETSC_DIR=%s" % self.spec["petsc"].prefix)
        else:
            options.append("--enable-petsc=no")

        if self.spec.satisfies("+slepc"):
            options.append("--enable-slepc=yes")
            options.append("SLEPC_DIR=%s" % self.spec["slepc"].prefix)
        else:
            options.append("--enable-slepc=no")

        # and, finally, other things:
        if self.spec.satisfies("+debug"):
            options.append("--with-methods=dbg")
        else:
            options.append("--with-methods=opt")

        if self.spec.satisfies("+mpi"):
            options.append("CC=%s" % self.spec["mpi"].mpicc)
            options.append("CXX=%s" % self.spec["mpi"].mpicxx)
            options.append("--with-mpi=%s" % self.spec["mpi"].prefix)
        else:
            options.append("--disable-mpi")
            # libMesh will try to link with the system MPI library unless we
            # provide explicit overrides
            options.append("CC=%s" % self.compiler.cc)
            options.append("CXX=%s" % self.compiler.cxx)

        if self.spec.satisfies("threads=openmp"):
            # OpenMP cannot be used if pthreads is not available: see
            # parallel/threads_pthread.h and parallel/threads.h
            options.append("--enable-openmp=yes")
            options.append("--with-thread-model=pthread")
            options.append("--enable-pthreads=yes")
        else:
            options.append("--enable-openmp=no")

        if self.spec.satisfies("threads=pthreads"):
            options.append("--with-thread-model=pthread")
            options.append("--enable-pthreads=yes")
        else:
            if "threads=openmp" not in self.spec:
                options.append("--enable-pthreads=no")

        if self.spec.satisfies("threads=tbb"):
            options.append("--with-thread-model=tbb")
            options.append("--enable-tbb=yes")
            options.append("--with-tbb=%s" % self.spec["tbb"].prefix)
        else:
            options.append("--enable-tbb=no")

        return options

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.append_flags("PERL", self.spec["perl"].command.path)
