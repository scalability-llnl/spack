# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gasnet(Package, CudaPackage, ROCmPackage):
    """GASNet is a language-independent, networking middleware layer that
    provides network-independent, high-performance communication primitives
    including Remote Memory Access (RMA) and Active Messages (AM). It has been
    used to implement parallel programming models and libraries such as UPC,
    UPC++, Co-Array Fortran, Legion, Chapel, and many others. The interface is
    primarily intended as a compilation target and for use by runtime library
    writers (as opposed to end users), and the primary goals are high
    performance, interface portability, and expressiveness.

    ***NOTICE***: The GASNet library built by this Spack package is ONLY intended for
    unit-testing purposes, and is generally UNSUITABLE FOR PRODUCTION USE.
    The RECOMMENDED way to build GASNet is as an embedded library as configured
    by the higher-level client runtime package (UPC++, Legion, etc), including
    system-specific configuration.
    """

    homepage = "https://gasnet.lbl.gov"
    url = "https://gasnet.lbl.gov/EX/GASNet-2021.3.0.tar.gz"
    git = "https://bitbucket.org/berkeleylab/gasnet.git"

    maintainers("PHHargrove", "bonachea")

    tags = ["e4s", "ecp"]

    version("develop", branch="develop")
    version("main", branch="stable")
    version("master", branch="master")

    version("2024.5.0", sha256="f945e80f71d340664766b66290496d230e021df5e5cd88f404d101258446daa9")
    version("2023.9.0", sha256="2d9f15a794e10683579ce494cd458b0dd97e2d3327c4d17e1fea79bd95576ce6")
    version("2023.3.0", sha256="e1fa783d38a503cf2efa7662be591ca5c2bb98d19ac72a9bc6da457329a9a14f")
    version("2022.9.2", sha256="2352d52f395a9aa14cc57d82957d9f1ebd928d0a0021fd26c5f1382a06cd6f1d")
    version("2022.9.0", sha256="6873ff4ad8ebee49da4378f2d78095a6ccc31333d6ae4cd739b9f772af11f936")
    version(
        "2022.3.0",
        deprecated=True,
        sha256="91b59aa84c0680c807e00d3d1d8fa7c33c1aed50b86d1616f93e499620a9ba09",
    )
    version(
        "2021.9.0",
        deprecated=True,
        sha256="1b6ff6cdad5ecf76b92032ef9507e8a0876c9fc3ee0ab008de847c1fad0359ee",
    )
    version(
        "2021.3.0",
        deprecated=True,
        sha256="8a40fb3fa8bacc3922cd4d45217816fcb60100357ab97fb622a245567ea31747",
    )
    version(
        "2020.10.0",
        deprecated=True,
        sha256="ed17baf7fce90499b539857ee37b3eea961aa475cffbde77e4c607a34ece06a0",
    )
    version(
        "2020.3.0",
        deprecated=True,
        sha256="019eb2d2284856e6fabe6c8c0061c874f10e95fa0265245f227fd3497f1bb274",
    )
    version(
        "2019.9.0",
        deprecated=True,
        sha256="117f5fdb16e53d0fa8a47a1e28cccab1d8020ed4f6e50163d985dc90226aaa2c",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    # Do NOT add older versions here.
    # GASNet-EX releases over 2 years old are not supported.

    # The optional network backends:
    variant(
        "conduits",
        values=any_combination_of("smp", "mpi", "ibv", "udp", "ofi", "ucx").with_default("smp"),
        description="The hardware-dependent network backends to enable.\n"
        + "(smp) = SMP conduit for single-node operation\n"
        + "(ibv) = Native InfiniBand verbs conduit\n"
        + "(ofi) = OFI conduit over libfabric, for HPE Cray Slingshot and Intel Omni-Path\n"
        + "(udp) = Portable UDP conduit, for Ethernet networks\n"
        + "(mpi) = Low-performance/portable MPI conduit\n"
        + "(ucx) = EXPERIMENTAL UCX conduit for Mellanox IB/RoCE ConnectX-5+\n"
        + "For detailed recommendations, consult https://gasnet.lbl.gov",
    )

    variant("debug", default=False, description="Enable library debugging mode")

    variant(
        "cuda",
        default=False,
        description="Enables support for the CUDA memory kind in some conduits.\n"
        + "NOTE: Requires CUDA Driver library be present on the build system",
        when="@2020.11:",
    )
    conflicts(
        "+cuda",
        when="@:2020.10",
        msg="GASNet version 2020.11.0 or newer required for CUDA support",
    )

    variant(
        "rocm",
        default=False,
        description="Enables support for the ROCm/HIP memory kind in some conduits",
        when="@2021.9:",
    )
    conflicts(
        "+rocm", when="@:2021.8", msg="GASNet version 2021.9.0 or newer required for ROCm support"
    )

    variant(
        "level_zero",
        default=False,
        description="Enables *experimental* support for the Level Zero "
        + "memory kind on Intel GPUs in some conduits",
        when="@2023.9.0:",
    )

    depends_on("mpi", when="conduits=mpi")
    depends_on("libfabric", when="conduits=ofi")

    depends_on("autoconf@2.69", type="build", when="@master:")
    depends_on("automake@1.16:", type="build", when="@master:")

    conflicts("^hip@:4.4.0", when="+rocm")

    conflicts("^hip@6:", when="@:2024.4+rocm")  # Bug 4686

    depends_on("oneapi-level-zero@1.8.0:", when="+level_zero")

    def install(self, spec, prefix):
        if spec.satisfies("@master:"):
            bootstrapsh = Executable("./Bootstrap")
            bootstrapsh()
            # Record git-describe when fetched from git:
            try:
                git = which("git")
                git("describe", "--long", "--always", output="version.git")
            except spack.util.executable.ProcessError:
                spack.main.send_warning_to_tty("Omitting version stamp due to git error")

        # The GASNet-EX library has a highly multi-dimensional configure space,
        # to accomodate the varying behavioral requirements of each client runtime.
        # The library's ABI/link compatibility is strongly dependent on these
        # client-specific build-time settings, and that variability is deliberately NOT
        # encoded in the variants of this package. The recommended way to build/deploy
        # GASNet is as an EMBEDDED library within the build of the client package
        # (eg. Berkeley UPC, UPC++, Legion, etc), some of which provide build-time
        # selection of the GASNet library sources. This spack package provides
        # the GASNet-EX sources, for use by appropriate client packages.
        install_tree(".", prefix + "/src")

        # Library build is provided for unit-testing purposes only (see notice above)
        if "conduits=none" not in spec:
            options = ["--prefix=%s" % prefix]

            if spec.satisfies("+debug"):
                options.append("--enable-debug")

            if spec.satisfies("+cuda"):
                options.append("--enable-kind-cuda-uva")
                options.append("--with-cuda-home=" + spec["cuda"].prefix)

            if spec.satisfies("+rocm"):
                options.append("--enable-kind-hip")
                options.append("--with-hip-home=" + spec["hip"].prefix)

            if spec.satisfies("+level_zero"):
                options.append("--enable-kind-ze")
                options.append("--with-ze-home=" + spec["oneapi-level-zero"].prefix)

            if spec.satisfies("conduits=mpi"):
                options.append("--enable-mpi-compat")
            else:
                options.append("--disable-mpi-compat")

            options.append("--disable-auto-conduit-detect")
            for c in spec.variants["conduits"].value:
                options.append("--enable-" + c)

            options.append("--enable-rpath")

            configure(*options)
            make()
            make("install")

            for c in spec.variants["conduits"].value:
                testdir = join_path(self.prefix.tests, c)
                mkdirp(testdir)
                make("-C", c + "-conduit", "testgasnet-par")
                install(c + "-conduit/testgasnet", testdir)
            make("-C", c + "-conduit", "testtools-par")
            install(c + "-conduit/testtools", self.prefix.tests)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        if self.spec.satisfies("conduits=smp"):
            make("-C", "smp-conduit", "run-tests")
        self.test_testtools()

    def _setup_test_env(self):
        """Set up key stand-alone test environment variables."""
        os.environ["GASNET_VERBOSEENV"] = "1"  # include diagnostic info

        # The following are not technically relevant to test_testtools
        os.environ["GASNET_SPAWN_VERBOSE"] = "1"  # include spawning diagnostics
        if "GASNET_SSH_SERVERS" not in os.environ:
            os.environ["GASNET_SSH_SERVERS"] = "localhost " * 4

    def test_testtools(self):
        """run testtools and check output"""
        if self.spec.satisfies("conduits=none"):
            raise SkipTest("Test requires conduit libraries")

        testtools_path = join_path(self.prefix.tests, "testtools")
        assert os.path.exists(testtools_path), "Test requires testtools"

        self._setup_test_env()
        testtools = which(testtools_path, required=True)
        out = testtools(output=str.split, error=str.split)
        assert "Done." in out

    def test_testgasnet(self):
        """run testgasnet and check output"""
        if self.spec.satisfies("conduits=none"):
            raise SkipTest("Test requires conduit libraries")

        self._setup_test_env()
        ranks = "4"
        spawner = {
            "smp": ["env", "GASNET_PSHM_NODES=" + ranks],
            "mpi": [join_path(self.prefix.bin, "gasnetrun_mpi"), "-n", ranks],
            "ibv": [join_path(self.prefix.bin, "gasnetrun_ibv"), "-n", ranks],
            "ofi": [join_path(self.prefix.bin, "gasnetrun_ofi"), "-n", ranks],
            "ucx": [join_path(self.prefix.bin, "gasnetrun_ucx"), "-n", ranks],
            "udp": [join_path(self.prefix.bin, "amudprun"), "-spawn", "L", "-np", ranks],
        }

        expected = "done."
        for c in self.spec.variants["conduits"].value:
            os.environ["GASNET_SUPERNODE_MAXSIZE"] = "0" if (c == "smp") else "1"
            test = join_path(self.prefix.tests, c, "testgasnet")

            with test_part(
                self,
                "test_testgasnet_{0}".format(c),
                purpose="run {0}-conduit/testgasnet".format(c),
            ):
                exe = which(spawner[c][0], required=True)

                args = spawner[c][1:] + [test]
                out = exe(*args, output=str.split, error=str.split)
                assert expected in out
