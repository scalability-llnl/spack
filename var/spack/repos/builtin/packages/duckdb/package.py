# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Duckdb(MakefilePackage):
    """DuckDB is an in-process SQL OLAP Database Management System."""

    homepage = "https://duckdb.org"
    url = "https://github.com/duckdb/duckdb/archive/refs/tags/v0.9.2.tar.gz"
    git = "https://github.com/duckdb/duckdb.git"

    license("MIT")
    maintainers("glentner", "teaguesterling")

    version("master", branch="master")
    version("1.1.2", sha256="a3319a64c390ed0454c869b2e4fc0af2413cd49f55cd0f1400aaed9069cdbc4c")
    version("1.1.1", sha256="a764cef80287ccfd8555884d8facbe962154e7c747043c0842cd07873b4d6752")
    version("1.1.0", sha256="d9be2c6d3a5ebe2b3d33044fb2cb535bb0bd972a27ae38c4de5e1b4caa4bf68d")
    version("1.0.0", sha256="04e472e646f5cadd0a3f877a143610674b0d2bcf9f4102203ac3c3d02f1c5f26")
    version("0.10.3", sha256="7855587b3491dd488993287caee28720bee43ae28e92e8f41ea4631e9afcbf88")
    version("0.10.2", sha256="662a0ba5c35d678ab6870db8f65ffa1c72e6096ad525a35b41b275139684cea6")
    version(
        "0.10.0",
        sha256="5a925b8607d00a97c1a3ffe6df05c0a62a4df063abd022ada82ac1e917792013",
        deprecated=True,
    )
    version(
        "0.9.2",
        sha256="afff7bd925a98dc2af4039b8ab2159b0705cbf5e0ee05d97f7bb8dce5f880dc2",
        deprecated=True,
    )
    version(
        "0.9.1",
        sha256="37a43188d9354ce3ca101b2b118d867f5f76d04c3b83c09d86fd7508351a631b",
        deprecated=True,
    )
    version(
        "0.9.0",
        sha256="3dbf3326a831bf0797591572440e81a3d6d668f8e33a25ce04efae19afc3a23d",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:")
    with default_args(type="build"):
        depends_on("cmake")
        depends_on("gmake")
        depends_on("ninja", when="+ninjabuild")
        depends_on("py-pip", when="+python")
        depends_on("py-setuptools-scm", when="+python")
        depends_on("pkgconfig", when="+static_openssl")
        depends_on("zlib-api", when="+static_openssl")
    depends_on("openssl", when="+httpfs")
    depends_on("icu4c", when="~icu")

    # Build Options
    variant("cli", default=True, description="Compile with command line client")
    variant("icu", default=False, description="Compile with bundled ICU library")
    variant("ninjabuild", default=True, description="Use GEN=ninja to build")
    variant("static_openssl", default=False, description="Build with static openSSL")
    variant(
        "openssl",
        default=False,
        description="Compile with bundled OpenSSL library",
        when="@:0.9.2",
    )

    variant("extension_autoload", default=False, description="Enable extension auto-loading")
    variant("extension_autoinstall", default=False, description="Enable extension auto-installing")
    variant("extension_repo", default=True, description="Copy extensions to prefix")

    # Extensions
    variant("autocomplete", default=True, description="Include autocomplete for CLI in build")
    variant("excel", default=True, description="Include Excel formatting extension in build")
    variant("fts", default=True, description="Include FTS (full text search) support in build")
    variant("httpfs", default=True, description="Include HTTPFS (& S3) support in build")
    variant("inet", default=True, description="Include INET (ip address) support in build")
    variant("json", default=True, description="Include JSON support in build")
    variant("parquet", default=True, description="Include parquent support in build")
    variant("tpce", default=False, description="Include TPCE in build")
    variant("tpch", default=False, description="Include TPCH in build")

    # APIs
    variant("python", default=True, description="Build with Python driver")
    extends("python", when="+python")

    # Observed failure in an AVX2-specific codeblock on x86_64_v4 target
    conflicts(
        "@1.0.0",
        when="target=x86_64_v3:",
        msg="See: https://github.com/duckdb/duckdb/issues/12362",
    )

    @property
    def duckdb_extension_prefix(self):
        return self.prefix.lib.duckdb

    def setup_build_environment(self, env):
        cmake_args = []  # Future use
        if self.spec.satisfies("+ninjabuild"):
            env.set("GEN", "ninja")
        if self.spec.satisfies("+python"):
            env.set("SETUPTOOLS_SCM_PRETEND_VERSION", f"{self.spec.version}")
        if self.spec.satisfies("+static_openssl"):
            env.set("STATIC_OPENSSL", "1")
        variant_flags = [
            "autocomplete",
            "cli",
            "excel",
            "fts",
            "httpfs",
            "icu",
            "inet",
            "json",
            "openssl",  # Deprecate after 0.9.2 retired
            "parquet",
            "python",
            "tpce",
            "tpch",
        ]
        for flag in variant_flags:
            make_flag = "BUILD_" + flag.upper()
            if "+" + flag in self.spec:
                env.set(make_flag, "1")
            elif "~" + flag in self.spec:
                env.set(make_flag, "0")
        if self.spec.satisfies("@0.10.2:"):
            env.set("OVERRIDE_GIT_DESCRIBE", f"v{self.spec.version}")
        if self.spec.satisfies("+extension_repo"):
            env.set("LOCAL_EXTENSION_REPO", self.prefix.lib.duckdb.extensions)
        if self.spec.satisfies("+extension_autoload"):
            env.set("ENABLE_EXTENSION_AUTOLOADING", "1")
        if self.spec.satisfies("+extension_autoinstall"):
            env.set("ENABLE_EXTENSION_AUTOINSTALL", "1")

        if cmake_args:
            env.set("EXTRA_CMAKE_VARIABLES", " ".join(cmake_args))

    def url_for_version(self, version):
        return "https://github.com/duckdb/duckdb/archive/refs/tags/v{0}.tar.gz".format(version)

    def patch(self):
        # DuckDB pulls its version from a git tag, which it can't find in the tarball
        # and thus defaults to something arbitrary and breaks extensions.
        # We use the Spack version to inject it in the right place during the build
        # Patching is not needed for versions from 0.10.2 onward as we can
        # set OVERRIDE_GIT_DESCRIBE to force the version when not building from a repo.

        version = self.spec.version
        if self.spec.satisfies("@:0.9.2"):
            # Prior to version 0.10.0, this was sufficient
            filter_file(
                r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\}, '
                r'version \$\{DUCKDB_VERSION\}"\))',
                'set(DUCKDB_VERSION "v{0}")\n\\1'.format(version),
                "CMakeLists.txt",
            )
        elif not self.spec.satisfies("@0.10.0"):
            # Override the fallback values that are set when GIT_COMMIT_HASH doesn't work
            for i, n in enumerate(["MAJOR", "MINOR", "PATCH"]):
                filter_file(
                    r"set\(DUCKDB_{0}_VERSION \d+\)".format(n),
                    "set(DUCKDB_{0}_VERSION {1})".format(n, version[i]),
                    "CMakeLists.txt",
                )
            # Need to manually set DUCKDB_NORMALIZED_VERSION for helper scripts
            filter_file(
                r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\},'
                r" version \$\{DUCKDB_VERSION\},"
                r' extension folder \$\{DUCKDB_NORMALIZED_VERSION\}"\))',
                'set(DUCKDB_VERSION "v${DUCKDB_MAJOR_VERSION}'
                '.${DUCKDB_MINOR_VERSION}.${DUCKDB_PATCH_VERSION}")'
                '\nset(DUCKDB_NORMALIZED_VERSION "${DUCKDB_VERSION}")'
                "\n\\1",
                "CMakeLists.txt",
            )

        if self.spec.satisfies("+extension_repo"):
            mkdirp(self.prefix.lib.duckdb.extensions)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdirp(prefix.lib)
        mkdir(prefix.include)
        build_dir = join_path("build", "release")
        install(join_path(build_dir, "duckdb"), prefix.bin)
        install(join_path(build_dir, "src", "libduckdb.so"), prefix.lib)
        install(join_path(build_dir, "src", "libduckdb_static.a"), prefix.lib)
        install_tree(join_path("src", "include"), prefix.include)
