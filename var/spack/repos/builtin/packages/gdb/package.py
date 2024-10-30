# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gdb(AutotoolsPackage, GNUMirrorPackage):
    """GDB, the GNU Project debugger, allows you to see what is going on
    'inside' another program while it executes -- or what another
    program was doing at the moment it crashed.
    """

    homepage = "https://www.gnu.org/software/gdb"
    gnu_mirror_path = "gdb/gdb-11.2.tar.gz"

    maintainers("robertu94")

    license("GPL-3.0-or-later AND LGPL-3.0-or-later")

    version("14.2", sha256="2de5174762e959a5e529e20c20d88a04735469d8fffd98f61664e70b341dc47c")
    version("14.1", sha256="683e63182fb72bd5d8db32ab388143796370a8e3e71c26bc264effb487db7927")
    version("13.2", sha256="7ead13d9e19fa0c57bb19104e1a5f67eefa9fc79f2e6360de491e8fddeda1e30")
    version("13.1", sha256="4cc3d7143d6d54d289d227b1e7289dbc0fa4cbd46131ab87136e1ea831cf46d4")
    version("12.1", sha256="87296a3a9727356b56712c793704082d5df0ff36a34ca9ec9734fc9a8bdfdaab")
    version("11.2", sha256="b558b66084835e43b6361f60d60d314c487447419cdf53adf83a87020c367290")
    version("11.1", sha256="cc2903474e965a43d09c3b263952d48ced39dd22ce2d01968f3aa181335fcb9c")
    version("10.2", sha256="b33ad58d687487a821ec8d878daab0f716be60d0936f2e3ac5cf08419ce70350")
    version("10.1", sha256="f12f388b99e1408c01308c3f753313fafa45517740c81ab7ed0d511b13e2cf55")
    version("9.2", sha256="38ef247d41ba7cc3f6f93a612a78bab9484de9accecbe3b0150a3c0391a3faf0")
    version("9.1", sha256="fcda54d4f35bc53fb24b50009a71ca98410d71ff2620942e3c829a7f5d614252")
    version("8.3.1", sha256="26ce655216cd03f4611518a7a1c31d80ec8e884c16715e9ba8b436822e51434b")
    version("8.3", sha256="b2266ec592440d0eec18ee1790f8558b3b8a2845b76cc83a872e39b501ce8a28")
    version("8.2.1", sha256="0107985f1edb8dddef6cdd68a4f4e419f5fec0f488cc204f0b7d482c0c6c9282")
    version("8.2", sha256="847e4b65e5a7b872e86019dd59659029e2b06cae962e0ef345f169dcb4b851b8")
    version("8.1", sha256="e54a2322da050e4b00785370a282b9b8f0b25861ec7cfbbce0115e253eea910e")
    version("8.0.1", sha256="52017d33cab5b6a92455a1a904046d075357abf24153470178c0aadca2d479c5")
    version("8.0", sha256="8968a19e14e176ee026f0ca777657c43456514ad41bb2bc7273e8c4219555ac9")
    version("7.12.1", sha256="142057eacecfb929d52b561eb47a1103c7d504cec3f659dd8a5ae7bc378f7e77")
    version("7.11.1", sha256="57e9e9aa3172ee16aa1e9c66fef08b4393b51872cc153e3f1ffdf18a57440586")
    version("7.10.1", sha256="ff14f8050e6484508c73cbfa63731e57901478490ca1672dc0b5e2b03f6af622")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("python", default=True, description="Compile with Python support", when="@8.2:")
    variant("xz", default=True, description="Compile with lzma support")
    variant("source-highlight", default=False, description="Compile with source-highlight support")
    variant("lto", default=False, description="Enable lto")
    variant("quad", default=False, description="Enable quad")
    variant("gold", default=False, description="Enable gold linker")
    variant("ld", default=False, description="Enable ld")
    variant("tui", default=False, description="Enable tui")
    variant("debuginfod", default=True, description="Enable debuginfod support", when="@10.1:")

    # Resolves the undefined references to libintl_gettext while linking gdbserver
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
    patch("gdb-libintl-10.patch", level=0, when="@10.1:11.0")
    patch("gdb-libintl-11.patch", level=0, when="@11.1:")

    # Upstream patch and backport to fix build with glibc@2.25:
    # http://lists.busybox.net/pipermail/buildroot/2017-March/188055.html
    patch(
        "https://git.buildroot.net/buildroot/plain/package/gdb/7.11.1/0002-Sync-proc_service-definition-with-GLIBC.patch?id=a8a2e5288ed4704907383b10bab704fca211f5db",
        sha256="f2648907cc22f7d02551d0018d44848f9db9fc5cdfda4fea65906a372f4f551b",
        when="@7.11.1",
    )
    patch(
        "https://git.buildroot.net/buildroot/plain/package/gdb/7.10.1/0007-Sync-proc_service-definition-with-GLIBC.patch?id=a8a2e5288ed4704907383b10bab704fca211f5db",
        sha256="6bfa89d9989d70167b307e6b0aa5f72dd0bc3d124553c4b54b270f8c4adf5fdc",
        when="@7.10.1",
    )

    # Silence warnings about imp being deprecated on new python versions
    # https://sourceware.org/pipermail/gdb-patches/2021-February/176622.html
    patch("importlib.patch", when="@8.3.1:10.2 ^python@3.4:")

    # Required dependency
    depends_on("texinfo", type="build")

    # Optional dependencies
    with when("+python"), default_args(type=("build", "link", "run")):
        depends_on("python")
        # gdb@9.2 will segmentation fault if it builds with python@3.9.
        # https://bugzilla.redhat.com/show_bug.cgi?id=1829702
        depends_on("python@:3.8", when="@:9.2")
        # pyOS_ReadlineTState became private API in cpython commit
        # d228825e08883fc13f35eb91435f95d32524931c
        depends_on("python@:3.12", when="@:14.2")
    depends_on("xz", when="+xz")
    depends_on("zlib-api")
    depends_on("zstd", when="@13.1:")
    depends_on("pkgconfig", type="build", when="@13.1:")
    depends_on("source-highlight", when="+source-highlight")
    depends_on("ncurses", when="+tui")
    depends_on("gmp", when="@11.1:")
    depends_on("elfutils@0.179:+debuginfod", when="@10.1:+debuginfod")
    depends_on("mpfr@4.2:", when="@14:")

    build_directory = "spack-build"

    def configure_args(self):
        args = [
            "--with-system-gdbinit={}".format(self.prefix.etc.gdbinit),
            "--with-system-zlib",
            *self.enable_or_disable("lto"),
            *self.with_or_without("quad"),
            *self.enable_or_disable("gold"),
            *self.enable_or_disable("ld"),
            *self.enable_or_disable("tui"),
            *self.with_or_without("debuginfod"),
        ]

        if self.spec.satisfies("@13.1:"):
            args.append("--with-zstd")

        if self.spec.version >= Version("11.1"):
            args.append("--with-gmp={}".format(self.spec["gmp"].prefix))

        if self.spec.satisfies("+python"):
            args.append("--with-python={}".format(self.spec["python"].command))
            args.append("LDFLAGS={}".format(self.spec["python"].libs.ld_flags))

        return args

    @run_after("install")
    def gdbinit(self):
        if self.spec.satisfies("+python"):
            tool = self.spec["python"].command.path + "-gdb.py"
            if os.path.exists(tool):
                mkdir(self.prefix.etc)
                with open(self.prefix.etc.gdbinit, "w") as gdbinit:
                    gdbinit.write("add-auto-load-safe-path {0}\n".format(tool))

    def check(self):
        """The GDB testsuite is extensive and is hard to pass. Skip it for now."""
        pass
