# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FontUtil(AutotoolsPackage, XorgPackage):
    """X.Org font package creation/installation utilities and fonts."""

    homepage = "https://cgit.freedesktop.org/xorg/font/util"
    xorg_mirror_path = "font/font-util-1.3.1.tar.gz"

    license("custom")

    version("1.4.1", sha256="f029ae80cdd75d89bee7f7af61c21e07982adfb9f72344a158b99f91f77ef5ed")
    version("1.4.0", sha256="30b90fe52347916be9b08f95f717f17c9c1f58bef8cabb49014d0fdd2b0df643")
    version("1.3.2", sha256="f115a3735604de1e852a4bf669be0269d8ce8f21f8e0e74ec5934b31dadc1e76")
    version("1.3.1", sha256="34ebb0c9c14e0a392cdd5ea055c92489ad88d55ae148b2f1cfded0f3f63f2b5b")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    depends_on("bdftopcf", type="build")
    depends_on("mkfontscale", type="build")
    depends_on("mkfontdir", type="build")

    font_baseurl = "https://www.x.org/archive/individual/font/"
    default_fonts = []
    fonts = []
    # name, version, sha256
    fonts_resource = [
        ["encodings", "1.0.4", "55861d9cf456bd717a3d30a3193402c02174ed3c0dcee828798165fe307ee324"],
        [
            "font-alias",
            "1.0.3",
            "63087cb61d17bfc9cd6f4f9359f63a3b1dd83300a31a42fd93dca084724c6afb",
        ],
        [
            "font-adobe-100dpi",
            "1.0.3",
            "97d9c1e706938838e4134d74f0836ae9d9ca6705ecb405c9a0ac8fdcbd9c2159",
        ],
        [
            "font-adobe-75dpi",
            "1.0.3",
            "61eb1fcfec89f7435cb92cd68712fbe4ba412ca562b1f5feec1f6daa1b8544f6",
        ],
        [
            "font-adobe-utopia-100dpi",
            "1.0.4",
            "e8c3417d89183b1fc383fb3e0f3948c0d01fabcb9edace8b7ec85eab8cdc18c4",
        ],
        [
            "font-adobe-utopia-75dpi",
            "1.0.4",
            "254be39c09da1c4e77d2a75a2969330ee2db395120a428671c50aef3ab745fc0",
        ],
        [
            "font-adobe-utopia-type1",
            "1.0.4",
            "d9e86a8805b0fb78222409169d839a8531a1f5c7284ee117ff2a0af2e5016c3f",
        ],
        [
            "font-arabic-misc",
            "1.0.3",
            "3022b6b124f4cc6aade961f8d1306f67ff42e3b7922fb2244847f287344aefea",
        ],
        [
            "font-bh-100dpi",
            "1.0.3",
            "817703372f080d6508cf109011b17f3572ff31047559fe82d93b487ca4e4e2d9",
        ],
        [
            "font-bh-75dpi",
            "1.0.3",
            "720b6a513894bfc09a163951ec3dd8311201e08ee40e8891547b6c129ffb5fce",
        ],
        [
            "font-bh-ttf",
            "1.0.3",
            "c583b4b968ffae6ea30d5b74041afeac83126682c490a9624b770d60d0e63d59",
        ],
        [
            "font-bh-type1",
            "1.0.3",
            "d5602f1d749ccd31d3bc1bb6f0c5d77400de0e5e3ac5abebd2a867aa2a4081a4",
        ],
        [
            "font-bh-lucidatypewriter-100dpi",
            "1.0.3",
            "5e05a642182ec6a77bd7cacb913d3c86b364429329a5f223b69792d418f90ae9",
        ],
        [
            "font-bh-lucidatypewriter-75dpi",
            "1.0.3",
            "38301bbdb6374494f30c0b44acc7052ed8fc2289e917e648ca566fc591f0a9e0",
        ],
        [
            "font-bitstream-100dpi",
            "1.0.3",
            "0a8c77c1540dc376fb2bb5a02bd33ee5f3563fbac9fc07c7947cac462c4bb48a",
        ],
        [
            "font-bitstream-75dpi",
            "1.0.3",
            "c43ae370932eb8a4789a5b1f9801da15228b0d4c803251785c38d82aef024a4b",
        ],
        [
            "font-bitstream-speedo",
            "1.0.2",
            "aeea5f130480a3f05149bde13d240e668d8fb4b32c02b18914fcccd1182abe72",
        ],
        [
            "font-bitstream-type1",
            "1.0.3",
            "3399b7586c18be509cdaeceeebf754b861faa1d8799dda1aae01aeb2a7a30f01",
        ],
        [
            "font-cronyx-cyrillic",
            "1.0.3",
            "d64b9bfa5fa8dedf084f1695997cc32149485d2a195c810f62a1991ab5cd5519",
        ],
        [
            "font-cursor-misc",
            "1.0.3",
            "a0b146139363dd0a704c7265ff9cd9150d4ae7c0d248091a9a42093e1618c427",
        ],
        [
            "font-daewoo-misc",
            "1.0.3",
            "21166546b0490aa3ec73215fa4ea28d91c6027b56178800ba51426bd3d840cc3",
        ],
        [
            "font-dec-misc",
            "1.0.3",
            "c4923342f6068c83fd4f5dbcf60d671c28461300db7e2aee930c8634b1e4b74a",
        ],
        [
            "font-ibm-type1",
            "1.0.3",
            "4509703e9e581061309cf4823bffd4a93f10f48fe192a1d8be1f183fd6ab9711",
        ],
        [
            "font-isas-misc",
            "1.0.3",
            "493965263070a5ee2a301dfdb2e87c1ca3c00c7882bfb3dd99368565ba558ff5",
        ],
        [
            "font-jis-misc",
            "1.0.3",
            "57c2db8824865117287d57d47f2c8cf4b2842d036c7475534b5054be69690c73",
        ],
        [
            "font-micro-misc",
            "1.0.3",
            "97ee77a9d8ca3e7caf0c78c386eb0b96e8a825ca3642ec035cfb83f5f2cf1475",
        ],
        [
            "font-misc-cyrillic",
            "1.0.3",
            "79dfde93d356e41c298c2c1b9c638ec1a144f438d5146d0df6219afb1c2b8818",
        ],
        [
            "font-misc-ethiopic",
            "1.0.3",
            "d3b93f7f73a526919bf73a38e10ef4643cd541403a682a8068d54bbcdd9c7e27",
        ],
        [
            "font-misc-meltho",
            "1.0.3",
            "eaddfc6d9b32bf38c9dc87c354be3b646a385bc8d9de6e536269f6e1ca50644e",
        ],
        [
            "font-misc-misc",
            "1.1.2",
            "46142c876e176036c61c0c24c0a689079704d5ca5b510d48c025861ee2dbf829",
        ],
        [
            "font-mutt-misc",
            "1.0.3",
            "fcecbfc475dfe5826d137f8edc623ba27d58d32f069165c248a013b3c566bb59",
        ],
        [
            "font-schumacher-misc",
            "1.1.2",
            "dc3b8d5890480943e735e0375f0e0d8333094fcb6d6845ba321b2e39db78d148",
        ],
        [
            "font-screen-cyrillic",
            "1.0.4",
            "9e82783758e8c67a9aadaf1a7222d13418a87455e4ce0a9974fb1df0278bdf74",
        ],
        [
            "font-sun-misc",
            "1.0.3",
            "549c6ba59979da25e85c218a26e5c527c3c24ebab2c76509c1ebc34d94fae227",
        ],
        [
            "font-winitzki-cyrillic",
            "1.0.3",
            "503e70ee66af34f6ec4426c0f4ae708e9d30dafdcd58f671a87c7bf56b1952a3",
        ],
        [
            "font-xfree86-type1",
            "1.0.4",
            "02b3839ae79ba6a7750525bb3b0c281305664b95bf63b4a0baa230a277b4f928",
        ],
    ]
    for f_r in fonts_resource:
        f = f_r[0]
        resource(
            name=f,
            url=font_baseurl + f + "-" + f_r[1] + ".tar.gz",
            sha256=f_r[2],
            destination=f,
            when="fonts=" + f,
        )

        conflicts("fonts=font-bh-ttf", when="arch=linux-rhel7-broadwell")

        if f != "font-bh-ttf":
            default_fonts.append(f)

        fonts.append(f)

    variant(
        "fonts",
        description="Installs fonts",
        values=fonts,
        default=",".join(default_fonts),
        multi=True,
    )

    def setup_build_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("PKG_CONFIG_PATH", self.prefix.lib.pkgconfig)

    @run_after("install")
    def font_install(self):
        autoconf_args = ["-ifv"]
        p = join_path(self.spec["util-macros"].prefix, "share", "aclocal")
        autoconf_args.append(f"--include={p}")
        p = join_path(self.spec.prefix, "share", "aclocal")
        autoconf_args.append(f"--include={p}")
        fonts = self.spec.variants["fonts"].value
        autoreconf = which("autoreconf")

        for font in fonts:
            fontroot = find(font, "*", recursive=False)
            with working_dir(fontroot[0]):
                autoreconf(*autoconf_args)
                configure = Executable("./configure")
                configure(f"--prefix={self.prefix}")
                make("install")
