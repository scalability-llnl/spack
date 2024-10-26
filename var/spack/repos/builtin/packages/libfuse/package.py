# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Libfuse(MesonPackage):
    """The reference implementation of the Linux FUSE (Filesystem in
    Userspace) interface"""

    homepage = "https://github.com/libfuse/libfuse"
    url = "https://github.com/libfuse/libfuse/releases/download/fuse-2.9.9/fuse-2.9.9.tar.gz"

    keep_werror = "all"

    version("3.16.2", sha256="1bc306be1a1f4f6c8965fbdd79c9ccca021fdc4b277d501483a711cbd7dbcd6c")
    version("3.11.0", sha256="25a00226d2d449c15b2f08467d6d5ebbb2a428260c4ab773721c32adbc6da072")
    version("3.10.5", sha256="e73f75e58da59a0e333d337c105093c496c0fd7356ef3a5a540f560697c9c4e6")
    version("3.10.4", sha256="bfcb2520fd83db29e9fefd57d3abd5285f38ad484739aeee8e03fbec9b2d984a")
    version("3.10.3", sha256="c32527782cef620df58b162aa29901d1fb13253b029375d5860a2253a810344e")
    version("3.10.2", sha256="a16f93cc083264afd0d2958a0dc88f24c6c5d40a9f3842c645b1909e13edb75f")
    version("3.10.1", sha256="d8954e7b4c022c651aa80db3bb4a161437dd285cd5f1a23d0e25f055dcebe00d")
    version("3.10.0", sha256="52bbb52035f7eeaa54d139e21805d357f848f6e02ac956831d04988165a92c7b")
    version("3.9.4", sha256="9e076ae757a09cac9ce1beb50b3361ae83a831e5abc0f1bf5cdf771cd1320338")
    version("3.9.3", sha256="0f8f7ad9cc6667c6751efa425dd0a665dcc9d75f0b7fc0cb5b85141a514110e9")
    version("3.9.2", sha256="b4409255cbda6f6975ca330f5b04cb335b823a95ddd8c812c3d224ec53478fc0")
    version("2.9.9", sha256="d0e69d5d608cc22ff4843791ad097f554dd32540ddc9bed7638cc6fea7c1b4b5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version < Version("3.0.0"):
            return "https://github.com/libfuse/libfuse/releases/download/fuse-{0}/fuse-{1}.tar.gz".format(
                version, version
            )
        return "https://github.com/libfuse/libfuse/archive/refs/tags/fuse-{0}.tar.gz".format(
            version
        )

    variant(
        "useroot",
        when="+utils",
        default=False,
        description="Use root privileges to make fusermount a setuid binary after installation",
    )
    variant(
        "system_install",
        when="+utils",
        default=False,
        description=(
            "Do not run the post-install script "
            "which typically sets up udev rules and "
            "and init script in /etc/init.d"
        ),
    )
    variant("utils", default=True, description="Build and install helper and example programs.")

    depends_on("autoconf", type="build", when="@:2")
    depends_on("automake", type="build", when="@:2")
    depends_on("libtool", type="build", when="@:2")
    depends_on("gettext", type="build", when="@:2")

    provides("fuse")
    conflicts("+useroot", when="~system_install", msg="useroot requires system_install")
    conflicts("platform=darwin", msg="libfuse does not support OS-X, use macfuse instead")

    # Drops the install script which does system configuration
    patch("0001-Do-not-run-install-script.patch", when="@3:3.11 ~system_install")
    patch(
        "https://src.fedoraproject.org/rpms/fuse3/raw/0519b7bf17c4dd1b31ee704d49f8ed94aa5ba6ab/f/fuse3-gcc11.patch",
        sha256="3ad6719d2393b46615b5787e71778917a7a6aaa189ba3c3e0fc16d110a8414ec",
        when="@3: %gcc@11:",
    )

    patch(
        "https://github.com/libfuse/libfuse/commit/6d55007027dfe7b75a74899f497f075046cc5404.patch?full_index=1",
        sha256="2e265d31628175ce9dcea1ca2e423fdbed9469e2ace6b24a7fe7a72cb54b1da9",
        when="@:2",
    )
    patch(
        "https://github.com/libfuse/libfuse/commit/5d38afc8a5b4a2a6e27aad7a1840046e99cd826d.patch?full_index=1",
        sha256="6b7ea8451d29944adb2fdc1bd119c93e74fe54431b1315f148a071015343ec1a",
        when="@:2",
    )
    # https://bugs.gentoo.org/803923
    patch(
        "https://github.com/libfuse/libfuse/commit/5a43d0f724c56f8836f3f92411e0de1b5f82db32.patch?full_index=1",
        sha256="94d5c6d9785471147506851b023cb111ef2081d1c0e695728037bbf4f64ce30a",
        when="@:2",
    )

    executables = ["^fusermount3?$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"^fusermount.*version: (\S+)", output)
        return match.group(1) if match else None

    def meson_args(self):
        args = []

        if self.spec.satisfies("+utils"):
            args.append("-Dutils=true")
            args.append("-Dexamples=true")
        else:
            args.append("-Dutils=false")
            args.append("-Dexamples=false")

        if self.spec.satisfies("+useroot"):
            args.append("-Duseroot=true")
        else:
            args.append("-Duseroot=false")

        if self.spec.satisfies("~system_install"):
            # Fix meson's setup if meson does not have the host system's udev package:
            args.append("-Dudevrulesdir={0}".format(self.prefix.etc.rules.d))

            if self.spec.satisfies("@3.12:"):
                args.append("-Dinitscriptdir=")
        else:
            # Likewise, but with +system_install, it may install to /lib/udev/rules.d:
            args.append("-Dudevrulesdir={0}".format("/lib/udev/rules.d"))

        return args

    # Before libfuse 3.x this was an autotools package
    @when("@:2")
    def meson(self, spec, prefix):
        ar_args = ["-ivf"]
        for dep in self.spec.dependencies(deptype="build"):
            if os.path.exists(dep.prefix.share.aclocal):
                ar_args.extend(["-I", dep.prefix.share.aclocal])
        autoreconf(*ar_args)

        args = [
            "--prefix={0}".format(prefix),
            "MOUNT_FUSE_PATH={0}".format(self.prefix.sbin),
            "UDEV_RULES_PATH={0}".format(self.prefix.etc),
            "INIT_D_PATH={0}".format(self.prefix.etc),
        ]

        args.append(
            "--enable-static"
            if self.spec.satisfies("default_library=static")
            else "--disable-static"
        )
        args.append(
            "--enable-shared"
            if self.spec.satisfies("default_library=shared")
            else "--disable-shared"
        )

        configure(*args)

    @when("@:2")
    def build(self, spec, prefix):
        make()

    @when("@:2")
    def install(self, spec, prefix):
        make("install")
