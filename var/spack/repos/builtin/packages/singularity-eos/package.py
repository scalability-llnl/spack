# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack
import spack.version
from spack.error import SpackError
from spack.package import *


def plugin_validator(pkg_name, variant_name, values):
    if values == ("none",):
        return
    for v in values:
        if v not in SingularityEos.plugins:
            raise SpackError(f"Unknown Singularity-EOS plugin '{v}'")


class SingularityEos(CMakePackage, CudaPackage, ROCmPackage):
    """Singularity-EOS: A collection of closure models and tools useful for
    multiphysics codes."""

    homepage = "https://lanl.github.io/singularity-eos/main/index.html"
    git = "https://github.com/lanl/singularity-eos.git"
    url = "https://github.com/lanl/singularity-eos/archive/refs/tags/release-1.6.1.tar.gz"

    maintainers("rbberger")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("1.9.1", sha256="148889e1b2d5bdc3d59c5fd6a6b5da25bb4f4f0f4343c57b3ccaf96691c93aff")
    version("1.9.0", sha256="460b36a8311df430e6d4cccf3e72a6b3afda7db8d092b4a0a4259c4363c4dbde")
    version("1.8.0", sha256="1f1ec496f714aa23cc7003c88a85bd10d0e53e37659ba7310541248e48a66558")
    version("1.7.0", sha256="ce0825db2e9d079503e98cecf1c565352be696109042b3a0941762b35f36dc49")
    # build with kokkos, kokkos-kernels for offloading support
    variant("kokkos", default=False, description="Enable kokkos")
    variant(
        "kokkos-kernels", default=False, description="Enable kokkos-kernals for linear algebra"
    )

    # for compatibility with downstream projects
    variant("mpi", default=False, description="Build with MPI support")

    # build converters for sesame, stellarcollapse eos's
    variant(
        "build_extra",
        description="Build converters",
        values=any_combination_of("sesame", "stellarcollapse").with_default("none"),
    )

    # build the Fortran interface
    variant("fortran", default=True, description="Enable building fortran interface")

    # build the Python bindings
    variant("python", default=False, description="Enable building Python bindings")

    variant("eospac", default=True, description="Enable EOSPAC for table reads")

    variant("hdf5", default=False, description="Enable HDF5 support")

    variant("spiner", default=True, description="Use Spiner")

    variant("closure", default=True, description="Build closure module")
    variant("shared", default=False, description="Build shared libs")

    plugins = {"dust": ("self", "example/plugin")}

    variant(
        "plugins",
        multi=True,
        default="none",
        validator=plugin_validator,
        description="list of plugins to build",
        when="@1.9.0:",
    )
    variant(
        "variant",
        default="default",
        description="include path used for variant header",
        when="@1.9.0:",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")
    # building/testing/docs
    depends_on("cmake@3.19:", type="build")
    depends_on("python@3:", when="+python")
    depends_on("py-pybind11@2.9.1:", when="+python")
    depends_on("catch2@2.13.7", when="@:1.8.0", type="test")
    depends_on("catch2@3.0.1:", when="@1.9.0:", type="test")
    depends_on("py-numpy", when="+python", type="test")

    # linear algebra when not using GPUs
    depends_on("eigen@3.3.8:", when="~kokkos-kernels")
    requires("+kokkos-kernels", when="+cuda")
    requires("+kokkos-kernels", when="+rocm")

    depends_on("eospac", when="+eospac")

    depends_on("ports-of-call@1.4.2,1.5.2:", when="@:1.7.0")
    depends_on("ports-of-call@1.5.2:", when="@1.7.1:")
    depends_on("ports-of-call@1.6.0:", when="@1.9.0:")
    depends_on("ports-of-call@main", when="@main")

    depends_on("spiner +kokkos", when="+kokkos+spiner")
    depends_on("spiner +hdf5", when="+hdf5+spiner")

    depends_on("spiner@:1.6.0", when="@:1.7.0 +spiner")
    depends_on("spiner@1.6.1:", when="@1.8.0: +spiner")
    depends_on("spiner@main", when="@main +spiner")

    depends_on("mpark-variant")
    depends_on(
        "mpark-variant",
        patches=patch(
            "https://raw.githubusercontent.com/lanl/singularity-eos/refs/heads/main/utils/gpu_compatibility.patch",
            sha256="c803670cbd95f9b97458fb4ef403de30229ec81566a5b8e5ccb75ad9d0b22541"
        ),
        when="+cuda",
    )
    depends_on("binutils@:2.39,2.42:+ld", when="build_type=Debug")
    depends_on("binutils@:2.39,2.42:+ld", when="build_type=RelWithDebInfo")
    depends_on(
        "mpark-variant",
        patches=patch(
            "https://raw.githubusercontent.com/lanl/singularity-eos/refs/heads/main/utils/gpu_compatibility.patch",
            sha256="c803670cbd95f9b97458fb4ef403de30229ec81566a5b8e5ccb75ad9d0b22541",
        ),
        when="+rocm",
    )

    for _myver, _kver in zip(("@1.7.0:",), ("@3.3:",)):
        depends_on("kokkos" + _kver, when=_myver + "+kokkos")
        depends_on("kokkos-kernels" + _kver, when=_myver + "+kokkos-kernels")

    # set up kokkos offloading dependencies
    for _flag in ("~cuda", "+cuda", "~rocm", "+rocm"):
        depends_on("kokkos" + _flag, when="+kokkos" + _flag)

    for _flag in ("~cuda", "+cuda"):
        depends_on("kokkos-kernels" + _flag, when="+kokkos-kernels" + _flag)

    depends_on("kokkos+pic", when="+kokkos-kernels")

    # specfic specs when using GPU/cuda offloading
    depends_on("kokkos +wrapper+cuda_lambda", when="+cuda+kokkos")

    # fix for older spacks
    if spack.version.Version(spack.spack_version) >= spack.version.Version("0.17"):
        depends_on("kokkos-kernels", when="+kokkos-kernels")

    for _flag in list(CudaPackage.cuda_arch_values):
        depends_on("kokkos cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag)
        depends_on("kokkos-kernels cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag)

    for _flag in ROCmPackage.amdgpu_targets:
        depends_on("kokkos amdgpu_target=" + _flag, when="+rocm+kokkos amdgpu_target=" + _flag)

    conflicts("cuda_arch=none", when="+cuda", msg="CUDA architecture is required")
    conflicts("amdgpu_target=none", when="+rocm", msg="ROCm architecture is required")

    # these are mirrored in the cmake configuration
    conflicts("+cuda", when="~kokkos")
    conflicts("+rocm", when="~kokkos")
    conflicts("+kokkos-kernels", when="~kokkos")
    conflicts("+hdf5", when="~spiner")

    conflicts("+fortran", when="~closure")

    # NOTE: these are set so that dependencies in downstream projects share
    # common MPI dependence
    for _flag in ("~mpi", "+mpi"):
        depends_on("hdf5~cxx+hl" + _flag, when="+hdf5" + _flag)
        depends_on("py-h5py" + _flag, when="@:1.6.2 " + _flag)

    # can be removed once <1.8.0 versions have been removed
    def flag_handler(self, name, flags):
        if name == "fflags":
            if self.spec.satisfies("%cce+fortran"):
                # The Cray fortran compiler generates module files with
                # uppercase names by default, which is not handled by the
                # CMake scripts. The following flag forces the compiler to
                # produce module files with lowercase names.
                flags.append("-ef")
        return (flags, None, None)

    def cmake_args(self):
        args = [
            self.define("SINGULARITY_PATCH_MPARK_VARIANT", False),
            self.define_from_variant("SINGULARITY_USE_CUDA", "cuda"),
            self.define_from_variant("SINGULARITY_USE_KOKKOS", "kokkos"),
            self.define_from_variant("SINGULARITY_USE_KOKKOSKERNELS", "kokkos-kernels"),
            self.define_from_variant("SINGULARITY_USE_FORTRAN", "fortran"),
            self.define_from_variant("SINGULARITY_BUILD_CLOSURE", "closure"),
            self.define_from_variant("SINGULARITY_BUILD_PYTHON", "python"),
            self.define_from_variant("SINGULARITY_USE_SPINER", "spiner"),
            self.define_from_variant("SINGULARITY_USE_SPINER_WITH_HDF5", "hdf5"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("SINGULARITY_BUILD_TESTS", self.run_tests),
            self.define(
                "SINGULARITY_BUILD_SESAME2SPINER",
                "sesame" in self.spec.variants["build_extra"].value,
            ),
            self.define(
                "SINGULARITY_TEST_SESAME",
                ("sesame" in self.spec.variants["build_extra"].value and self.run_tests),
            ),
            self.define(
                "SINGULARITY_BUILD_STELLARCOLLAPSE2SPINER",
                "stellarcollapse" in self.spec.variants["build_extra"].value,
            ),
            self.define(
                "SINGULARITY_TEST_STELLAR_COLLAPSE",
                ("stellarcollapse" in self.spec.variants["build_extra"].value and self.run_tests),
            ),
            self.define("SINGULARITY_TEST_PYTHON", ("+python" in self.spec and self.run_tests)),
            self.define("SINGULARITY_USE_HDF5", "^hdf5" in self.spec),
            self.define("SINGULARITY_USE_EOSPAC", "^eospac" in self.spec),
        ]

        if self.spec.satisfies("@1.9.0:"):
            if "none" not in self.spec.variants["plugins"].value:
                pdirs = []
                for p in self.spec.variants["plugins"].value:
                    spackage, path = self.plugins[p]
                    if spackage == "self":
                        pdirs.append(join_path(self.stage.source_path, path))
                    else:
                        pdirs.append(join_path(self.spec[spackage].prefix, path))
                args.append(self.define("SINGULARITY_PLUGINS", ";".join(pdirs)))

            variant_path = self.spec.variants["variant"].value
            if variant_path != "default":
                parts = os.path.normpath("variant_path").split(os.sep)
                if parts[0] in self.plugins.keys():
                    spackage, path = self.plugins[parts[0]]
                    parts[0] = self.spec[spackage].prefix
                    variant_path = join_path(*parts)
                args.append(self.define("SINGULARITY_VARIANT", variant_path))

        if "+rocm" in self.spec:
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            args.append(self.define("CMAKE_C_COMPILER", self.spec["hip"].hipcc))
        if "+kokkos+cuda" in self.spec:
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["kokkos"].kokkos_cxx))

        if "+kokkos" in self.spec:
            args.append(
                self.define("CMAKE_CXX_STANDARD", self.spec["kokkos"].variants["cxxstd"].value)
            )

        # check if goldfiles were downloaded into source folder
        goldfiles = os.path.join(self.stage.source_path, "goldfiles.tar.gz")
        if (
            self.spec.satisfies("+tests build_extra=stellarcollapse")
            and self.run_tests
            and os.path.exists(goldfiles)
        ):
            args.append(self.define("SINGULARITY_GOLDFILE_URL", f"file://{goldfiles}"))

        return args

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        if "+python" in self.spec:
            python_version = self.spec["python"].version.up_to(2)
            python_inst_dir = join_path(
                lib_dir, "python{0}".format(python_version), "site-packages"
            )
            env.prepend_path("PYTHONPATH", python_inst_dir)
