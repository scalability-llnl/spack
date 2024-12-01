# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

from spack.package import *


class BerkeleyDb(AutotoolsPackage):
    """Oracle Berkeley DB"""

    homepage = "https://www.oracle.com/database/technologies/related/berkeleydb.html"
    # URL must remain http:// so Spack can bootstrap curl
    url = "https://download.oracle.com/berkeley-db/db-18.1.40.tar.gz"

    executables = [r"^db_load$"]  # One should be sufficient

    license("UPL-1.0")

    version("18.1.40", sha256="0cecb2ef0c67b166de93732769abdeba0555086d51de1090df325e18ee8da9c8")
    version(
        "18.1.32",
        sha256="fa1fe7de9ba91ad472c25d026f931802597c29f28ae951960685cde487c8d654",
        deprecated=True,
    )
    version("6.2.32", sha256="a9c5e2b004a5777aa03510cfe5cd766a4a3b777713406b02809c17c8e0e7a8fb")
    version("6.1.29", sha256="b3c18180e4160d97dd197ba1d37c19f6ea2ec91d31bbfaf8972d99ba097af17d")
    version(
        "6.0.35",
        sha256="24421affa8ae436fe427ae4f5f2d1634da83d3d55a5ad6354a98eeedb825de55",
        deprecated=True,
    )
    version("5.3.28", sha256="e0a992d740709892e81f9d93f06daf305cf73fb81b545afe72478043172c3628")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("docs", default=False, description="Build documentation")
    variant("cxx", default=True, description="Build with C++ API")
    variant("stl", default=True, description="Build with C++ STL API")

    configure_directory = "dist"
    build_directory = "build_unix"

    patch("drop-docs.patch", when="~docs")
    # Correct autoconf macro to detect TLS support.
    # Patch developed by @eschnett. There is no upstream issue because
    # Oracle's web site does not have instructions for submitting such
    # an issue or pull request.
    patch("tls.patch")

    conflicts("%clang@7:", when="@5.3.28")
    conflicts("%gcc@8:", when="@5.3.28")

    conflicts("+stl", when="~cxx", msg="+stl implies +cxx")

    @classmethod
    def determine_version(cls, exe):
        """Return the version of the provided executable or ``None`` if
        the version cannot be determined.

        Arguments:
            exe (str): absolute path to the executable being examined
        """
        output = Executable(exe)("-V", output=str, error=str)
        match = re.search(r"Berkeley DB\s+([\d\.]+)", output)
        return match.group(1) if match else None

    def patch(self):
        # some of the docs are missing in 18.1.40
        if self.spec.satisfies("@18.1.40"):
            filter_file(r"bdb-sql", "", "dist/Makefile.in")
            filter_file(r"gsg_db_server", "", "dist/Makefile.in")

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--disable-static",
            "--enable-dbm",
            # compat with system berkeley-db on darwin
            "--enable-compat185",
            # SSL support requires OpenSSL, but OpenSSL depends on Perl, which
            # depends on Berkey DB, creating a circular dependency
            "--with-repmgr-ssl=no",
        ]

        config_args += self.enable_or_disable("cxx")
        config_args += self.enable_or_disable("stl")

        # The default glibc provided by CentOS 7 and Red Hat 8 does not provide
        # proper atomic support when using the NVIDIA compilers
        if spec.satisfies("%nvhpc") and (
            spec.satisfies("os=centos7") or spec.satisfies("os=rhel8")
        ):
            config_args.append("--disable-atomicsupport")

        return config_args

    def check_exe_version(self, exe):
        """Check that the installed executable prints the correct version."""
        installed_exe = join_path(self.prefix.bin, exe)
        if not os.path.exists(installed_exe):
            raise SkipTest(f"{exe} is not installed")

        exe = which(installed_exe)
        out = exe("-V", output=str.split, error=str.split)
        assert self.spec.version.string in out

    def test_db_checkpoint(self):
        """check db_checkpoint version"""
        self.check_exe_version("db_checkpoint")

    def test_db_deadlock(self):
        """check db_deadlock version"""
        self.check_exe_version("db_deadlock")

    def test_db_dump(self):
        """check db_dump version"""
        self.check_exe_version("db_dump")

    def test_db_load(self):
        """check db_load version"""
        self.check_exe_version("db_load")

    def test_db_stat(self):
        """check db_stat version"""
        self.check_exe_version("db_stat")

    def test_db_upgrade(self):
        """check db_upgrade version"""
        self.check_exe_version("db_upgrade")

    def test_db_verify(self):
        """check db_verify version"""
        self.check_exe_version("db_verify")
