# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gaudi(CMakePackage):
    """An experiment-independent HEP event data processing framework"""

    homepage = "https://gaudi.web.cern.ch/gaudi/"
    git = "https://gitlab.cern.ch/gaudi/Gaudi.git"
    url = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v33r1/Gaudi-v33r1.tar.gz"

    tags = ["hep"]

    version("master", branch="master")
    version("39.0", sha256="faa3653e2e6c769292c0592e3fc35cd98a2820bd6fc0c967cac565808b927262")
    version("38.3", sha256="47e8c65ea446656d2dae54a32205525e08257778cf80f9f029cd244d6650486e")
    version("38.2", sha256="08759b1398336987ad991602e37079f0744e8d8e4e3d5df2d253b8dedf925068")
    version("38.1", sha256="79d42833edcebc2099f91badb6f72708640c05f678cc4521a86e857f112486dc")
    version("38.0", sha256="52f2733fa0af760c079b3438bb9c7e36b28ea704f78b0085458e1918c11e1653")
    version("37.2", sha256="9b866caab46e182de98b59eddbde80d6fa0e670fe4a35906f1518b04bd99b2d2")
    version("37.1", sha256="1d7038fd5dfb5f2517ce57623cf8090549ffe2ea8f0171d534e5c1ca20bd009a")
    version("37.0", sha256="823f3821a4f498ddd2dd123fbb8a3787b361ddfd818f4ab13572076fc9afdfe4")
    version("36.14", sha256="b11e0afcb797d61a305856dfe8079d48d74c6b6867ceccc0a83aab5978c9ba5f")
    version("36.13", sha256="41e711c83428663996c825044b268ce515bef85dad74b4a9453f2207b4b1be7b")
    version("36.12", sha256="dfce9156cedfa0a7234f880a3c395e592a5f3dc79070d5d196fdb94b83ae203e")
    version("36.11", sha256="81664d033b0aa8598a0e4cb7e455e697baeb063a11bbde2390164776238ba9f7")
    version("36.10", sha256="2c1f181c54a76b493b913aeecbd6595236afc08e41d7f1d80be6fe65ac95adb3")
    version("36.9", sha256="b4e080094771f111bd0bcdf744bcab7b028c7e2af7c5dfaa4a977ebbf0160a8f")
    version("36.8", sha256="64b4300a57335af7c1f74c736d7610041a1ef0c1f976e3342a22385b60519afc")
    version("36.7", sha256="8dca43185ba11e1b33f5535d2e384542d84500407b0d1f8cb920be00f05c9716")
    version("36.6", sha256="8fc7be0ce32f99cc6b0be4ebbb246f4bb5008ffbf0c012cb39c0aff813dce6af")
    version("36.5", sha256="593e0316118411a5c5fde5d4d87cbfc3d2bb748a8c72a66f4025498fcbdb0f7e")
    version("36.4", sha256="1a5c27cdc21ec136b47f5805406c92268163393c821107a24dbb47bd88e4b97d")
    version("36.3", sha256="9ac228d8609416afe4dea6445c6b3ccebac6fab1e46121fcc3a056e24a5d6640")
    version("36.2", sha256="a1b4bb597941a7a5b8d60382674f0b4ca5349c540471cd3d4454efbe7b9a09b9")
    version("36.1", sha256="9f718c832313676249e5c3ac76ba4346978ee2328f8cdcb29176498b080402e9")
    version("36.0", sha256="8a0458cef5b616532f9db7cca9fa0e892e602b64c9e93dc0cc6d972e03034830")
    version("35.0", sha256="c01b822f9592a7bf875b9997cbeb3c94dea97cb13d523c12649dbbf5d69b5fa6")

    depends_on("cxx", type="build")

    conflicts("%gcc@:10", when="@39:", msg="Gaudi needs a c++20 capable compiler for this version")

    maintainers("drbenmorgan", "vvolkl", "jmcarcell")

    variant("aida", default=False, description="Build AIDA interfaces support")
    variant("cppunit", default=False, description="Build with CppUnit unit testing")
    variant("docs", default=False, description="Build documentation with Doxygen")
    variant("examples", default=False, description="Build examples")
    variant("gaudialg", default=False, description="Build GaudiAlg support", when="@37.0:38")
    variant("gperftools", default=False, description="Build with Google PerfTools support")
    variant("heppdt", default=False, description="Build with HEP Particle Data Table support")
    variant("jemalloc", default=False, description="Build with jemalloc allocator support")
    variant("unwind", default=False, description="Build with unwind call-chains")
    variant("vtune", default=False, description="Build with Intel VTune profiler support")
    variant("xercesc", default=False, description="Build with Xerces-C XML support")

    patch("fmt_fix.patch", when="@36.6:36.12 ^fmt@10:")
    # fix issues with catch2 3.1 and above
    patch(
        "https://gitlab.cern.ch/gaudi/Gaudi/-/commit/110f2189f386c3a23150ccdfdc47c1858fc7098e.diff",
        sha256="b05f6b7c1efb8c3af291c8d81fd1627e58af7c5f9a78a0098c6e3bfd7ec80c15",
        when="@37.1 ^catch2@3.1:",
    )
    # add missing <list> include for newer compilers
    patch(
        "https://gitlab.cern.ch/gaudi/Gaudi/-/commit/54b727f08a685606420703098131b387d3026637.diff",
        sha256="41aa1587a3e59d49e0fa9659577073c091871c2eca1b8b237c177ab98fbacf3f",
        when="@:38.1",
    )

    # add a few missing includes (c++20?)
    patch("includes.patch", when="@37:38")

    # These dependencies are needed for a minimal Gaudi build
    depends_on("aida")
    # The boost components that are required for Gaudi
    boost_libs = "+".join(
        [
            "system",
            "filesystem",
            "regex",
            "thread",
            "python",
            "test",
            "program_options",
            "log",
            "graph",
        ]
    )
    depends_on(f"boost@1.70: +{boost_libs}", when="@35:")
    depends_on(f"boost@1.70: +{boost_libs}+fiber", when="@39:")

    depends_on("clhep")
    depends_on("cmake", type="build")
    depends_on("cmake@3.19:", type="build", when="@39:")
    depends_on("cppgsl")
    depends_on("fmt@:8", when="@:36.9")
    depends_on("fmt@:10")
    depends_on("intel-tbb@:2020.3", when="@:37.0")
    depends_on("tbb", when="@37.1:")
    depends_on("uuid")
    depends_on("nlohmann-json")
    depends_on("python +dbm", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run", "test"))
    depends_on("range-v3")
    depends_on("root +python +root7 +ssl +tbb +threads")
    depends_on("zlib-api")
    depends_on("py-pytest-cov", when="@39:")

    # Testing dependencies
    # Note: gaudi only builds examples when testing enabled
    for pv in (["catch2", "@36.8:"], ["py-nose", "@35:"], ["py-pytest", "@36.2:"]):
        depends_on(pv[0], when=pv[1], type="test")
        depends_on(pv[0], when=pv[1] + " +examples")

    # Adding these dependencies triggers the build of most optional components
    depends_on("cppunit", when="+cppunit")
    depends_on("doxygen +graphviz", when="+docs")
    depends_on("gperftools", when="+gperftools")
    depends_on("gdb")
    depends_on("heppdt", when="+heppdt")
    depends_on("jemalloc", when="+jemalloc")
    depends_on("libunwind", when="+unwind")
    depends_on("xerces-c", when="+xercesc")
    # NOTE: pocl cannot be added as a minimal OpenCL implementation because
    #       ROOT does not like being exposed to LLVM symbols.

    # The Intel VTune dependency is taken aside because it requires a license
    depends_on("intel-parallel-studio -mpi +vtune", when="+vtune")

    def cmake_args(self):
        args = [
            # Note: gaudi only builds examples when testing enabled
            self.define("BUILD_TESTING", self.run_tests or self.spec.satisfies("+examples")),
            self.define_from_variant("GAUDI_USE_AIDA", "aida"),
            self.define_from_variant("GAUDI_USE_CPPUNIT", "cppunit"),
            self.define_from_variant("GAUDI_ENABLE_GAUDIALG", "gaudialg"),
            self.define_from_variant("GAUDI_USE_GPERFTOOLS", "gperftools"),
            self.define_from_variant("GAUDI_USE_HEPPDT", "heppdt"),
            self.define_from_variant("GAUDI_USE_JEMALLOC", "jemalloc"),
            self.define_from_variant("GAUDI_USE_UNWIND", "unwind"),
            self.define_from_variant("GAUDI_USE_XERCESC", "xercesc"),
            self.define_from_variant("GAUDI_USE_DOXYGEN", "docs"),
            # needed to build core services like rndmsvc
            self.define("GAUDI_USE_CLHEP", True),
            self.define("GAUDI_USE_PYTHON_MAJOR", str(self.spec["python"].version.up_to(1))),
            # todo:
            self.define("GAUDI_USE_INTELAMPLIFIER", False),
        ]
        # Release notes for v39.0: https://gitlab.cern.ch/gaudi/Gaudi/-/releases/v39r0
        # Gaudi@39: needs C++ >= 20, and we need to force CMake to use C++ 20 with old gcc:
        if self.spec.satisfies("@39: %gcc@:13"):
            args.append(self.define("GAUDI_CXX_STANDARD", "20"))
        return args

    def setup_run_environment(self, env):
        # environment as in Gaudi.xenv
        env.prepend_path("PATH", self.prefix.scripts)
        env.prepend_path("PYTHONPATH", self.prefix.python)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)

    def url_for_version(self, version):
        major = str(version[0])
        minor = str(version[1])
        url = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v{0}r{1}/Gaudi-v{0}r{1}.tar.gz".format(
            major, minor
        )
        return url
