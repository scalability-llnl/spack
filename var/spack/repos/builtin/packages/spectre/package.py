# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spectre(CMakePackage):
    """The SpECTRE numerical relativity code.

    SpECTRE is an open-source code for multi-scale, multi-physics problems in
    astrophysics and gravitational physics. In the future, we hope that it can
    be applied to problems across discipline boundaries in fluid dynamics,
    geoscience, plasma physics, nuclear physics, and engineering. It runs at
    petascale and is designed for future exascale computers.

    SpECTRE is being developed in support of our collaborative Simulating
    eXtreme Spacetimes (SXS) research program into the multi-messenger
    astrophysics of neutron star mergers, core-collapse supernovae, and
    gamma-ray bursts."""

    homepage = "https://spectre-code.com"
    url = "https://github.com/sxs-collaboration/spectre/archive/v2021.12.15.tar.gz"
    git = "https://github.com/sxs-collaboration/spectre.git"

    maintainers("nilsvu")

    generator("ninja")

    license("MIT")

    version("develop", branch="develop")
    version(
        "2024.09.29", sha256="b5e84b4564ad7cd2e069a24c6c472aab342753fe8393242eceba378b52226acb"
    )
    version(
        "2024.09.16", sha256="2524d4e3cbe9206c0d8830fd6969dcf4cf53aefb26c882c6a743638611763171"
    )
    version(
        "2024.08.03", sha256="18582b625b121c16cd9a1ec421c4ac6cb77bb252622a205b038306e75a466138"
    )
    version(
        "2024.06.18", sha256="75ca22f3f9d59887b4ae40397fffc0ada9f218cbb23013e86e14deabb30490f7"
    )
    version(
        "2024.06.05", sha256="7f1dcb5dc067a3977d1720ab655507f52821d898ea1e2b2a82c52dd9e246804f"
    )
    version(
        "2024.05.11", sha256="be3a91011dd52adfe6f1263a1ee4bf8c51ac95c7d537ad934453997637e5d31a"
    )
    version(
        "2024.04.12", sha256="2ca46e1c493225e9067546595b1bb234d8634de4974ba87a7b8f011e686b44b6"
    )
    version(
        "2024.03.19", sha256="42a25c8827b56268d9826239cde521491be19318d83785b35cd0265a9f6a1f7c"
    )
    version(
        "2024.02.05", sha256="cf5c4da473d665d0cac0a32562b1b8e8c0f1a77eebca8c3171e52cdf3056fdb3"
    )
    version(
        "2023.12.08", sha256="662b4df6b6cdb097f9edcba869b3e05affeae485de8766ca66bf21399c39a9d8"
    )
    version(
        "2023.10.11", sha256="f25d17bc80cc49ebdd81726326701fe9ecd2b6705d86e6e3d48d9e4a458c8aff"
    )
    version(
        "2023.09.07", sha256="2375117df09d99a2716d445ff51d151422467bd42cd38b5f1177d2d40cb90916"
    )
    version(
        "2023.08.18", sha256="bdeb7da707d51d0e3b2a29b1d28646c5a64cba15844612e7b3726e8a28b37692"
    )
    version(
        "2023.07.29", sha256="134668b81b8e89e3fd02b8b1415a1198889d7fb90f04ca6556458d3ce4489e43"
    )
    version(
        "2023.06.19", sha256="f1140dfca1a9cf58f04acfe853c5597fa19c463d52b3643428e379496bff1236"
    )
    version(
        "2023.05.16", sha256="9cfe585e85b63e69d1b9b3922c68d3bd83d95853b6955e706133f2aaa933bd2b"
    )
    version(
        "2023.04.07", sha256="f18238788155413c4c1f73c5591f4bf60a3d331f0c926b3737a61b33c99dfb9c"
    )
    version(
        "2023.03.09", sha256="d8cd3512a8477b0b9ac83141d18fc7c55280bd886c6d97b60e8ae26c16c648ab"
    )
    version(
        "2023.02.09", sha256="cdd85aed10ea7d372a7989da16a379e684276978c1e53438cb562910601fd471"
    )
    version(
        "2023.01.13", sha256="fa1392015e4a8900483e0428e6b7b51a6c129f3d64f7ff862d810cfea0e04b40"
    )
    version(
        "2022.12.16", sha256="2b692ff1be889c86bc2d95ef523dc1a4880e66b9bdf75883e299643f4ccbcb50"
    )
    version(
        "2022.12.02", sha256="a930a41fe16834bf8dd9191180fd9db8fd8a871fbd10cc2c48a5360c0990a5b7"
    )
    version(
        "2022.11.15", sha256="3860fdb49b5ca5bc067a291f744f67f59081db21c82beb92b4c033edf39fc62e"
    )
    version(
        "2022.10.04", sha256="f9666ad7e546b2b6b5bc7743db1ab20eaada77ce5016f4467a96c9aab838ae1b"
    )
    version(
        "2022.09.02", sha256="8a218237c76f85debf8a1c65de67a6c7fe41c5df51efd7b5c160868ba5d40927"
    )
    version(
        "2022.08.01", sha256="453ad831f3d8c2d4dbed0b2e4f08f7a3b64e6634a2025b5ac1a0b242c1d87d93"
    )
    version(
        "2022.07.18", sha256="8812aeba70d60d6800fe8866542c3d2e0fae34aaac0c8d1c4324cf6c804f3fe1"
    )
    version(
        "2022.06.14", sha256="872ab6729d8675c90b0d194f4ca34e4c02ce23e60c558a43b874fee9da9dfe78"
    )
    version(
        "2022.05.05", sha256="4577d3a0e85c3ce2a39f1ec40d6c5455d876d55069b39c5e062efbf261c18455"
    )
    version(
        "2022.04.04", sha256="264d9b585fa1838b118e50893ce149d76bbf568ee4c27a3732fe0db904de986a"
    )
    version(
        "2022.03.07", sha256="41b2dea4d4a91313987fbad5252cad4a7e1cb3dcef5fbad0a09ea942423f5013"
    )
    version(
        "2022.02.17", sha256="4bc2949453a35699090efc2bb71b8bd2b951909e0f02d0f8c8af255d1668e63f"
    )
    version(
        "2022.02.08", sha256="996275536c990a6d49cd61f207c04ad771a1449506f38507afc35f95b29d4cf1"
    )
    version(
        "2022.01.03", sha256="872a0d152c19864ad543ddcc585ce30baaad4185c2617c13463d780175cbde5f"
    )
    version(
        "2021.12.15", sha256="4bfe9e27412e263ffdc6fcfcb84011f16d34a9fdd633ad7fc84a34c898f67e5c"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Configuration variants
    variant(
        "executables",
        values=any_combination_of(
            # CCE
            "CharacteristicExtract",
            "ReduceCceWorldtube",
            # Elliptic / initial data
            "SolvePoisson1D",
            "SolvePoisson2D",
            "SolvePoisson3D",
            "SolveElasticity2D",
            "SolveElasticity3D",
            "SolveXcts",
            # Tools
            "ExportCoordinates1D",
            "ExportCoordinates2D",
            "ExportCoordinates3D",
        ),
        description="Executables to install",
    )
    variant("python", default=True, description="Build Python bindings")
    variant("doc", default=False, description="Build documentation")
    # Build type and debug symbols:
    # - Both Debug and Release builds have debug symbols enabled by default in
    #   the SpECTRE build system, so we can view backtraces, etc., when
    #   production code fails.
    variant(
        "build_type",
        values=("Debug", "Release"),
        default="Release",
        description="CMake build type",
    )
    # - Allow disabling debug symbols to reduce memory usage and executable size
    variant("debug_symbols", default=True, description="Build with debug symbols")
    variant("shared", default=False, description="Build shared libraries instead of static")
    variant(
        "memory_allocator",
        values=("system", "jemalloc"),
        multi=False,
        default="system",
        description="Which memory allocator to use",
    )
    variant(
        "openmp",
        default=False,
        when="@2024.03.19:",
        description=(
            "Enable OpenMP parallelization in some parts of the code"
            " (Python bindings and exporter)"
        ),
    )
    variant(
        "formaline",
        default=True,
        description=(
            "Write the source tree into simulation output files "
            "to increase reproducibility of results"
        ),
    )
    variant(
        "profiling", default=False, description="Enable options to make profiling SpECTRE easier"
    )

    # Compiler support
    conflicts("%gcc@:8", when="@2022.06.14:")
    conflicts("%gcc@:6")
    conflicts("%clang@:12", when="@2023.10.11:")
    conflicts("%clang@:7")
    conflicts("%apple-clang@:12", when="@2023.10.11:")
    conflicts("%apple-clang@:10")

    # Build dependencies
    depends_on("cmake@3.18:", when="@2023.02.09:", type="build")
    depends_on("cmake@3.12:", type="build")
    depends_on("python@2.7:", type="build")

    # Link dependencies
    depends_on("charmpp@7.0.0:", when="@2022.09.02:")
    depends_on("charmpp@6.10.2:")
    depends_on("blaze@3.8")
    depends_on("boost@1.60:+math+program_options")
    depends_on("brigand@master")
    depends_on("gsl")
    depends_on("hdf5")
    depends_on("jemalloc", when="memory_allocator=jemalloc")
    depends_on("libsharp~mpi~openmp")
    depends_on("libxsmm@1.16.1:1")
    depends_on("blas")
    depends_on("lapack")
    depends_on("yaml-cpp@0.6:")

    # Test dependencies
    depends_on("catch2@3.4.0:3", when="@2023.08.18:", type="test")
    depends_on("catch2@2.8:2", when="@:2023.07.29", type="test")
    depends_on("py-numpy@1.10:", type="test")
    depends_on("py-scipy", type="test")
    depends_on("py-h5py", type="test")

    # Python bindings
    with when("+python"):
        extends("python")
        depends_on("python@3.8:", when="@2023.08.18:", type=("build", "run"))
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("py-pybind11@2.6:", type="build")
        depends_on("py-click", when="@2022.12.16:", type=("build", "run"))
        depends_on("py-h5py@3.5.0:", type=("build", "run"))
        depends_on("py-humanize", when="@2023.04.07:", type=("build", "run"))
        depends_on("py-jinja2", when="@2023.07.29:", type=("build", "run"))
        depends_on("py-numpy@1.10:", type=("build", "run"))
        depends_on("py-scipy", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
        depends_on("py-pandas@1.5:1", when="@2023.04.07:", type=("build", "run"))
        depends_on("py-pyyaml", type=("build", "run"))
        depends_on("py-rich", when="@2022.12.16:", type=("build", "run"))

    # Docs
    with when("+doc"):
        depends_on("doxygen", type="build")
        depends_on("perl", type="build", when="@2022.03.07:")
        depends_on("py-beautifulsoup4", type="build")
        depends_on("py-pybtex", type="build")
        depends_on("py-nbconvert", type="build", when="@2022.03.07:")

    # Incompatibilities
    # - Shared libs builds on macOS don't work before
    #   https://github.com/sxs-collaboration/spectre/pull/2680
    conflicts("+shared", when="@:2022.01.03 platform=darwin")
    # - Blaze with `BLAZE_BLAS_MODE` enabled doesn't work before
    #   https://github.com/sxs-collaboration/spectre/pull/3806 because it
    #   doesn't find the BLAS header. Also, we haven't tested Blaze with BLAS
    #   kernels before then.
    conflicts("^blaze+blas", when="@:2022.02.17")

    # Patch Charm++ v7.0.0 for Python bindings (see
    # https://github.com/sxs-collaboration/spectre/pull/3942 and
    # https://github.com/UIUC-PPL/charm/issues/3600)
    depends_on(
        "charmpp@6.10.2:",
        patches=patch(
            "https://raw.githubusercontent.com/sxs-collaboration/spectre/develop/support/Charm/v7.0.0.patch",
            sha256="576c745de202f030275aaeb3c6206f7ebdda696385353e0d1417ed7c47b856ca",
            when="@7.0.0",
        ),
        when="@2022.06.14: +python platform=linux",
    )

    # These patches backport updates to the SpECTRE build system to earlier
    # releases, to support installing them with Spack. In particular, we try to
    # support releases associated with published papers, so their results are
    # reproducible.
    # - Backport installation of targets, based on upstream patch:
    #   https://github.com/sxs-collaboration/spectre/commit/fe3514117c8205dbf18c4d42ec17712e67d33251
    patch("install-pre-2022.01.03.patch", when="@:2022.01.03")
    # - Backport experimental support for Charm++ v7+
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/a2203824ef38ec79a247703ae8cd215befffe391.patch?full_index=1",
        sha256="e1b22e5ebeb814c07f4aff690b7b4f3a7ba1f06ea4bc91468c68637521a458a7",
        when="@:2022.01.03 ^charmpp@7.0.0:",
    )
    # - Backport IWYU toggle to avoid CMake configuration issues
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/cffeba1bc24bf7c00ec8bac710f02d3db36fa111.patch?full_index=1",
        sha256="a3752024b743aeba6f7a53d26bf583e1e46adbd08a2e6f74470a777dde7b2dff",
        when="@:2022.01.03",
    )
    # - Backport patch for Boost 1.77
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/001fc190a6ec73ad6c19ada9444d04a2320f2b96.patch?full_index=1",
        sha256="96b3a3cb49ee30206eb70d1160feda84b7e7b4e1c7dd81ba7138b5c4fa718622",
        when="@:2022.01.03 ^boost@1.77:",
    )
    # - Backport patch for Python 3.10 in tests
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/82ff2c39cdae0ecc1e42bdf4564506a4ca869818.patch?full_index=1",
        sha256="36cdb5e48f6b49306709057e5e6ca37a44258ad6ecf918c1e87a71d7121e36ba",
        when="@:2022.01.03 ^python@3.10:",
    )
    # - Backport patch for hdf5+mpi
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/eb887635f5e2b394ae2c7e96170e9d907eb315cf.patch?full_index=1",
        sha256="ccc4631541d6aca996ced358a3ee43d3f8b8eb62fd7bec4534685445688d4d84",
        when="@:2022.01.03 ^hdf5+mpi",
    )
    # - Backport `BUILD_TESTING` toggle, based on upstream patch:
    #   https://github.com/sxs-collaboration/spectre/commit/79bed6cad6e95efadf48a5846f389e90801202d4
    patch("build-testing-pre-2022.01.03.patch", when="@:2022.01.03")
    # - Backport `PYTHONPATH` in CTest environment
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/ada1d15d5963bd22581dd8966599e1529a99645d.patch?full_index=1",
        sha256="6ae3d5b08bd3f0e743e1043c9363e32db2a4f9c549eb958ff989f1e7f3078f6c",
        when="@:2022.01.03",
    )
    # - Backport executable name CTest labels
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/1b61e62a27b02b658cc6a74c4d46af1f5b5d0a4d.patch?full_index=1",
        sha256="aeb41c30dd7a8bf61b79efbb79cfa81372cfc2e870a2b494fc583a8bd554c703",
        when="@:2022.01.03",
    )
    # - Backport fix for PCH builds with Spack
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/4bb3f25f905f83d8295a28a8036f6971dc4e75a2.patch?full_index=1",
        sha256="6e8ec4584b6b03866594d0744c041012c68f6b2382abaa9abeec39cd2f2a6480",
        when="@:2022.01.03",
    )
    # - Backport installation of shared libs
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/b7c54a2a20c6d62aae6b1c97e3468d4cd39ed6ad.patch?full_index=1",
        sha256="5ce050c73bab007c0bea9c1f4ae4fb5cd5abab820eeb89cf6cb81f8856d07c30",
        when="@:2022.01.03 +shared",
    )
    # - Fix an issue with Boost pre v1.67
    patch(
        "https://github.com/sxs-collaboration/spectre/commit/b229e939f15362aca892d4480a9182daf88305d4.patch?full_index=1",
        sha256="87811b73d72d60cf82cd85e464b42843add50c3be858c7c8272936aeb8574933",
        when="@2022.02.08 ^boost@:1.66",
    )

    def cmake_args(self):
        args = [
            self.define("CHARM_ROOT", self.spec["charmpp"].prefix),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_PYTHON_BINDINGS", "python"),
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_DOCS", "doc"),
            self.define("USE_GIT_HOOKS", False),
            self.define("USE_IWYU", False),
            self.define_from_variant("USE_FORMALINE", "formaline"),
            self.define_from_variant("ENABLE_OPENMP", "openmp"),
            self.define_from_variant("MEMORY_ALLOCATOR").upper(),
            self.define_from_variant("ENABLE_PROFILING", "profiling"),
            self.define("USE_PCH", True),
            self.define_from_variant("DEBUG_SYMBOLS"),
        ]
        # Allow for more time on slower machines
        if self.run_tests:
            if self.spec.satisfies("@:2022.01.03"):
                args.extend(
                    [
                        self.define("SPECTRE_INPUT_FILE_TEST_TIMEOUT_FACTOR", "10"),
                        self.define("SPECTRE_UNIT_TEST_TIMEOUT_FACTOR", "10"),
                        self.define("SPECTRE_PYTHON_TEST_TIMEOUT_FACTOR", "10"),
                    ]
                )
            else:
                args.append(self.define("SPECTRE_TEST_TIMEOUT_FACTOR", "10"))
        return args

    @property
    def build_targets(self):
        spec = self.spec
        targets = list(self.spec.variants["executables"].value)
        if "none" in targets:
            targets.remove("none")
        if "+python" in spec:
            targets.append("all-pybindings")
        if "+doc" in spec:
            targets.append("doc")
        if self.run_tests:
            targets.append("unit-tests")
        if len(targets) == 0:
            raise InstallError(
                "Specify at least one target to build. See "
                "'spack info spectre' for available targets."
            )
        return targets

    @run_after("install")
    def install_docs(self):
        if "+doc" in self.spec:
            with working_dir(self.build_directory):
                install_tree(join_path("docs", "html"), self.prefix.docs)

    @property
    def archive_files(self):
        # Archive the `BuildInfo.txt` file for debugging builds
        return super().archive_files + [join_path(self.build_directory, "BuildInfo.txt")]

    def check(self):
        with working_dir(self.build_directory):
            # The test suite contains a lot of tests. We select only those
            # related to the targets that were specified.
            # - Unit tests
            ctest("--output-on-failure", "-L", "unit")
            # - Input file tests for the specified executables
            for executable in self.spec.variants["executables"].value:
                if executable == "none":
                    continue
                ctest("--output-on-failure", "-L", executable)
