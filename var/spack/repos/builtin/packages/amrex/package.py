# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Amrex(CMakePackage, CudaPackage, ROCmPackage):
    """AMReX is a publicly available software framework designed
    for building massively parallel block- structured adaptive
    mesh refinement (AMR) applications."""

    homepage = "https://amrex-codes.github.io/amrex/"
    url = "https://github.com/AMReX-Codes/amrex/releases/download/23.05/amrex-23.05.tar.gz"
    git = "https://github.com/AMReX-Codes/amrex.git"

    test_requires_compiler = True

    tags = ["ecp", "e4s"]

    maintainers("WeiqunZhang", "asalmgren", "atmyers")

    license("BSD-3-Clause")

    version("develop", branch="development")
    version("24.10", sha256="a2d15e417bd7c41963749338e884d939c80c5f2fcae3279fe3f1b463e3e4208a")
    version("24.09", sha256="a1435d16532d04a1facce9a9ae35d68a57f7cd21a5f22a6590bde3c265ea1449")
    version("24.08", sha256="e09623e715887a19a1f86ed6fdb8335022fd6c03f19372d8f13b55cdeeadf5de")
    version("24.07", sha256="6baf76c1377d765e94020a9bd89dd1bf1485d0440d41cce2ba35d4dfee562580")
    version("24.06", sha256="103a97163d81716165fcff1af56df61741608b56f90730a725e9e4eb797bebf0")
    version("24.05", sha256="f3db5ea2b81973e3e244c5cf39d5a5383a98f297f56ed91c8dcdd2e24f7b750e")
    version("24.04", sha256="77a91e75ad0106324a44ca514e1e8abc54f2fc2d453406441c871075726a8167")
    version("24.03", sha256="024876fe65838d1021fcbf8530b992bff8d9be1d3f08a1723c4e2e5f7c28b427")
    version("24.02", sha256="286cc3ca29daa69c8eafc1cd7a572662dec9eb78631ac3d33a1260868fdc6996")
    version("24.01", sha256="83dbd4dad6dc51fa4a80aad0347b15ee5a6d816cf4abcd87f7b0e2987d8131b7")
    version("23.12", sha256="90e00410833d7a82bf6d9e71a70ce85d2bfb89770da7e34d0dda940f2bf5384a")
    version("23.11", sha256="49b9fea10cd2a2b6cb0fedf7eac8f7889eacc68a05ae5ac7c5702bc0eb1b3848")
    version("23.10", sha256="3c85aa0ad5f96303e797960a6e0aa37c427f6483f39cdd61dbc2f7ca16357714")
    version("23.09", sha256="1a539c2628041b17ad910afd9270332060251c8e346b1482764fdb87a4f25053")
    version("23.08", sha256="a83b7249d65ad8b6ac1881377e5f814b6db8ed8410ea5562b8ae9d4ed1f37c29")
    version("23.07", sha256="4edb991da51bcaad040f852e42c82834d8605301aa7eeb01cd1512d389a58d90")
    version("23.06", sha256="3bddcb07cce3e65e06cac35005c30820d311ce47ae54b46e4af333fa272b236b")
    version("23.05", sha256="a4bf5ad5322e706b9fae46ff52043e2cca5ddba81479647816251e9ab21c0027")
    version("23.04", sha256="b070949611abd2156208e675e40e5e73ed405bf83e3b1e8ba70fbb451a9e7dd7")
    version("23.03", sha256="e17c721b1aba4f66e467723f61b59e56c02cf1b72cab5a2680b13ff6e79ef903")
    version("23.02", sha256="f443c5eb4b89f4a74bf0e1b8a5943da18ab81cdc76aff12e8282ca43ffd06412")
    version("23.01", sha256="3b1770653a7c6d3e6167bc3cce98cbf838962102c510d1f872ab08f1115933b7")
    version("22.12", sha256="7b11e547e70bdd6f4b36682708a755d173eaecd8738536306d4217df4dd1be3d")
    version("22.11", sha256="8be9d5c6934d73b98c71c9c67ca7113f18794268f257333591d9b2449d7410c4")
    version("22.10", sha256="458da410d7f43e428726bfc905123e85d05786080f892ebaa26f94c5f8e79b07")
    version("22.09", sha256="24601fbb9d554f7b66d7db89b14ff95dadb18d51db893af7ee6c70d4b7dd4be6")
    version("22.08", sha256="d89167c4567fa246b06478a5b160010a0117dc58be9e879beb15be53cb08b6e9")
    version("22.07", sha256="7df433c780ab8429362df8d6d995c95d87a7c3f31ab81d5b0f416203dece086d")
    version("22.06", sha256="d8aa58e72c86a3da9a7be5a5947294fd3eaac6b233f563366f9e000d833726db")
    version("22.05", sha256="a760c7ca12915ca56b60d1f3c44103185db21ec2b8c01bc7b6762ff9c84e3f53")
    version("22.04", sha256="c33f5bdbc1ca21d8dd34b494a9c6c67a7eda4f42403cec3a7c13963f9140ebcf")
    version("22.03", sha256="2a67233e55f20b937e2da97f1ed3ab0666e12ef283b4d14c9456ebf21f36b77c")
    version("22.02", sha256="5d8dd3fa3c416b04e70188e06b7e8fc2838d78b43a2cf33a285184c77f0c1e1e")
    version("22.01", sha256="857df5b2fa8e3010b8856b81879a5be32ba7cc2e575474256eae7ef815b8354d")
    version("21.12", sha256="439f9ebf2b440fc739a7976f3ade188ec3e1de5f51a0b151e6b8dda36fa67278")
    version("21.11", sha256="2edb72d7cf7e86340fcaceb325368560957bcd952fd34cd501bfdf038e1338a4")
    version("21.10", sha256="a11954c03b1ec26c26b676460dc5de5195469e813b70fbcea6dfdefeafaf5407")
    version("21.09", sha256="983b41d93bf9417c032080fd2ec7c04d0d2b820e613a076bd07566aa5a8aa4bd")
    version("21.08", sha256="34fb6c72735c74820b27db1138e5bc9fe698ffbd8344aae10a5fbdace479b57f")
    version("21.07", sha256="9630b8c0c7ffbf3f5ea4d973a3fdb40b9b10fec0f8df33b9e24d76d2c1d15771")
    version("21.06", sha256="6982c22837d7c0bc4583065d9da55e0aebcf07b54386e4b90a779391fe73fd53")
    version("21.05", sha256="eb6d21e48279ad67278413c77b29a1754c18ffe741aa6b3a9f3f01eeac13177f")
    version("21.04", sha256="1c610e4b0800b16f7f1da74193ff11af0abfb12198b36a7e565a6a7f793087fa")
    version("21.03", sha256="6307bf75c80c2076bf5bd1cff4d12483280a32b5175fe117f32eed9c89cd1ac5")
    version("21.02", sha256="4a7ef997c43f9f03f1b06dd1aafa01218773a3265a5c1811f77eb4521b5e75b3")
    version("21.01", sha256="59de3ed429347ee6a7ad4f09c0c431248f2e081f59c301db37cacb36993622f4")
    version("20.12", sha256="a8ba1d605780250da77619939582ce44b33cd286f2dbcc0dfd5cdbaf209140a5")
    version("20.11", sha256="b86f4f2ebf414cec050e562d4ab81545944bda581b496d69767b4bf6a3060855")
    version("20.10", sha256="92def480d1f0bcb5bcb9dfae2ddc8997060414386a1d71ccbfdad785fa2e46fa")
    version("20.09", sha256="3ae203f18656117d8201da16e899a6144ec217817a2a5d9b7649e2eef9cacdf9")
    version("20.08", sha256="a202430cd8dbef2de29b20fe9b5881cc58ee762326556ec3c0ad9c3f85ddfc2f")
    version("20.07", sha256="c386f566f4c57ee56b5630f79ce2c6117d5a612a4aab69b7b26e48d577251165")
    version("20.06", sha256="be2f2a5107111fcb8b3928b76024b370c7cb01a9e5dd79484cf7fcf59d0b4858")
    version("20.05", sha256="97d753bb75e845a0a959ec1a044a48e6adb86dd008b5e29ce7a01d49ed276338")
    version("20.04", sha256="a7ece54d5d89cc00fd555551902a0d4d0fb50db15d2600f441353eed0dddd83b")
    version("20.03", sha256="9728f20c0d7297c935fe5cbc63c1ee60f983b833a735c797340ee2765d626165")
    version("20.02", sha256="2eda858b43e7455718ccb96c18f678da1778ec61031e90effdcb9c3e7e6f9bb5")
    version("20.01", sha256="957e7a7fe90a0a9f4ae10bf9e46dba68d72448d0bec69a4a4e66a544930caca3")
    version("19.10", sha256="9f30a2b3ec13711dfc6a1b59af59bd7df78449b5846ac6457b5dbbdecb20c576")
    version("19.08", sha256="94b1e9a9dcfb8c5b52aef91a2ed373aef504d766dd7d0aba6731ceb94e48e940")
    version("18.10.1", sha256="e648465c9c3b7ff4c696dfa8b6d079b4f61c80d96c51e27af210951c9367c201")
    version("18.10", sha256="298eba03ef03d617c346079433af1089d38076d6fab2c34476c687740c1f4234")
    version("18.09.1", sha256="a065ee4d1d98324b6c492ae20ea63ba12a4a4e23432bf5b3fe9788d44aa4398e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Config options
    variant(
        "dimensions",
        default="3",
        values=("1", "2", "3"),
        multi=False,
        description="Dimensionality",
        when="@:23.05",
    )
    variant(
        "dimensions",
        default="1,2,3",
        values=("1", "2", "3"),
        multi=True,
        description="Dimensionality",
        when="@23.06:",
    )
    variant("shared", default=False, description="Build shared library")
    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant(
        "precision",
        default="double",
        description="Real precision (double/single)",
        values=("single", "double"),
    )
    variant("ascent", default=False, description="Enable Ascent in situ visualization")
    variant(
        "catalyst",
        default=False,
        description="Enable Catalyst2 in situ visualization",
        when="@24.09:",
    )
    variant(
        "conduit",
        default=False,
        description="Enable Conduit for data exchange (in situ visualization)",
    )
    variant("eb", default=True, description="Build Embedded Boundary classes", when="@24.10:")
    variant("eb", default=False, description="Build Embedded Boundary classes", when="@:24.09")
    variant("fortran", default=False, description="Build Fortran API")
    variant("linear_solvers", default=True, description="Build linear solvers")
    variant("amrdata", default=False, description="Build data services")
    variant("particles", default=False, description="Build particle classes")
    variant("plotfile_tools", default=False, description="Build plotfile_tools like fcompare")
    variant("tiny_profile", default=False, description="Enable tiny profiling")
    variant("hdf5", default=False, description="Enable HDF5-based I/O")
    variant("hypre", default=False, description="Enable Hypre interfaces")
    variant("petsc", default=False, description="Enable PETSc interfaces")
    variant("sundials", default=False, description="Enable SUNDIALS interfaces")
    variant("pic", default=False, description="Enable PIC")
    variant("sycl", default=False, description="Enable SYCL backend")

    # Build dependencies
    depends_on("mpi", when="+mpi")
    with when("+ascent"):
        depends_on("ascent")
        depends_on("ascent +cuda", when="+cuda")
        depends_on("ascent +mpi", when="+mpi")
    with when("+conduit"):
        depends_on("conduit")
        depends_on("conduit +mpi", when="+mpi")
    with when("+catalyst"):
        depends_on("libcatalyst@2.0: +conduit")
        depends_on("libcatalyst +mpi", when="+mpi")
    with when("+sundials"):
        depends_on("sundials@4.0.0:4.1.0 +ARKODE +CVODE", when="@19.08:20.11")
        depends_on("sundials@5.7.0: +ARKODE +CVODE", when="@21.07:22.04")
        depends_on("sundials@6.0.0: +ARKODE +CVODE", when="@22.05:")
    for arch in CudaPackage.cuda_arch_values:
        depends_on(
            "sundials@5.7.0: +ARKODE +CVODE +cuda cuda_arch=%s" % arch,
            when="@21.07:22.04 +sundials +cuda cuda_arch=%s" % arch,
        )
        depends_on(
            "sundials@6.0.0: +ARKODE +CVODE +cuda cuda_arch=%s" % arch,
            when="@22.05: +sundials +cuda cuda_arch=%s" % arch,
        )
    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(
            "sundials@5.7.0: +ARKODE +CVODE +rocm amdgpu_target=%s" % tgt,
            when="@21.07:22.04 +sundials +rocm amdgpu_target=%s" % tgt,
        )
        depends_on(
            "sundials@6.0.0: +ARKODE +CVODE +rocm amdgpu_target=%s" % tgt,
            when="@22.05: +sundials +rocm amdgpu_target=%s" % tgt,
        )

    with when("+cuda"):
        depends_on("cuda@9.0.0:", when="@:22.04")
        depends_on("cuda@10.0.0:", when="@22.05:")
        depends_on("cuda@11.0.0:", when="@22.12:")
    depends_on("python@2.7:", type="build", when="@:20.04")
    depends_on("cmake@3.5:", type="build", when="@:18.10")
    depends_on("cmake@3.13:", type="build", when="@18.11:19.03")
    depends_on("cmake@3.14:", type="build", when="@19.04:22.05")
    depends_on("cmake@3.17:", type="build", when="@22.06:23.01")
    depends_on("cmake@3.18:", type="build", when="@23.02:")
    # cmake @3.17: is necessary to handle cuda @11: correctly
    depends_on("cmake@3.17:", type="build", when="^cuda @11:")
    depends_on("cmake@3.20:", type="build", when="+rocm")
    depends_on("cmake@3.22:", type="build", when="+sycl")
    depends_on("hdf5@1.10.4: +mpi", when="+hdf5")
    depends_on("rocrand", type="build", when="+rocm")
    depends_on("hiprand", type="build", when="+rocm")
    depends_on("rocprim", type="build", when="@21.05: +rocm")
    with when("+hypre"):
        depends_on("hypre@2.18.2:", type="link", when="@:21.02")
        depends_on("hypre@2.19.0:", type="link", when="@21.03: ~cuda")
        depends_on("hypre@2.20.0:", type="link", when="@21.03: +cuda")
    depends_on("petsc", type="link", when="+petsc")
    depends_on("intel-oneapi-mkl", type=("build", "link"), when="+sycl")

    # these versions of gcc have lambda function issues
    # see https://github.com/spack/spack/issues/22310
    conflicts("%gcc@8.1.0:8.3.0", when="@21.03")
    conflicts("%gcc@8.1.0:8.2.0", when="@21.01:21.02")

    # Check options compatibility
    conflicts(
        "+ascent", when="~conduit", msg="AMReX Ascent support needs Conduit interfaces (+conduit)"
    )
    conflicts(
        "+catalyst",
        when="~conduit",
        msg="AMReX Catalyst2 support needs Conduit interfaces (+conduit)",
    )
    conflicts(
        "+sundials",
        when="@19.08:20.11 ~fortran",
        msg="AMReX SUNDIALS support needs AMReX Fortran API (+fortran)",
    )
    conflicts(
        "+sundials",
        when="@20.12:21.06",
        msg="AMReX 20.12 -- 21.06 does not support SUNDIALS interfaces",
    )
    conflicts(
        "+hdf5", when="@:20.06", msg="AMReX HDF5 support needs AMReX newer than version 20.06"
    )
    conflicts(
        "+hypre", when="@:20.06", msg="AMReX Hypre support needs AMReX newer than version 20.06"
    )
    conflicts(
        "+hypre",
        when="@:20.07 ~fortran",
        msg="AMReX < 20.08 needs the Fortran API (+fortran) for Hypre support",
    )
    conflicts(
        "+hypre", when="~linear_solvers", msg="AMReX Hypre support needs variant +linear_solvers"
    )
    conflicts("+petsc", when="@:20.06", msg="PETSc support needs AMReX newer than version 20.06")
    conflicts(
        "+petsc",
        when="@:20.07 ~fortran",
        msg="AMReX < 20.08 needs the Fortran API (+fortran) for PETSc support",
    )
    conflicts(
        "+petsc", when="~linear_solvers", msg="AMReX PETSc support needs variant +linear_solvers"
    )
    conflicts(
        "+cuda", when="@:19.08", msg="AMReX CUDA support needs AMReX newer than version 19.08"
    )
    conflicts("cuda_arch=10", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=11", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=12", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=13", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=20", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=21", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=30", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=32", when="+cuda", msg="AMReX only supports compute capabilities >= 3.5")
    conflicts(
        "+rocm", when="@:20.11", msg="AMReX HIP support needs AMReX newer than version 20.11"
    )
    conflicts(
        "%rocm@4.2.0:4.2",
        when="+rocm",
        msg="AMReX does not support rocm-4.2 due to a compiler bug",
    )
    # GPU vendor support is mutually exclusive
    conflicts("+cuda", when="+rocm", msg="CUDA and HIP support are exclusive")
    conflicts("+cuda", when="+sycl", msg="CUDA and SYCL support are exclusive")
    conflicts("+rocm", when="+sycl", msg="HIP and SYCL support are exclusive")

    conflicts(
        "+sycl", when="@:21.05", msg="For SYCL support, AMReX version 21.06 and newer suggested."
    )

    def url_for_version(self, version):
        if version >= Version("20.05"):
            url = "https://github.com/AMReX-Codes/amrex/releases/download/{0}/amrex-{0}.tar.gz"
        else:
            url = "https://github.com/AMReX-Codes/amrex/archive/{0}.tar.gz"
        return url.format(version.dotted)

    def get_cuda_arch_string(self, values):
        if "none" in values:
            return "Auto"
        else:
            # Use format x.y instead of CudaPackage xy format
            vf = tuple(float(x) / 10.0 for x in values)
            return ";".join(str(x) for x in vf)

    #
    # For versions > 20.11
    #
    @when("@20.12:,develop")
    def cmake_args(self):
        if self.spec.satisfies("@23.01: +sycl") and not self.spec.satisfies("%oneapi@2023.0.0:"):
            raise InstallError("amrex +sycl requires %oneapi@2023.0.0:")
        args = [
            "-DUSE_XSDK_DEFAULTS=ON",
            self.define_from_variant("AMReX_SPACEDIM", "dimensions"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("AMReX_ASCENT", "ascent"),
            self.define_from_variant("AMReX_CATALYST", "catalyst"),
            self.define_from_variant("AMReX_CONDUIT", "conduit"),
            self.define_from_variant("AMReX_MPI", "mpi"),
            self.define_from_variant("AMReX_OMP", "openmp"),
            "-DXSDK_PRECISION:STRING=%s" % self.spec.variants["precision"].value.upper(),
            self.define_from_variant("XSDK_ENABLE_Fortran", "fortran"),
            self.define_from_variant("AMReX_FORTRAN_INTERFACES", "fortran"),
            self.define_from_variant("AMReX_EB", "eb"),
            self.define_from_variant("AMReX_LINEAR_SOLVERS", "linear_solvers"),
            self.define_from_variant("AMReX_AMRDATA", "amrdata"),
            self.define_from_variant("AMReX_PARTICLES", "particles"),
            self.define_from_variant("AMReX_PLOTFILE_TOOLS", "plotfile_tools"),
            self.define_from_variant("AMReX_TINY_PROFILE", "tiny_profile"),
            self.define_from_variant("AMReX_HDF5", "hdf5"),
            self.define_from_variant("AMReX_HYPRE", "hypre"),
            self.define_from_variant("AMReX_PETSC", "petsc"),
            self.define_from_variant("AMReX_SUNDIALS", "sundials"),
            self.define_from_variant("AMReX_PIC", "pic"),
        ]

        if self.spec.satisfies("%fj"):
            args.append("-DCMAKE_Fortran_MODDIR_FLAG=-M")

        if self.spec.satisfies("+cuda"):
            args.append("-DAMReX_GPU_BACKEND=CUDA")
            args.append("-DAMReX_CUDA_ERROR_CAPTURE_THIS=ON")
            args.append("-DAMReX_CUDA_ERROR_CROSS_EXECUTION_SPACE_CALL=ON")
            cuda_arch = self.spec.variants["cuda_arch"].value
            args.append("-DAMReX_CUDA_ARCH=" + self.get_cuda_arch_string(cuda_arch))

        if self.spec.satisfies("+rocm"):
            args.append("-DCMAKE_CXX_COMPILER={0}".format(self.spec["hip"].hipcc))
            args.append("-DAMReX_GPU_BACKEND=HIP")
            targets = self.spec.variants["amdgpu_target"].value
            args.append("-DAMReX_AMD_ARCH=" + ";".join(str(x) for x in targets))

        if self.spec.satisfies("+sycl"):
            args.append("-DAMReX_GPU_BACKEND=SYCL")
            # SYCL GPU backend only supported with Intel's oneAPI or DPC++ compilers
            sycl_compatible_compilers = ["icpx"]
            if not (os.path.basename(self.compiler.cxx) in sycl_compatible_compilers):
                raise InstallError(
                    "AMReX's SYCL GPU Backend requires the oneAPI CXX (icpx) compiler."
                )

        return args

    #
    # For versions <= 20.11
    #
    @when("@:20.11")
    def cmake_args(self):
        args = [
            "-DUSE_XSDK_DEFAULTS=ON",
            self.define_from_variant("DIM", "dimensions"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_OMP", "openmp"),
            "-DXSDK_PRECISION:STRING=%s" % self.spec.variants["precision"].value.upper(),
            self.define_from_variant("XSDK_ENABLE_Fortran", "fortran"),
            self.define_from_variant("ENABLE_FORTRAN_INTERFACES", "fortran"),
            self.define_from_variant("ENABLE_EB", "eb"),
            self.define_from_variant("ENABLE_LINEAR_SOLVERS", "linear_solvers"),
            self.define_from_variant("ENABLE_AMRDATA", "amrdata"),
            self.define_from_variant("ENABLE_PARTICLES", "particles"),
            self.define_from_variant("ENABLE_SUNDIALS", "sundials"),
            self.define_from_variant("ENABLE_HDF5", "hdf5"),
            self.define_from_variant("ENABLE_HYPRE", "hypre"),
            self.define_from_variant("ENABLE_PETSC", "petsc"),
            self.define_from_variant("ENABLE_CUDA", "cuda"),
        ]

        if self.spec.satisfies("%fj"):
            args.append("-DCMAKE_Fortran_MODDIR_FLAG=-M")

        if self.spec.satisfies("+cuda"):
            cuda_arch = self.spec.variants["cuda_arch"].value
            args.append("-DCUDA_ARCH=" + self.get_cuda_arch_string(cuda_arch))

        return args

    @run_after("build")
    def setup_standalone_test(self):
        """Setup stand-alonetests for AMReX versions from 21.12 on."""
        if self.spec.satisfies("@:21.11"):
            return

        cache_extra_test_sources(self, ["Tests"])

    def test_run_install_test(self):
        """build and run AmrCore test"""
        if self.spec.satisfies("@:21.11"):
            raise SkipTest("Test is not supported for versions @:21.11")

        args = ["-S{0}".format(join_path(".", "cache", "amrex", "Tests", "SpackSmokeTest"))]
        args.append("-DAMReX_ROOT=" + self.prefix)
        if self.spec.satisfies("+mpi"):
            args.append("-DMPI_C_COMPILER=" + self.spec["mpi"].mpicc)
            args.append("-DMPI_CXX_COMPILER=" + self.spec["mpi"].mpicxx)

        if self.spec.satisfies("+cuda"):
            args.append("-DCMAKE_CUDA_COMPILER=" + join_path(self.spec["cuda"].prefix.bin, "nvcc"))

        args.extend(self.cmake_args())
        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        cmake(*args)

        make = which("make")
        make()

        install_test = which("install_test")
        inputs_path = join_path(
            ".", "cache", "amrex", "Tests", "Amr", "Advection_AmrCore", "Exec", "inputs-ci"
        )
        out = install_test(inputs_path, output=str.split, error=str.split)
        assert "finalized" in out
