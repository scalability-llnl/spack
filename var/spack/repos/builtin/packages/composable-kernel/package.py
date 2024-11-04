# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class ComposableKernel(CMakePackage):
    """Composable Kernel: Performance Portable Programming Model
    for Machine Learning Tensor Operators."""

    homepage = "https://github.com/ROCm/composable_kernel"
    git = "https://github.com/ROCm/composable_kernel.git"
    url = "https://github.com/ROCm/composable_kernel/archive/refs/tags/rocm-6.1.2.tar.gz"
    maintainers("srekolam", "afzpatel")

    license("MIT")

    version("master", branch="develop")
    version("6.2.1", sha256="708ff25218dc5fa977af4a37105b380d7612a70c830fa7977b40b3df8b8d3162")
    version("6.2.0", sha256="4a3024f4f93c080db99d560a607ad758745cd2362a90d0e8f215331686a6bc64")
    version("6.1.2", sha256="54db801e1c14239f574cf94dd764a2f986b4abcc223393d55c49e4b276e738c9")
    version("6.1.1", sha256="f55643c6eee0878e8f2d14a382c33c8b84af0bdf8f31b37b6092b377f7a9c6b5")
    version("6.1.0", sha256="355a4514b96b56aa9edf78198a3e22067e7397857cfe29d9a64d9c5557b9f83d")
    version("6.0.2", sha256="f648a99388045948b7d5fbf8eb8da6a1803c79008b54d406830b7f9119e1dcf6")
    version("6.0.0", sha256="a8f736f2f2a8afa4cddd06301205be27774d85f545429049b4a2bbbe6fcd67df")
    version("5.7.1", sha256="75f66e023c2e31948e91fa26366eaeac72d871fc2e5188361d4465179f13876e")
    version("5.7.0", sha256="d9624dbaef04e0138f9f73596c49b4fe9ded69974bae7236354baa32649bf21a")
    version("5.6.1", commit="f5ec04f091fa5c48c67d7bacec36a414d0be06a5")
    version("5.6.0", commit="f5ec04f091fa5c48c67d7bacec36a414d0be06a5")
    version("5.5.1", commit="ac9e01e2cc3721be24619807adc444e1f59a9d25")
    version("5.5.0", commit="8b76b832420a3d69708401de6607a033163edcce")
    with default_args(deprecated=True):
        version("5.4.3", commit="bb3d9546f186e39cefedc3e7f01d88924ba20168")
        version("5.4.0", commit="236bd148b98c7f1ec61ee850fcc0c5d433576305")

    depends_on("cxx", type="build")  # generated

    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
        description="set gpu targets",
    )

    depends_on("python", type="build")
    depends_on("z3", type="build")
    depends_on("zlib", type="build")
    depends_on("ncurses+termlib", type="build")
    depends_on("bzip2", type="build")
    depends_on("sqlite", type="build")
    depends_on("half", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("cmake@3.16:", type="build")

    for ver in [
        "master",
        "6.2.1",
        "6.2.0",
        "6.1.2",
        "6.1.1",
        "6.1.0",
        "6.0.2",
        "6.0.0",
        "5.7.1",
        "5.7.0",
        "5.6.1",
        "5.6.0",
        "5.5.1",
        "5.5.0",
        "5.4.3",
        "5.4.0",
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        depends_on("rocm-cmake@" + ver, when="@" + ver, type="build")

    # Build is breaking on warning, -Werror, -Wunused-parameter. The patch is part of:
    # https://github.com/ROCm/composable_kernel/commit/959073842c0db839d45d565eb260fd018c996ce4
    patch("0001-mark-kernels-maybe-unused.patch", when="@6.2")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define(
                "CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(spec["llvm-amdgpu"].prefix)
            ),
            self.define("CMAKE_C_COMPILER", "{0}/bin/clang".format(spec["llvm-amdgpu"].prefix)),
            self.define("CMAKE_BUILD_TYPE", "Release"),
        ]
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("GPU_TARGETS", "amdgpu_target"))
        else:
            args.append(self.define("INSTANCES_ONLY", "ON"))
        if self.spec.satisfies("@5.6.0:"):
            if self.run_tests:
                args.append(self.define("BUILD_TESTING", "ON"))
            args.append(self.define("CK_BUILD_JIT_LIB", "ON"))
            args.append(self.define("CMAKE_POSITION_INDEPENDENT_CODE", "ON"))
        if self.spec.satisfies("@:5.7"):
            args.append(self.define("CMAKE_CXX_FLAGS", "-O3"))
        if self.spec.satisfies("@6.2:"):
            args.append(self.define("BUILD_DEV", "OFF"))
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            # only instances is necessary to build and install
            if self.spec.satisfies("@5.6.0:"):
                make()
            else:
                make("instances")
