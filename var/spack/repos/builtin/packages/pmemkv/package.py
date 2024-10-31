# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pmemkv(CMakePackage):
    """pmemkv is a local/embedded key-value datastore,
    optimized for persistent memory.
    """

    homepage = "https://pmem.io/pmemkv/"
    url = "https://github.com/pmem/pmemkv/archive/1.4.tar.gz"
    git = "https://github.com/pmem/pmemkv.git"

    version("master", branch="master")
    version("1.4", sha256="6630917e0203eff7a520071c858baa7b7e108088da2fe8c4b31ec5f8c661fbe9")
    version("1.3", sha256="f1b946ef3545bcc2751fa2e4faab0538cd3072b66d4c4575f21712e0cc53bae8")
    version("1.2", sha256="22de74392e0a6eea5aa1955ed2d59462bf45ec69a01eb1cf2115e39e7bdc4754")
    version("1.1", sha256="c4ca07c1fecad39b5dbf197673f033f27d74c9f9987f036f6eaf5c7f23a342f3")
    version("1.0.3", sha256="cae393a01ba69364271c5894046bf2c611f677ac88012f2473fadf6fcd20ff29")
    version("1.0.2", sha256="a0cbbb60c0342d6fd0b73d2cee1a1423c6a894b8d21daf669016809961fe23b8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libpmemobj-cpp@develop", when="@master")
    depends_on("libpmemobj-cpp@1.12:", when="@1.4:")
    depends_on("libpmemobj-cpp@1.11:", when="@1.3:")
    depends_on("libpmemobj-cpp@1.10:", when="@1.2:")
    depends_on("libpmemobj-cpp@1.9:", when="@1.1:")
    depends_on("libpmemobj-cpp@1.8:", when="@1.0.2:")

    depends_on("pmdk@master", when="@master")
    depends_on("pmdk@master", when="@1.4:")
    depends_on("pmdk@1.8:", when="@1.1:")
    depends_on("pmdk@1.7:", when="@1.0.2:")

    depends_on("memkind@1.8.0:")

    depends_on("rapidjson")

    # tbb is one of virtual dependencies.
    # Please refer https://spack.readthedocs.io/en/latest/packaging_guide.html#virtual-dependencies
    # we can use any packages which provides 'tbb'
    # For example, 'intel-tbb' or 'intel-oneapi-tbb'
    # Default is 'intel-tbb' (etc/spack/defaults/packages.yaml)
    depends_on("tbb")

    depends_on("cmake@3.3:")

    variant("cmap", default=True, description="enable cmap engine.")
    variant("vcmap", default=True, description="enable vcmap engine.")
    variant("vsmap", default=True, description="enable vsmap engine.")
    variant("csmap", default=False, description="enable experimental csmap engine.")
    variant("stree", default=True, description="enable experimental stree engine.")
    variant("tree3", default=False, description="enable experimental tree3 engine.")
    variant("radix", default=False, description="enable experimental radix engine.")
    variant("robinhood", default=False, description="enable experimental robinhood engine.")
    variant("dram_vcmap", default=False, description="enable testing dram_vcmap engine.")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("BUILD_DOC", False),
            self.define("BUILD_EXAMPLES", False),
            self.define("BUILD_TESTS", False),
            self.define("BUILD_JSON_CONFIG", True),
            self.define("TESTS_LONG", False),
            self.define("TESTS_USE_FORCED_PMEM", False),
            self.define("TESTS_USE_VALGRIND", False),
            self.define("TESTS_PMEMOBJ_DRD_HELGRIND", False),
            self.define("TESTS_JSON", False),
            self.define_from_variant("ENGINE_CMAP", "cmap"),
            self.define_from_variant("ENGINE_VCMAP", "vcmap"),
            self.define_from_variant("ENGINE_VSMAP", "vsmap"),
            self.define_from_variant("ENGINE_CSMAP", "csmap"),
            self.define_from_variant("ENGINE_STREE", "stree"),
            self.define_from_variant("ENGINE_TREE3", "tree3"),
            self.define_from_variant("ENGINE_RADIX", "radix"),
            self.define_from_variant("ENGINE_ROBINHOOD", "robinhood"),
            self.define_from_variant("ENGINE_DRAM_VCMAP", "dram_vcmap"),
        ]

        if ("+csmap" in spec) or ("+robinhood" in spec):
            args.append(self.define("CXX_STANDARD", 14))

        return args
