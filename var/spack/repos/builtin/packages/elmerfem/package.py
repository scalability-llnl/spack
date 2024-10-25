# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Elmerfem(CMakePackage):
    """Elmer is an open source multiphysical simulation software. It
    includes physical models of fluid dynamics, structural mechanics,
    electromagnetics, heat transfer and acoustics."""

    homepage = "https://www.csc.fi/web/elmer"
    url = "https://github.com/ElmerCSC/elmerfem/archive/release-8.4.tar.gz"
    git = "https://github.com/ElmerCSC/elmerfem.git"

    version("ice", branch="elmerice")
    version("devel", branch="devel")
    version("9.0", sha256="08c5bf261e87ff37456c1aa0372db3c83efabe4473ea3ea0b8ec66f5944d1aa0")
    version("8.4", sha256="cc3ce807d76798361592cc14952cdc3db1ad8f9bac038017514033ce9badc5b3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("gui", default=False, description="Enable GUI support.")
    variant("mpi", default=True, description="Enable MPI support.")
    variant("openmp", default=True, description="Enable OpenMP support.")
    variant("mumps", default=False, description="Enable MUMPS support.")
    variant("hypre", default=False, description="Enable Hypre support.")
    variant("trilinos", default=False, description="Enable Trilinos support.")
    variant("zoltan", default=False, description="Enable Zoltan support.")
    variant("lua", default=False, description="Enable Lua support.")
    variant("scatt2d", default=False, description="Build Scattered2DDataInterpolator solver.")

    depends_on("qt@5:+opengl", when="+gui")
    depends_on("qwt", when="+gui")
    depends_on("paraview+qt", when="+gui")
    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack", when="+mpi")
    depends_on("mumps+openmp", when="+mumps+openmp")
    depends_on("mumps~openmp", when="+mumps~openmp")
    depends_on("hypre", when="+hypre")
    depends_on("trilinos~hypre~zoltan~zoltan2", when="+trilinos")
    depends_on("zoltan+fortran", when="+zoltan")
    depends_on("lua@5.1.5", when="+lua")
    depends_on("nn-c", when="+scatt2d")
    depends_on("csa-c", when="+scatt2d")

    def cmake_args(self):
        spec = self.spec

        args = ["-DWITH_ElmerIce=ON", "-DWITH_CONTRIB=ON"]

        if spec.satisfies("+gui"):
            args.append("-DWITH_ELMERGUI:BOOL=TRUE")
            args.append("-DWITH_QT5:BOOL=TRUE")
            args.append("-DWITH_QWT:BOOL=TRUE")
            args.append("-DWITH_PARAVIEW:BOOL=TRUE")
        else:
            args.append("-DWITH_ELMERGUI:BOOL=FALSE")

        if spec.satisfies("+mpi"):
            args.append("-DWITH_MPI=ON")
        else:
            args.append("-DWITH_MPI=OFF")

        if self.spec.satisfies("^intel-mkl"):
            args.append("-DWITH_MKL:BOOL=TRUE")

        if spec.satisfies("+openmp"):
            args.append("-DWITH_OpenMP=ON")
        else:
            args.append("-DWITH_OpenMP=OFF")

        if spec.satisfies("+mumps"):
            args.append("-DWITH_Mumps=ON")
        else:
            args.append("-DWITH_Mumps=OFF")

        if spec.satisfies("+hypre"):
            args.append("-DWITH_Hypre=ON")
        else:
            args.append("-DWITH_Hypre=OFF")

        if spec.satisfies("+trilinos"):
            args.extend(["-DWITH_Trilinos=ON", "-DCMAKE_CXX_STANDARD=11"])
        else:
            args.append("-DWITH_Trilinos=OFF")

        if spec.satisfies("+lua"):
            args.extend(["-DWITH_LUA=ON", "-DUSE_SYSTEM_LUA=ON"])
            if spec.satisfies("%gcc"):
                args.append("-DCMAKE_Fortran_FLAGS=-ffree-line-length-none")

        else:
            args.append("-DWITH_LUA=OFF")

        if spec.satisfies("+zoltan"):
            args.extend(["-DWITH_Zoltan=ON", "-DUSE_SYSTEM_ZOLTAN=ON"])
        else:
            args.append("-DWITH_Zoltan=OFF")

        if spec.satisfies("+scatt2d"):
            args.extend(
                [
                    "-DWITH_ScatteredDataInterpolator=ON",
                    "-DNN_LIBRARY=" + join_path(self.spec["nn-c"].prefix, "lib", "libnn.a"),
                    "-DNN_INCLUDE_DIR=" + join_path(self.spec["nn-c"].prefix, "include"),
                    "-DCSA_LIBRARY=" + join_path(self.spec["csa-c"].prefix, "lib", "libcsa.so"),
                    "-DCSA_INCLUDE_DIR=" + join_path(self.spec["csa-c"].prefix, "include"),
                ]
            )

        return args

    def patch(self):
        if self.spec.satisfies("@8.4"):
            # from commit f02cb33acd59 upstream
            filter_file(
                "FOREACH(D RANGE 1 depth)",
                "FOREACH(D RANGE 1 ${depth})",
                "fem/tests/CMakeLists.txt",
                string=True,
            )

    def setup_run_environment(self, env):
        env.set("ELMER_HOME", self.prefix)
        env.set("ELMER_Fortran_COMPILER", self.compiler.fc)
        if self.spec.satisfies("+gui"):
            env.set("ELMERGUI_HOME", self.prefix.share.ElmerGUI)
