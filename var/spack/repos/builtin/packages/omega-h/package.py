# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class OmegaH(CMakePackage, CudaPackage):
    """Omega_h is a C++11 library providing data structures and algorithms
    for adaptive discretizations. Its specialty is anisotropic triangle and
    tetrahedral mesh adaptation. It runs efficiently on most modern HPC
    hardware including GPUs.
    """

    homepage = "https://github.com/sandialabs/omega_h"
    url = "https://github.com/sandialabs/omega_h/archive/v9.34.1.tar.gz"
    git = "https://github.com/sandialabs/omega_h.git"

    maintainers("cwsmith")
    tags = ["e4s"]
    version("main", branch="main")
    version(
        "scorec.10.8.5",
        commit="62026fc305356abb5e02a9fce3fead9cf5077fbe",
        git="https://github.com/SCOREC/omega_h.git",
    )
    version(
        "scorec.10.7.0",
        commit="0e5de8618c3370f702e08c1b1af476dbbc118892",
        git="https://github.com/SCOREC/omega_h.git",
    )
    version(
        "scorec.10.6.0",
        commit="f376fad4741b55a4b2482218eb3437d719b7c72e",
        git="https://github.com/SCOREC/omega_h.git",
    )
    version(
        "scorec.10.1.0",
        commit="e88912368e101d940f006019585701a704295ab0",
        git="https://github.com/SCOREC/omega_h.git",
    )
    version("9.34.13", sha256="2eadfd6d634abc0b50396a82fd446f8f0b586ba6e64788c47827162c2aadec02")
    version("9.34.1", sha256="3a812da3b8df3e0e5d78055e91ad23333761bcd9ed9b2c8c13ee1ba3d702e46c")
    version("9.32.5", sha256="963a203e9117024cd48d829d82b8543cd9133477fdc15386113b594fdc3246d8")
    version("9.29.0", sha256="b41964b018909ffe9cea91c23a0509b259bfbcf56874fcdf6bd9f6a179938014")
    version("9.27.0", sha256="aa51f83508cbd14a41ae953bda7da98a6ad2979465c76e5b3a3d9a7a651cb34a")
    version("9.22.2", sha256="ab5636be9dc171a514a7015df472bd85ab86fa257806b41696170842eabea37d")
    version("9.19.1", sha256="60ef65c2957ce03ef9d1b995d842fb65c32c5659d064de002c071effe66b1b1f")
    version("9.19.0", sha256="4a1606c4e7287a1b67359cf6ef1c2d7e24b7dc379065566a1d2e0b0330c0abbd")
    version("9.15.0", sha256="342a506a0ff22f6cac759862efdcf34e360110f7901eb9b4c5de8afe38741522")
    version("9.14.0", sha256="035d0f47142f965a57818d1cb6c5c00b5ae6b5a0178b67b0bc9177fa99ba083d")
    version("9.13.14", sha256="f617dfd024c9cc323e56800ca23df3386bfa37e1b9bd378847d1f5d32d2b8e5d")
    version("9.13.13", sha256="753702edf4bda9ae57ea21f09ca071e341604a468d8c86468c9aebba049f581c")

    variant("shared", default=True, description="Build shared libraries")
    variant("mpi", default=True, description="Activates MPI support")
    variant("zlib", default=True, description="Activates ZLib support")
    variant("trilinos", default=True, description="Use Teuchos and Kokkos")
    variant("throw", default=False, description="Errors throw exceptions instead of abort")
    variant("examples", default=False, description="Compile examples")
    variant("optimize", default=True, description="Compile C++ with optimization")
    variant("symbols", default=True, description="Compile C++ with debug symbols")
    variant("warnings", default=False, description="Compile C++ with warnings")
    variant("gmsh", default=False, description="Use Gmsh C++ API")
    variant("kokkos", default=False, description="Use Kokkos")

    depends_on("cxx", type="build")
    depends_on("c", type="build", when="+mpi")

    depends_on("gmsh", when="+examples")
    depends_on("gmsh@4.4.1:", when="+gmsh")
    depends_on("mpi", when="+mpi")
    depends_on("trilinos +kokkos", when="+trilinos")
    depends_on("kokkos", when="+kokkos")
    depends_on("zlib-api", when="+zlib")
    # Note: '+cuda' and 'cuda_arch' variants are added by the CudaPackage
    depends_on("cuda", when="+cuda")
    conflicts(
        "^cuda@11.2",
        when="@scorec.10.1.0:",
        msg="Thrust is broken in CUDA = 11.2.* see https://github.com/sandialabs/omega_h/issues/366",
    )
    conflicts(
        "^cuda@:11.3",
        when="@scorec.10.8.5:",
        msg="see https://github.com/SCOREC/omega_h/issues/66",
    )

    # the sandia repo has a fix for cuda > 11.2 support
    #  see github.com/sandialabs/omega_h/pull/373
    conflicts(
        "^cuda@11.2",
        when="@:9.34.4",
        msg="Thrust is broken in CUDA = 11.2.* see https://github.com/sandialabs/omega_h/issues/366",
    )

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86610
    conflicts("%gcc@8:8.2", when="@:9.22.1")

    def patch(self):
        if "@:9.34.8" in self.spec:
            filter_file(
                r"OUTPUT_QUIET", "OUTPUT_VARIABLE Gmsh_VERSION_STRING", "cmake/FindGmsh.cmake"
            )

    def _bob_options(self):
        cmake_var_prefix = "Omega_h_CXX_"
        for variant in ["optimize", "symbols", "warnings"]:
            cmake_var = cmake_var_prefix + variant.upper()
            if "+" + variant in self.spec:
                yield "-D" + cmake_var + ":BOOL=ON"
            else:
                yield "-D" + cmake_var + ":BOOL=FALSE"

    def cmake_args(self):
        args = ["-DUSE_XSDK_DEFAULTS:BOOL=OFF"]
        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS:BOOL=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS:BOOL=OFF")
        if "+mpi" in self.spec:
            args.append("-DOmega_h_USE_MPI:BOOL=ON")
            ver = self.spec.version
            # old versions don't call find_package(MPI)
            if ver < Version("9.33.2") and "scorec" not in str(ver):
                args.append("-DCMAKE_CXX_COMPILER:FILEPATH={0}".format(self.spec["mpi"].mpicxx))
        else:
            args.append("-DOmega_h_USE_MPI:BOOL=OFF")
        if "+cuda" in self.spec:
            args.append("-DOmega_h_USE_CUDA:BOOL=ON")
            cuda_arch_list = self.spec.variants["cuda_arch"].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != "none":
                if "scorec" in str(self.spec.version):
                    args.append("-DOmega_h_CUDA_ARCH={0}".format(cuda_arch))
                else:
                    args.append("-DCMAKE_CUDA_FLAGS=-arch=sm_{0}".format(cuda_arch))
        else:
            args.append("-DOmega_h_USE_CUDA:BOOL=OFF")
        if "+trilinos" in self.spec:
            args.append("-DOmega_h_USE_Trilinos:BOOL=ON")
        if "+gmsh" in self.spec:
            args.append("-DOmega_h_USE_Gmsh:BOOL=ON")
        if "+kokkos" in self.spec:
            args.append("-DOmega_h_USE_Kokkos:BOOL=ON")
        if "+zlib" in self.spec:
            args.append("-DOmega_h_USE_ZLIB:BOOL=ON")
            args.append("-DZLIB_ROOT:PATH={0}".format(self.spec["zlib-api"].prefix))
        else:
            args.append("-DOmega_h_USE_ZLIB:BOOL=OFF")
        if "+examples" in self.spec:
            args.append("-DOmega_h_EXAMPLES:BOOL=ON")
        else:
            args.append("-DOmega_h_EXAMPLES:BOOL=OFF")
        if "+throw" in self.spec:
            args.append("-DOmega_h_THROW:BOOL=ON")
        else:
            args.append("-DOmega_h_THROW:BOOL=OFF")
        if "@:9.29.99" in self.spec:
            # omega-h requires empty CMAKE_BUILD_TYPE
            args.append("-DCMAKE_BUILD_TYPE:STRING=")
            args += list(self._bob_options())
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "cxxflags":
            flags.append(self.compiler.cxx11_flag)

            if self.spec.satisfies("%cce"):
                flags.append("-Wno-final-dtor-non-final-class")

        return (None, None, flags)

    def test_mesh(self):
        """test construction, adaptation, and conversion of a mesh"""
        if self.spec.satisfies("@:9.34.0") and not self.spec.satisfies("@:scorec"):
            raise SkipTest("Package must be installed as version 9.34.1 or later")

        with test_part(self, "test_mesh_create", purpose="mesh construction"):
            exe = which(self.prefix.bin.osh_box)
            exe("1", "1", "1", "2", "2", "2", "box.osh")

        with test_part(self, "test_mesh_adapt", purpose="mesh adaptation"):
            exe = which(self.prefix.bin.osh_scale)
            actual = exe("box.osh", "100", "box_100.osh", output=str.split, error=str.split)
            assert "adapting took" in actual

        with test_part(self, "test_mesh_convert", purpose="mesh to vtu conversion"):
            exe = which(self.prefix.bin.osh2vtk)
            exe("box_100.osh", "box_100_vtk")
