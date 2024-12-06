# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Openpbs(AutotoolsPackage):
    """OpenPBS software optimizes job scheduling and workload
    management in high-performance computing (HPC) environments - clusters,
    clouds, and supercomputers - improving system efficiency and people's
    productivity."""

    homepage = "https://www.openpbs.org"
    url = "https://github.com/openpbs/openpbs/archive/v19.1.3.tar.gz"

    license("AGPL-3.0-only")

    version("20.0.1", sha256="685a4abcea92bf518df02b544d25e237ae8cef76f86525f7bf3554812e9f50fa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("perl", type="build")

    depends_on("ssmtp", type=("build", "run"))
    depends_on("xauth", type=("build", "run"))

    depends_on("python@3.5:3.9", type=("build", "link", "run"))

    depends_on("libx11")
    depends_on("libice")
    depends_on("libsm")
    depends_on("openssl")
    depends_on("postgresql")
    depends_on("expat")
    depends_on("libedit")
    depends_on("ncurses")
    depends_on("hwloc@:1")
    depends_on("libical")
    depends_on("swig")
    depends_on("tcl")
    depends_on("tk")
    depends_on("zlib-api")

    # The configure script cannot properly handle dependencies in non-system
    # directories.
    patch("with_lib.patch")

    # The package does not really depend on libcrypt but links to it. We
    # eliminate this redundant dependency to avoid linking to a system library.
    patch("no_crypt.patch")

    # Fix installation directories.
    patch("install.patch")

    # Link to the dynamic library of Python instead of the static one.
    patch("python.patch")

    # Provides PBS functionality
    provides("pbs")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def configure_args(self):
        return [
            "--x-includes=%s" % self.spec["libx11"].prefix.include,
            "--x-libraries=%s" % self.spec["libx11"].prefix.lib,
            "--with-pbs-server-home=%s" % self.spec.prefix.var.spool.pbs,
            "--with-database-dir=%s" % self.spec["postgresql"].prefix,
            "--with-pbs-conf-file=%s" % self.spec.prefix.etc.join("pbs.conf"),
            "--with-expat=%s" % self.spec["expat"].prefix,
            "--with-editline=%s" % self.spec["libedit"].prefix,
            "--with-hwloc=%s" % self.spec["hwloc"].prefix,
            "--with-libical=%s" % self.spec["libical"].prefix,
            "--with-sendmail=%s" % self.spec["ssmtp"].prefix.sbin.sendmail,
            "--with-swig=%s" % self.spec["swig"].prefix,
            "--with-tcl=%s" % self.spec["tcl"].prefix,
            # The argument --with-tk is introduced with with_lib.patch
            "--with-tk=%s" % self.spec["tk"].prefix,
            "--with-xauth=xauth",
            "--with-libz=%s" % self.spec["zlib-api"].prefix,
        ]

    @run_after("install")
    def post_install(self):
        # Calling the postinstall script requires root privileges
        # Executable(self.prefix.libexec.pbs_postinstall)()
        tty.warn(
            self.spec.format(
                "To finalize the installation of {name}, you need to run "
                '"{prefix}/libexec/pbs_postinstall" with root privileges'
            )
        )
