# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Rpm(AutotoolsPackage):
    """
    The RPM package manager
    https://github.com/rpm-software-management/rpm/blob/master/INSTALL
    Note that debugedit is an additional tool that *should* compile with
    adding libdw and elfutils, but the library (as of 4.16.1.2) is being
    removed from rpm and will be put somewhere else.
    """

    homepage = "https://github.com/rpm-software-management/rpm"
    url = "https://github.com/rpm-software-management/rpm/archive/rpm-4.16.0-release.tar.gz"
    git = "https://github.com/rpm-software-management/rpm.git"

    maintainers("haampie")

    version("master", branch="master")
    version("4.18.2", sha256="8be0a812b2e707c72ae486b54db18ae211dd4158ad35e32b308d662c59a75e85")
    version("4.16.1.2", sha256="3d2807807a8ccaa92a8ced74e09b5bf5b2417a5bbf9bee4abc7c6aa497547bf3")
    version("4.16.0", sha256="a62b744e3404b107e8467e1a36ff0f2bf9e5c1b748dbfeb36db54bbb859446ea")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "crypto",
        values=("openssl", "libgcrypt"),
        default="libgcrypt",
        multi=False,
        description="What cryptographic library to use",
    )
    variant("sqlite", default=False, description="Use sqlite instead of ndb")
    variant(
        "berkeley-db",
        values=("full", "readonly", "none"),
        default="none",
        multi=False,
        description="Type of support for Berkeley DB",
    )
    variant("selinux", default=False, description="Enable support for SELinux")
    variant("python", default=False, description="Build Python bindings to RPM library")
    variant("lua", default=True, description="Build with lua support")
    variant("zstd", default=False, description="Build with zstd suport")
    variant(
        "posix", default=False, description="Enable POSIX.1e draft 15 file capabilities support"
    )
    variant("gpg", default=False, description="Install gpg for using cryptographic signatures")
    variant("openmp", default=True, description="OpenMP multithreading support")
    variant("nls", default=False, description="Enable native language support")

    # Always required
    depends_on("popt")

    # Without this file patch, we don't detect lua
    depends_on("lua+pcfile@5.3.5:", when="+lua")

    # Enable POSIX.1e draft 15 file capabilities support
    depends_on("libcap", when="+posix")
    depends_on("berkeley-db@4.5:", when="berkeley-db=full")
    depends_on("berkeley-db@4.5:", when="berkeley-db=readonly")

    depends_on("gettext", when="+nls")
    depends_on("gettext", type="build")
    depends_on("iconv")
    depends_on("file")  # provides magic.h
    depends_on("libarchive")

    # support for cryptographic signatures
    depends_on("gnupg", when="+gpg")

    # cryptographic library to support digests and signatures
    depends_on("libgcrypt", when="crypto=libgcrypt")
    depends_on("openssl@1.0.2:", when="crypto=openssl")

    # RPM needs some database, ndb requires no extra dependencies but sqlite does
    depends_on("sqlite@3.22.0:", when="+sqlite")

    # Python 2.x support is being deprecated
    depends_on("python@3.1:", when="+sqlite")

    # compression support -- there is no configure option for many of these
    # and they autodetect the libraries, so it's better to just make them
    # hard requirements to avoid linking against system libraries.
    depends_on("zlib-api")
    depends_on("bzip2")
    depends_on("gzip")
    depends_on("xz")
    depends_on("lzma")
    with when("+zstd"):
        depends_on("zstd")
        depends_on("zstd@1.3.8:", when="@4.17:")

    # java jar dependency analysis (already requirement for lua)
    depends_on("unzip", type="run")

    # Build dependencies
    depends_on("doxygen", type="build")
    depends_on("pandoc", type="build", when="@4.17:")
    depends_on("pkgconfig", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # Lua is about to become a hard requirement
    conflicts("~lua", when="@4.17:")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh", "--noconfigure")

    def configure_args(self):
        spec = self.spec

        args = [
            "--enable-ndb",
            "--disable-inhibit-plugin",
            "--with-crypto={0}".format(spec.variants["crypto"].value),
        ]

        args += self.enable_or_disable("nls")
        args += self.enable_or_disable("sqlite")
        args += self.with_or_without("selinux")
        args += self.with_or_without("python")
        # OpenMP multithreading support automatically enabled if C compiler has
        # support for OpenMP version 4.5 or higher
        args += self.enable_or_disable("openmp")

        # Option got removed in 4.17
        if self.spec.satisfies("@:4.16"):
            args += self.with_or_without("lua")

        # Legacy berkely db support
        if "berkeley-db=full" in spec:
            args.extend(["--enable-bdb", "--disable-bdb-ro"])
        elif "berkeley-db=readonly" in spec:
            args.extend(["--disable-bdb", "--enable-bdb-ro"])
        else:
            args.extend(["--disable-bdb", "--disable-bdb-ro"])

        # enable POSIX.1e draft 15 file capabilities support
        if "+posix" in spec:
            args.append("--with-cap")

        if "crypto=openssl" in spec:
            tty.warn(openssl_warning)

        return args


# This warning is from the INSTALL about licensing when using openssl.
# We need to show it to the user if they choose the openssl variant.

openssl_warning = """
When compiling against OpenSSL, there is a possible license incompatibility.
For more details on this, see https://people.gnome.org/~markmc/openssl-and-the-gpl.html
Some Linux distributions have different legal interpretations of this
possible incompatibility. It is recommended to consult with a lawyer before
building RPM against OpenSSL.
Fedora: https://fedoraproject.org/wiki/Licensing:FAQ#What.27s_the_deal_with_the_OpenSSL_license.3F
Debian: https://lists.debian.org/debian-legal/2002/10/msg00113.html"""
