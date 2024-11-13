# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdrm(AutotoolsPackage, MesonPackage):
    """A userspace library for accessing the DRM, direct rendering manager,
    on Linux, BSD and other systems supporting the ioctl interface."""

    homepage = "https://dri.freedesktop.org/libdrm/"
    url = "https://dri.freedesktop.org/libdrm/libdrm-2.4.101.tar.xz"
    list_url = "https://dri.freedesktop.org/libdrm/"
    git = "https://gitlab.freedesktop.org/mesa/drm"

    maintainers("wdconinc")

    license("MIT")

    version("2.4.123", sha256="a2b98567a149a74b0f50e91e825f9c0315d86e7be9b74394dae8b298caadb79e")
    version("2.4.122", sha256="d9f5079b777dffca9300ccc56b10a93588cdfbc9dde2fae111940dfb6292f251")
    version("2.4.121", sha256="909084a505d7638887f590b70791b3bbd9069c710c948f5d1f1ce6d080cdfcab")
    version("2.4.120", sha256="3bf55363f76c7250946441ab51d3a6cc0ae518055c0ff017324ab76cdefb327a")
    version("2.4.119", sha256="0a49f12f09b5b6e68eaaaff3f02ca7cff9aa926939b212d343161d3e8ac56291")
    version("2.4.118", sha256="a777bd85f2b5fc9c57f886c82058300578317cafdbc77d0a769d7e9a9567ab88")
    version("2.4.117", sha256="a2888d69e3eb1c8a77adc08a75a60fbae01f0d208d26f034d1a12e362361242b")
    version("2.4.116", sha256="46c53f40735ea3d26d614297f155f6131a510624a24274f654f6469ca905339a")
    version("2.4.115", sha256="554cfbfe0542bddb391b4e3e05bfbbfc3e282b955bd56218d21c0616481f65eb")
    version("2.4.114", sha256="3049cf843a47d12e5eeefbc3be3496d782fa09f42346bf0b7defe3d1e598d026")
    version("2.4.113", sha256="7fd7eb2967f63beb4606f22d50e277d993480d05ef75dd88a9bd8e677323e5e1")
    version("2.4.112", sha256="00b07710bd09b35cd8d80eaf4f4497fe27f4becf467a9830f1f5e8324f8420ff")
    version("2.4.111", sha256="1ad7164f77424de6f4ecba7c262bde196a214c6e19a6fbf497f0815f4d7ab2a9")
    version("2.4.110", sha256="eecee4c4b47ed6d6ce1a9be3d6d92102548ea35e442282216d47d05293cf9737")
    version("2.4.109", sha256="629352e08c1fe84862ca046598d8a08ce14d26ab25ee1f4704f993d074cb7f26")
    version("2.4.108", sha256="a1d7948cbc536763fde14b4beb5e4da7867607966d4cf46301087e8b8fe3d6a0")
    version("2.4.107", sha256="c554cef03b033636a975543eab363cc19081cb464595d3da1ec129f87370f888")
    version("2.4.100", sha256="6a5337c054c0c47bc16607a21efa2b622e08030be4101ef4a241c5eb05b6619b")
    version("2.4.81", sha256="64036c5e0668fdc2b820dcc0ebab712f44fd2c2147d23dc5a6e003b19f0d3e9f")
    version("2.4.75", sha256="a411bff814b4336c8908dcbd045cd89fdc7afedc75b795d897d462e467cbb01d")
    version("2.4.70", sha256="73615b9c1c4852e5ce045efa19c866e8df98e396b2443bf859eea05574ecb64f")
    version("2.4.59", sha256="ed9d03a92c2d80e6310cc350db3430620f1659ae084a07c6824cee7bc81ae8fa")
    version("2.4.33", sha256="bd2a8fecf28616f2157ca33ede691c139cc294ed2d0c4244b62ca7d22e98e5a4")

    depends_on("c", type="build")

    variant("docs", default=False, description="Build man pages")

    depends_on("pkgconfig", type="build")
    depends_on("libpciaccess@0.10:")
    depends_on("libpthread-stubs")

    # 2.4.90 is the first version to use meson, but spack supports meson since 2.4.101.
    build_system(
        conditional("meson", when="@2.4.101:"),
        conditional("autotools", when="@:2.4.100"),
        default="meson",
    )

    with when("build_system=meson"):
        depends_on("meson@0.53:", type="build", when="@2.4.101:")
        depends_on("meson@0.59:", type="build", when="@2.4.117:")

    # >= 2.4.104 uses reStructuredText for man pages.
    with when("@2.4.104: +docs"):
        depends_on("py-docutils", type="build")

    # < 2.4.104 uses docbook for man pages.
    with when("@:2.4.103 +docs"):
        depends_on("docbook-xml", type="build")
        depends_on("docbook-xsl", type="build")
        depends_on("libxslt", type="build")

    def url_for_version(self, version):
        if version <= Version("2.4.100"):
            return self.list_url + "libdrm-%s.tar.gz" % version
        else:
            return self.list_url + "libdrm-%s.tar.xz" % version


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []
        args.append("--enable-static")
        if self.version <= Version("2.4.70"):
            # Needed to fix build for spack/spack#1740, but breaks newer
            # builds/compilers
            args.append("LIBS=-lrt")
        if (
            self.spec.satisfies("%gcc@10.0.0:")
            or self.spec.satisfies("%clang@11.0.0:")
            or self.spec.satisfies("%aocc@2.3.0:")
        ):
            args.append("CFLAGS=-fcommon")
        return args


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        if self.spec.satisfies("@:2.4.112"):
            return ["-Dman-pages=" + ("true" if self.spec.satisfies("+docs") else "false")]
        else:
            return ["-Dman-pages=" + ("enabled" if self.spec.satisfies("+docs") else "disabled")]
