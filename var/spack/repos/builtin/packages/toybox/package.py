# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Toybox(MakefilePackage):
    """All-in-one Linux command line"""

    homepage = "https://landley.net/toybox/"
    url = "https://landley.net/toybox/downloads/toybox-0.8.11.tar.gz"
    git = "https://github.com/landley/toybox.git"

    maintainers("Buldram")

    license("0BSD", checked_by="Buldram")

    version("0.8.11", sha256="15aa3f832f4ec1874db761b9950617f99e1e38144c22da39a71311093bfe67dc")
    version("0.8.10", sha256="d3afee05ca90bf425ced73f527e418fecd626c5340b5f58711a14531f8d7d108")
    version("0.8.9", sha256="06913dde3de7139b40f947bd7f23869dfc8796e9c6ff39de02719f8b7b2d47ad")
    version("0.8.8", sha256="dafd41978d40f02a61cf1be99a2b4a25812bbfb9c3157e679ee7611202d6ac58")
    version("0.8.7", sha256="b508bf336f82cb0739b77111f945931d1a143b5a53905cb753cd2607cfdd1494")
    version("0.8.6", sha256="4298c90a2b238348e4fdc9f89eb4988356c80da3f0cf78c279d2e82b9119034b")
    version("0.8.5", sha256="bfd230c187726347f7e31a1fc5841705871dfe4f3cbc6628f512b54e57360949")
    version("0.8.4", sha256="cb2a565a8d30015d08d73628795dca51a85b99b149aeabbbecd9e8dbdbd8fddc")
    version("0.8.3", sha256="eab28fd29d19d4e61ef09704e5871940e6f35fd35a3bb1285e41f204504b5c01")
    version("0.8.2", sha256="9a2760fa442e9baf1be6064ab5ba8b90f2098e1d4bc33c788960b8d73f52fed5")
    version("0.8.1", sha256="1ac41e62b809d2ab656479f7f4e20bb71c63c14473f5c7d13f25d4f7fcfefdb3")
    version("0.8.0", sha256="e3ccecd9446db909437427a026c2788f2a96ac7ebc591c95b35df77f4e923956")
    version("0.7.8", sha256="4962e16898cb3c6e2719205349c8e6749a30583618a264aa8911f9ad61d998d6")
    version("0.7.7", sha256="ee218ab21c80044c04112ada7f59320062c35909a6e5f850b1318b17988ffba0")
    version("0.7.6", sha256="e2c9643ebc2bcdec4d8f8db25d0b428dbe0928f7b730052dbbd25db47fb9db95")
    version("0.7.5", sha256="3ada450ac1eab1dfc352fee915ea6129b9a4349c1885f1394b61bd2d89a46c04")
    version("0.7.4", sha256="49d74ca897501e5c981516719870fe08581726f5c018abe35ef52c6f0de113e7")

    conflicts("platform=darwin", when="@:0.7.8,=0.8.1")
    conflicts("platform=freebsd", when="@:0.7.8,0.8.1:0.8.8")

    variant("userland", default=True, description="Install symlinked individual commands")
    variant("static", default=False, description="Build static binary")
    variant("ssl", default=True, description="Build with OpenSSL support")
    variant("zlib", default=True, description="Build with Zlib support")

    depends_on("c", type="build")
    depends_on("bash", type="build")
    depends_on("sed", type="build")
    depends_on("openssl", type="link", when="+ssl")
    depends_on("zlib-api", type="link", when="+zlib")

    # CVE-2022-32298
    patch(
        "https://github.com/landley/toybox/commit/6d4847934fc0fe47a3254ce6c0396d197a780cf4.patch?full_index=1",
        sha256="2c6ffad53102db23b620fd883636daad15c70a08c72f802a1fbcf96c331280cc",
        when="@=0.8.7",
    )
    # Fixes segfault when building with more recent toolchains.
    patch(
        "https://github.com/landley/toybox/commit/78289203031afc23585035c362beec10db54958d.patch?full_index=1",
        sha256="a27a831eb80f9d46809f619b52018eb2e481758581f7a6932423b95422f23911",
        when="@=0.7.4",
    )

    def setup_build_environment(self, env):
        env.set("NOSTRIP", 1)

        if not self.spec.satisfies("@=0.8.9"):
            env.set("V", 1)  # Verbose

        if self.spec.satisfies("+static"):
            env.append_flags("LDFLAGS", "--static")

    def edit(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            defconfig = "macos_defconfig"
        elif spec.satisfies("platform=freebsd"):
            defconfig = "bsd_defconfig"
        else:
            defconfig = "defconfig"

        make(defconfig, parallel=self.parallel and not spec.satisfies("@0.7.8:0.8.1"))

        config = FileFilter(".config")
        config.filter(
            "# CONFIG_TOYBOX_LIBCRYPTO is not set",
            "CONFIG_TOYBOX_LIBCRYPTO=" + ("y" if spec.satisfies("+ssl") else "n"),
        )
        config.filter(
            "# CONFIG_TOYBOX_LIBZ is not set",
            "CONFIG_TOYBOX_LIBZ=" + ("y" if spec.satisfies("+zlib") else "n"),
        )

    def install(self, spec, prefix):
        if spec.satisfies("+userland"):
            make("install_flat", "PREFIX=" + prefix.bin)
        else:
            mkdir(prefix.bin)
            install("toybox", prefix.bin)
