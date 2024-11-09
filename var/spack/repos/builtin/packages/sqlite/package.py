# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys
from tempfile import NamedTemporaryFile

import spack.platforms
from spack.package import *

is_windows = sys.platform == "win32"


class Sqlite(AutotoolsPackage, NMakePackage):
    """SQLite is a C-language library that implements a small, fast,
    self-contained, high-reliability, full-featured, SQL database engine.
    """

    homepage = "https://www.sqlite.org"
    tags = ["windows"]

    license("blessing")

    version("3.46.0", sha256="6f8e6a7b335273748816f9b3b62bbdc372a889de8782d7f048c653a447417a7d")
    version("3.45.3", sha256="b2809ca53124c19c60f42bf627736eae011afdcc205bb48270a5ee9a38191531")
    version("3.45.1", sha256="cd9c27841b7a5932c9897651e20b86c701dd740556989b01ca596fcfa3d49a0a")
    version("3.44.2", sha256="1c6719a148bc41cf0f2bbbe3926d7ce3f5ca09d878f1246fcc20767b175bb407")
    version("3.43.2", sha256="6d422b6f62c4de2ca80d61860e3a3fb693554d2f75bb1aaca743ccc4d6f609f0")
    version("3.42.0", sha256="7abcfd161c6e2742ca5c6c0895d1f853c940f203304a0b49da4e1eca5d088ca6")
    version("3.40.1", sha256="2c5dea207fa508d765af1ef620b637dcb06572afa6f01f0815bd5bbf864b33d9")
    version("3.40.0", sha256="0333552076d2700c75352256e91c78bf5cd62491589ba0c69aed0a81868980e7")
    version("3.39.4", sha256="f31d445b48e67e284cf206717cc170ab63cbe4fd7f79a82793b772285e78fdbb")
    version("3.39.2", sha256="852be8a6183a17ba47cee0bbff7400b7aa5affd283bf3beefc34fcd088a239de")
    version("3.38.5", sha256="5af07de982ba658fd91a03170c945f99c971f6955bc79df3266544373e39869c")
    version("3.38.3", sha256="61f2dd93a2e38c33468b7125967c3218bf9f4dd8365def6025e314f905dc942e")
    version("3.37.2", sha256="4089a8d9b467537b3f246f217b84cd76e00b1d1a971fe5aca1e30e230e46b2d8")
    version("3.37.1", sha256="40f22a13bf38bbcd4c7ac79bcfb42a72d5aa40930c1f3f822e30ccce295f0f2e")
    version("3.37.0", sha256="731a4651d4d4b36fc7d21db586b2de4dd00af31fd54fb5a9a4b7f492057479f7")
    version("3.36.0", sha256="bd90c3eb96bee996206b83be7065c9ce19aef38c3f4fb53073ada0d0b69bbce3")
    version("3.35.5", sha256="f52b72a5c319c3e516ed7a92e123139a6e87af08a2dc43d7757724f6132e6db0")
    version("3.35.4", sha256="7771525dff0185bfe9638ccce23faa0e1451757ddbda5a6c853bb80b923a512d")
    version("3.35.3", sha256="ecbccdd440bdf32c0e1bb3611d635239e3b5af268248d130d0445a32daf0274b")
    version("3.34.0", sha256="bf6db7fae37d51754737747aaaf413b4d6b3b5fbacd52bdb2d0d6e5b2edd9aee")
    version("3.33.0", sha256="106a2c48c7f75a298a7557bcc0d5f4f454e5b43811cc738b7ca294d6956bbb15")
    version("3.32.3", sha256="a31507123c1c2e3a210afec19525fd7b5bb1e19a6a34ae5b998fbd7302568b66")
    version("3.31.1", sha256="62284efebc05a76f909c580ffa5c008a7d22a1287285d68b7825a2b6b51949ae")
    version("3.30.1", sha256="8c5a50db089bd2a1b08dbc5b00d2027602ca7ff238ba7658fabca454d4298e60")
    version("3.30.0", sha256="e0a8cf4c7a87455e55e10413d16f358ca121ccec687fe1301eac95e2d340fc58")
    version("3.29.0", sha256="8e7c1e2950b5b04c5944a981cb31fffbf9d2ddda939d536838ebc854481afd5b")
    version("3.28.0", sha256="d61b5286f062adfce5125eaf544d495300656908e61fca143517afcc0a89b7c3")
    version("3.27.2", sha256="50c39e85ea28b5ecfdb3f9e860afe9ba606381e21836b2849efca6a0bfe6ef6e")
    version("3.27.1", sha256="54a92b8ff73ff6181f89b9b0c08949119b99e8cccef93dbef90e852a8b10f4f8")
    version("3.27.0", sha256="dbfb0fb4fc32569fa427d3658e888f5e3b84a0952f706ccab1fd7c62a54f10f0")
    version("3.26.0", sha256="5daa6a3fb7d1e8c767cd59c4ded8da6e4b00c61d3b466d0685e35c4dd6d7bf5d")

    depends_on("c", type="build")  # generated
    # All versions prior to 3.26.0 are vulnerable to Magellan when FTS
    # is enabled, see https://blade.tencent.com/magellan/index_en.html

    # no hard readline dep on Windows + no variant support, makefile has minimal to no options
    for plat in ["linux", "darwin", "freebsd"]:
        variant(
            "column_metadata",
            default=True,
            description="Build with COLUMN_METADATA",
            when=f"platform={plat}",
        )
        variant(
            "dynamic_extensions",
            default=True,
            description="Support loadable extensions",
            when=f"platform={plat}",
        )

        depends_on("readline", when=f"platform={plat}")

    variant("fts", default=True, description="Include fts4 and fts5 support")

    # functions variant is always available on Windows platform, otherwise is tied
    # to +dynamic_extensions
    function_condition = "platform=windows" if is_windows else "+dynamic_extensions"
    variant(
        "functions",
        default=is_windows,
        description="Provide mathematical and string extension functions for SQL "
        "queries using the loadable extensions mechanism",
        when=f"{function_condition}",
    )
    variant("rtree", default=True, description="Build with Rtree module")
    depends_on("zlib-api")
    depends_on("tcl", when="platform=windows")

    # See https://blade.tencent.com/magellan/index_en.html
    conflicts("+fts", when="@:3.25")

    resource(
        name="extension-functions",
        url="https://www.sqlite.org/contrib/download/extension-functions.c/download/extension-functions.c?get=25",
        sha256="991b40fe8b2799edc215f7260b890f14a833512c9d9896aa080891330ffe4052",
        expand=False,
        placement={"extension-functions.c?get=25": "extension-functions.c"},
        when="+functions",
    )

    # On some platforms (e.g., PPC) the include chain includes termios.h which
    # defines a macro B0. Sqlite has a shell.c source file that declares a
    # variable named B0 and will fail to compile when the macro is found. The
    # following patch undefines the macro in shell.c
    patch("sqlite_b0.patch", when="@3.18.0:3.21.0")

    # Starting version 3.17.0, SQLite uses compiler built-ins
    # __builtin_sub_overflow(), __builtin_add_overflow(), and
    # __builtin_mul_overflow(), which are not supported by Intel compiler.
    # Starting version 3.21.0 SQLite doesn't use the built-ins if Intel
    # compiler is used.
    patch("remove_overflow_builtins.patch", when="@3.17.0:3.20%intel")

    patch("quote_compiler_in_makefile.patch", when="platform=windows")

    build_system("autotools", "nmake")

    executables = ["^sqlite3$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # `sqlite3 --version` prints only the version number, timestamp, commit
        # hash(?) but not the program name. As a basic sanity check, the code
        # calls re.match() and attempts to match the ISO 8601 date following the
        # version number as well.
        match = re.match(r"(\S+) \d{4}-\d{2}-\d{2}", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        all_variants = []

        def call(exe, query):
            with NamedTemporaryFile(mode="w", buffering=1) as sqlite_stdin:
                sqlite_stdin.write(query + "\n")
                e = Executable(exe)
                e(
                    fail_on_error=False,
                    input=sqlite_stdin.name,
                    output=os.devnull,
                    error=os.devnull,
                )
            return e.returncode

        def get_variant(name, has_variant):
            fmt = "+{:s}" if has_variant else "~{:s}"
            return fmt.format(name)

        for exe in exes:
            variants = []

            # check for fts
            def query_fts(version):
                return "CREATE VIRTUAL TABLE name " "USING fts{:d}(sender, title, body);".format(
                    version
                )

            rc_fts4 = call(exe, query_fts(4))
            rc_fts5 = call(exe, query_fts(5))
            variants.append(get_variant("fts", rc_fts4 == 0 and rc_fts5 == 0))

            # check for functions
            # SQL query taken from extension-functions.c usage instructions
            query_functions = "SELECT load_extension('libsqlitefunctions');"
            rc_functions = call(exe, query_functions)
            variants.append(get_variant("functions", rc_functions == 0))

            # check for rtree
            query_rtree = "CREATE VIRTUAL TABLE name USING rtree(id, x, y);"
            rc_rtree = call(exe, query_rtree)
            variants.append(get_variant("rtree", rc_rtree == 0))

            # TODO: column_metadata, dynamic_extensions

            all_variants.append("".join(variants))

        return all_variants

    def url_for_version(self, version):
        if len(version) < 3:
            raise ValueError(f"Unsupported sqlite version: {version}")
        # See https://www.sqlite.org/chronology.html for version -> year
        # correspondence.
        if version >= Version("3.45.0"):
            year = "2024"
        elif version >= Version("3.41.0"):
            year = "2023"
        elif version >= Version("3.37.2"):
            year = "2022"
        elif version >= Version("3.34.1"):
            year = "2021"
        elif version >= Version("3.31.0"):
            year = "2020"
        elif version >= Version("3.27.0"):
            year = "2019"
        elif version >= Version("3.22.0"):
            year = "2018"
        elif version >= Version("3.16.0"):
            year = "2017"
        elif version >= Version("3.10.0"):
            year = "2016"
        elif version >= Version("3.8.8"):
            year = "2015"
        elif version >= Version("3.8.3"):
            year = "2014"
        elif version >= Version("3.7.16"):
            year = "2013"
        else:
            raise ValueError(f"Unsupported sqlite version {version}")
        return f"https://www.sqlite.org/{year}/sqlite-autoconf-{version[0]}{version[1]:02}{version[2]:02}00.tar.gz"

    @property
    def libs(self):
        prefix = "lib" if sys.platform != "win32" else ""
        return find_libraries(f"{prefix}sqlite3", root=self.prefix.lib, runtime=False)

    def test_example(self):
        """check example table dump"""

        test_data_dir = self.test_suite.current_test_data_dir
        db_filename = test_data_dir.join("packages.db")

        # Ensure the database only contains one table
        sqlite3 = which(self.prefix.bin.sqlite3)
        out = sqlite3(db_filename, ".tables", output=str.split, error=str.split)
        assert "packages" in out

        # Ensure the database dump matches expectations, where special
        # characters are replaced with spaces in the expected and actual
        # output to avoid pattern errors.
        expected = get_escaped_text_output(test_data_dir.join("dump.out"))
        out = sqlite3(db_filename, ".dump", output=str.split, error=str.split)
        check_outputs(expected, out)

    def test_version(self):
        """ensure version is expected"""
        vers_str = str(self.spec.version)

        sqlite3 = which(self.prefix.bin.sqlite3)
        out = sqlite3("-version", output=str.split, error=str.split)
        assert vers_str in out


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []

        if self.get_arch() == "ppc64le":
            args.append("--build=powerpc64le-redhat-linux-gnu")

        args.extend(self.enable_or_disable("fts4", variant="fts"))
        args.extend(self.enable_or_disable("fts5", variant="fts"))

        # Ref: https://www.sqlite.org/rtree.html
        args.extend(self.enable_or_disable("rtree"))

        # Ref: https://www.sqlite.org/loadext.html
        args.extend(self.enable_or_disable("dynamic-extensions", variant="dynamic_extensions"))

        # Ref: https://www.sqlite.org/compile.html
        if "+column_metadata" in self.spec:
            args.append("CPPFLAGS=-DSQLITE_ENABLE_COLUMN_METADATA=1")

        return args

    def get_arch(self):
        host_platform = spack.platforms.host()
        return str(host_platform.target("default_target"))

    @run_after("install")
    def build_libsqlitefunctions(self):
        if "+functions" in self.spec:
            libraryname = "libsqlitefunctions." + dso_suffix
            cc = Executable(spack_cc)
            cc(
                self.pkg.compiler.cc_pic_flag,
                "-lm",
                "-shared",
                "extension-functions.c",
                "-o",
                libraryname,
            )
            install(libraryname, self.prefix.lib)


class NMakeBuilder(spack.build_systems.nmake.NMakeBuilder):
    @property
    def makefile_name(self):
        return "Makefile.msc"

    def nmake_args(self):
        enable_fts = "1" if "+fts" in self.spec else "0"
        enable_rtree = "1" if "+rtree" in self.spec else "0"
        enable_functions = "1" if "+functions" in self.spec else "0"

        opts = (
            "OPTS="
            f"-DSQLITE_ENABLE_FTS3={enable_fts} "
            f"-DSQLITE_ENABLE_FTS4={enable_fts} "
            f"-DSQLITE_ENABLE_FTS5={enable_fts} "
            f"-DSQLITE_ENABLE_RTREE={enable_rtree} "
            "-DSQLITE_ENABLE_JSON1=1 "
            "-DSQLITE_ENABLE_GEOPOLY=1 "
            "-DSQLITE_ENABLE_SESSION=1 "
            "-DSQLITE_ENABLE_PREUPDATE_HOOK=1 "
            "-DSQLITE_ENABLE_SERIALIZE=1 "
            f"-DSQLITE_ENABLE_MATH_FUNCTIONS={enable_functions}"
        )

        return ["USE_NATIVE_LIBPATHS=1", "DYNAMIC_SHELL=1", opts]

    def install(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.include)
            mkdirp(prefix.lib)
            mkdirp(prefix.bin)
            install(f"{self.build_directory}\\*.exe", prefix.bin)
            install(f"{self.build_directory}\\*.dll", prefix.bin)
            install(f"{self.build_directory}\\*.lib", prefix.lib)
            install(f"{self.build_directory}\\*.h", prefix.include)
