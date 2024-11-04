# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class RocmTensile(CMakePackage):
    """Radeon Open Compute Tensile library"""

    homepage = "https://github.com/ROCm/Tensile/"
    git = "https://github.com/ROCm/Tensile.git"
    url = "https://github.com/ROCm/Tensile/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    license("MIT")

    maintainers("srekolam", "renjithravindrankannath", "haampie")
    version("6.2.0", sha256="6f7d679bfffd1f723f2788b00fdcb1b4673b597f9f85c2cdaab3c2aa17afb33d")
    version("6.1.2", sha256="6a08190f6d9c8cc76764a68e2dd3e7af4759d4146ddc1c4b3370c7762a6f6d83")
    version("6.1.1", sha256="04fd76e6a0e9b7528e61df0721b03c0e977c145a2a1ea331d515c9167d7ac35f")
    version("6.1.0", sha256="69bfdc711d3a86e6651b1dcfb2c461c7d3ae574e6d884833d4e07d3e7ad06491")
    version("6.0.2", sha256="1d8a92422560c1e908fa25fd97a4aa07a96659528a543f77618408ffcfe1f307")
    version("6.0.0", sha256="5d90add62d1439b7daf0527316e950e454e5d8beefb4f723865fe9ab26c7aa42")
    version("5.7.1", sha256="9211a51b23c22b7a79e4e494e8ff3c31e90bf21adb8cce260acc57891fb2c917")
    version("5.7.0", sha256="fe2ae067c1c579f33d7a1e26da3fe6b4ed44befa08f9dfce2ceae586f184b816")
    version("5.6.1", sha256="3e78c933563fade8781a1dca2079bff135af2f5d2c6eb0147797d2c1f24d006c")
    version("5.6.0", sha256="383728ecf49def59ab9a7f8a1d1e2eaf8b528e36b461e27030a2aab1a1ed80cb")
    version("5.5.1", sha256="b65cb7335abe51ba33be9d46a5ede992b4e5932fa33797397899a6bf33a770e9")
    version("5.5.0", sha256="70fd736d40bb4c3461f07c77ad3ae6c485e3e842671ce9b223d023d836884ae2")
    with default_args(deprecated=True):
        version("5.4.3", sha256="a4c5e62edd33ea6b8528eb3f017a14c28eaa67c540f5c9023f6a245340198b0f")
        version("5.4.0", sha256="2da9c1df3c6d9b44afdad621ef59a03389fb1a38a61a8b8bad9c9991b97157eb")
        version("5.3.3", sha256="ecb99243edf1cd2bb5e953915a7dae7867c3cdb0cd8ed15b8618aaaeb2bd7b29")
        version("5.3.0", sha256="05c546986549154e6c7b4f57a0b3bfd5cb223d2393c206ff1702f89454c832f4")

    depends_on("cxx", type="build")  # generated

    tensile_architecture = (
        "all",
        "gfx906:xnack-",
        "gfx908:xnack-",
        "gfx90a:xnack-",
        "gfx1010",
        "gfx1011",
        "gfx1012",
        "gfx1030",
    )

    variant(
        "tensile_architecture",
        default="all",
        description="AMD GPU architecture",
        values=tensile_architecture,
        multi=True,
    )
    variant("openmp", default=True, description="Enable OpenMP")
    depends_on("cmake@3:", type="build")
    depends_on("msgpack-c@3:")
    depends_on("boost", type=("build", "link"))
    depends_on(Boost.with_default_variants)

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
    ]:
        depends_on(f"rocm-cmake@{ver}", type="build", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", type="build", when=f"@{ver}")
        depends_on(f"rocm-openmp-extras@{ver}", when=f"@{ver}")
        depends_on(f"rocm-smi-lib@{ver}", type="build", when=f"@{ver}")

    root_cmakelists_dir = "Tensile/Source"

    patch("0003-require-openmp-extras-when-tensile-use-openmp.patch", when="@5.1.0:")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
        env.append_flags("LDFLAGS", "-pthread")

    def get_gpulist_for_tensile_support(self):
        arch = self.spec.variants["tensile_architecture"].value
        return self.tensile_architecture[1:] if arch[0] == "all" else arch

    def cmake_args(self):
        args = [
            self.define("amd_comgr_DIR", self.spec["comgr"].prefix),
            self.define("Tensile_COMPILER", "hipcc"),
            self.define("Tensile_LOGIC", "asm_full"),
            self.define("Tensile_CODE_OBJECT_VERSION", "V3"),
            self.define("Boost_USE_STATIC_LIBS", "OFF"),
            self.define_from_variant("TENSILE_USE_OPENMP", "openmp"),
            self.define("BUILD_WITH_TENSILE_HOST", True),
            self.define("Tensile_LIBRARY_FORMAT", "msgpack"),
            self.define("TENSILE_USE_OPENMP", True),
            self.define("ROCM_OPENMP_EXTRAS_DIR", self.spec["rocm-openmp-extras"].prefix),
        ]

        if self.spec.satisfies("^cmake@3.21.0:"):
            args.append(
                self.define("CMAKE_HIP_ARCHITECTURES", self.get_gpulist_for_tensile_support())
            )
        else:
            args.append(
                self.define("Tensile_ARCHITECTURE", self.get_gpulist_for_tensile_support())
            )

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree("./client", prefix.client)
            install_tree("./lib", prefix.lib)
