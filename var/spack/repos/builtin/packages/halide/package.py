# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Halide(CMakePackage, PythonExtension):
    """Halide is a programming language designed to make it easier to write
    high-performance image and array processing code on modern machines."""

    homepage = "https://halide-lang.org/"
    url = "https://github.com/halide/Halide/archive/refs/tags/v14.0.0.tar.gz"
    git = "https://github.com/halide/Halide.git"

    license("MIT")

    maintainers("wraith1995", "alexreinking")
    version("main", branch="main")
    version("18.0.0", sha256="1176b42a3e2374ab38555d9316c78e39b157044b5a8e765c748bf3afd2edb351")
    version("17.0.2", sha256="5f3a43ba27b47d3dcbcee963faabf1d633d4151031e60b6ff7cc62472e5677a0")
    version("17.0.1", sha256="beb18331d9e4b6f69943bcc75fb9d923a250ae689f09f6940a01636243289727")
    version("17.0.0", sha256="7e5a526b4074887b528d25b0265ddfa92c0a6d8bfdfbbba536313ecddf352da3")
    version("16.0.0", sha256="a0cccee762681ea697124b8172dd65595856d0fa5bd4d1af7933046b4a085b04")
    version("15.0.0", sha256="6680424f80c5731a85d977c06327096afe5af31da3667e91d4d36a25fabdda15")
    version("14.0.0", sha256="f9fc9765217cbd10e3a3e3883a60fc8f2dbbeaac634b45c789577a8a87999a01")
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Release", "Debug", "RelWithDebInfo"),
    )
    generator("ninja")
    variant("python", default=False, description="Install python bindings")
    variant("tutorials", default=False, description="Install the Halide Tutorials.")
    variant("utils", default=False, description="Install the Halide Utilities.")
    variant("tests", default=False, description="Build and Run Halide Tests and Apps.")
    variant("opencl", default=False, description="Build Non-llvm based OpenCl-C backend.")
    variant("metal", default=False, description="Build Non-llvm based Metal backend.")
    variant(
        "d3d12", default=False, description="Build Non-llvm based Direct3D 12 Compute backend."
    )
    extends("python", when="+python")
    _values = (
        "aarch64",
        "amdgpu",
        "arm",
        "hexagon",
        "nvptx",
        "powerpc",
        "riscv",
        "webassembly",
        "x86",
    )
    variant(
        "targets",
        default="arm,x86,nvptx,aarch64,hexagon,webassembly",
        description=("What targets to build. Spack's target family is always added "),
        values=_values,
        multi=True,
    )
    variant("sharedllvm", default=False, description="Link to the shared version of LLVM.")

    depends_on("cmake@3.22:", type="build")
    depends_on("llvm+clang+lld build_type=Release", type=("link", "run"))
    depends_on("llvm@14.0.0:14", type=("link", "run"), when="@14.0.0:14")
    depends_on("llvm@15.0.0:15", type=("link", "run"), when="@15.0.0:15")
    depends_on("llvm@16.0.0:16", type=("link", "run"), when="@16.0.0:16")
    depends_on("llvm@17.0.0:17", type=("link", "run"), when="@17.0.0:17")
    depends_on("llvm@17.0.0:18", type=("link", "run"), when="@18.0.0:18")

    for v in _values:
        depends_on(
            "llvm targets={0}".format(v), type=("link", "run"), when="targets={0}".format(v)
        )
    depends_on("llvm+llvm_dylib", type=("link", "run"), when="+sharedllvm")

    depends_on("libjpeg", type=("build", "link", "run"))
    depends_on("libpng", type=("build", "link", "run"))

    depends_on("python@3.8:", type=("build", "link", "run"), when="+python")
    # See https://github.com/halide/Halide/blob/main/requirements.txt
    depends_on("py-pybind11@2.6.2", type="build", when="@14.0.0:17+python")
    depends_on("py-pybind11@2.10.4", type="build", when="@18.0.0:+python")
    depends_on("py-setuptools@43:", type="build", when="+python")
    depends_on("py-scikit-build", type="build", when="+python")
    depends_on("py-wheel", type="build", when="+python")

    depends_on("py-imageio", type=("build", "run"), when="+python")
    depends_on("pil", type=("build", "run"), when="+python")
    depends_on("py-scipy", type=("build", "run"), when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")

    @property
    def libs(self):
        return find_libraries("libHalide", root=self.prefix, recursive=True)

    def cmake_args(self):
        # See https://github.com/halide/Halide/blob/main/README_cmake.md#building-halide-with-cmake
        spec = self.spec
        llvm_config = Executable(spec["llvm"].prefix.bin.join("llvm-config"))
        llvmdir = llvm_config("--cmakedir", output=str)
        args = [
            self.define("LLVM_DIR", llvmdir),
            self.define_from_variant("WITH_TESTS", "tests"),
            self.define_from_variant("WITH_TUTORIALS", "tutorials"),
            self.define_from_variant("WITH_UTILS", "utils"),
            self.define_from_variant("WITH_PYTHON_BINDINGS", "python"),
            self.define_from_variant("Halide_SHARED_LLVM", "sharedllvm"),
            self.define("WITH_WABT", False),
            self.define_from_variant("TARGET_OPENCL", "opencl"),
            self.define_from_variant("TARGET_METAL", "metal"),
            self.define_from_variant("TARGET_D3D12COMPUTE", "d3d12"),
        ]
        llvm_targets = get_llvm_targets_to_build(spec)
        for target in llvm_targets:
            args += [self.define("TARGET_{0}".format(target[0]), target[1])]

        if spec.satisfies("+python"):
            args += [
                self.define("PYBIND11_USE_FETCHCONTENT", False),
                self.define("Halide_INSTALL_PYTHONDIR", python_platlib),
            ]
        return args


def get_llvm_targets_to_build(spec):
    targets = spec.variants["targets"].value
    llvm_targets = set()
    # Convert targets variant values to CMake LLVM_TARGETS_TO_BUILD array.
    spack_to_cmake = {
        "aarch64": "AARCH64",
        "amdgpu": "AMDGPU",
        "arm": "ARM",
        "hexagon": "HEXAGON",
        "nvptx": "NVPTX",
        "powerpc": "POWERPC",
        "riscv": "RISCV",
        "webassembly": "WEBASSEMBLY",
        "x86": "X86",
    }
    for t in targets:
        llvm_targets.add((spack_to_cmake[t], True))

    if spec.target.family in ("x86", "x86_64"):
        llvm_targets.add(("X86", True))
    elif spec.target.family == "arm":
        llvm_targets.add(("ARM", True))
    elif spec.target.family == "aarch64":
        llvm_targets.add(("AARCH64", True))
    elif spec.target.family in ("ppc64", "ppc64le", "ppc", "ppcle"):
        llvm_targets.add(("POWERPC", True))

    # for everything not represented, we add False
    for v in spack_to_cmake.values():
        if (v, True) not in llvm_targets:
            llvm_targets.add((v, False))

    return list(llvm_targets)
