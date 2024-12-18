# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kripke(CMakePackage, CudaPackage, ROCmPackage):
    """Kripke is a simple, scalable, 3D Sn deterministic particle
    transport proxy/mini app.
    """

    homepage = "https://computing.llnl.gov/projects/co-design/kripke"
    git = "https://github.com/LLNL/Kripke.git"

    tags = ["proxy-app"]

    maintainers("vsrana01")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=False)
    version(
        "1.2.7", submodules=True, tag="v1.2.7", commit="ddcac43cdad999f0346eb682065ef0af1847029d"
    )
    version(
        "1.2.6", submodules=True, tag="v1.2.6", commit="55b39f34b68c68b2d828a33a75568abd66e1019f"
    )
    version(
        "1.2.5", submodules=True, tag="v1.2.5", commit="20e9ea975f1bf567829323a18927b69bed3f4ebd"
    )
    version(
        "1.2.4", submodules=False, tag="v1.2.4", commit="d85c6bc462f17a2382b11ba363059febc487f771"
    )
    version(
        "1.2.3", submodules=True, tag="v1.2.3", commit="66046d8cd51f5bcf8666fd8c810322e253c4ce0e"
    )
    version(
        "1.2.2",
        submodules=True,
        tag="v1.2.2-CORAL2",
        commit="a12bce71e751f8f999009aa2fd0839b908b118a4",
    )
    version(
        "1.2.1",
        submodules=True,
        tag="v1.2.1-CORAL2",
        commit="c36453301ddd684118bb0fb426cfa62764d42398",
    )
    version(
        "1.2.0",
        submodules=True,
        tag="v1.2.0-CORAL2",
        commit="67e4b0a2f092009d61f44b5122111d388a3bec2a",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI.")
    variant("openmp", default=False, description="Build with OpenMP enabled.")
    variant("caliper", default=False, description="Build with Caliper support enabled.")

    depends_on("mpi", when="+mpi")
    depends_on("blt", type="build")
    depends_on("caliper", when="+caliper")
    depends_on("adiak@0.4:", when="+caliper")
    depends_on("chai~examples+raja")
    depends_on("raja@:2024.02.1~exercises~examples")
    depends_on("umpire~examples")

    with when("+rocm @1.2.5:"):
        depends_on("raja+rocm", when="+rocm")
        depends_on("chai+rocm", when="+rocm")
        for arch in ROCmPackage.amdgpu_targets:
            depends_on(
                "raja+rocm amdgpu_target={0}".format(arch), when="amdgpu_target={0}".format(arch)
            )
            depends_on(
                "chai+rocm amdgpu_target={0}".format(arch), when="amdgpu_target={0}".format(arch)
            )

    conflicts("^blt@:0.3.6", when="+rocm")

    # googletest folder version hasn't been updated in over 5 years
    # and is commented out in later releases
    patch("001-remove-googletest-from-cmake.patch", when="@1.2.5:1.2.6")

    def cmake_args(self):
        spec = self.spec
        args = []

        args.extend(
            [
                "-DCAMP_DIR=%s" % self.spec["camp"].prefix,
                "-DBLT_SOURCE_DIR=%s" % self.spec["blt"].prefix,
                "-Dumpire_DIR=%s" % self.spec["umpire"].prefix,
                "-DRAJA_DIR=%s" % self.spec["raja"].prefix,
                "-Dchai_DIR=%s" % self.spec["chai"].prefix,
                "-DENABLE_CHAI=ON",
            ]
        )

        if spec.satisfies("+caliper"):
            args.append("-DENABLE_CALIPER=ON")

        if spec.satisfies("+mpi"):
            args.append("-DENABLE_MPI=ON")
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx))

        if spec.satisfies("+rocm"):
            # Set up the hip macros needed by the build
            args.append("-DENABLE_HIP=ON")
            args.append("-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix))
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            rocm_archs = spec.variants["amdgpu_target"].value
            if "none" not in rocm_archs:
                args.append("-DHIP_HIPCC_FLAGS=--amdgpu-target={0}".format(",".join(rocm_archs)))
                args.append("-DCMAKE_HIP_ARCHITECTURES={0}".format(rocm_archs))
        else:
            # Ensure build with hip is disabled
            args.append("-DENABLE_HIP=OFF")

        if spec.satisfies("+cuda"):
            args.append("-DENABLE_CUDA=ON")
            args.append(self.define("CMAKE_CUDA_HOST_COMPILER", self.spec["mpi"].mpicxx))
            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                args.append("-DCUDA_ARCH={0}".format(cuda_arch[0]))
                args.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch[0]))
                args.append(
                    "-DCMAKE_CUDA_FLAGS=--expt-extended-lambda -I%s -I=%s"
                    % (self.spec["cub"].prefix.include, self.spec["mpi"].prefix.include)
                )
        else:
            args.append("-DENABLE_CUDA=OFF")

        return args

    def install(self, spec, prefix):
        # Kripke does not provide install target, so we have to copy
        # things into place.
        mkdirp(prefix.bin)
        if spec.satisfies("@:1.2.4") or spec.satisfies("@1.2.7:"):
            install(join_path(self.build_directory, "kripke.exe"), prefix.bin)
        else:
            install(join_path(self.build_directory, "bin", "kripke.exe"), prefix.bin)
