# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import re

from spack.package import *


class Texlive(AutotoolsPackage):
    """TeX Live is an easy (we hope) way to get up and running with the TeX
    document production system. It provides a comprehensive TeX system with
    binaries for most flavors of Unix, including GNU/Linux, macOS, and also
    Windows. It includes all the major TeX-related programs, macro packages,
    and fonts that are free software, including support for many languages
    around the world."""

    homepage = "https://www.tug.org/texlive"
    url = "https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2020/texlive-20200406-source.tar.xz"
    base_url = "https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/{year}/texlive-{version}-{dist}.tar.xz"
    list_url = "https://ftp.math.utah.edu/pub/tex/historic/systems/texlive"
    list_depth = 1

    license("GPL-2.0-or-later AND GPL-3.0-or-later", checked_by="tgamblin")

    # Add information for new versions below.
    releases = [
        {
            "version": "20240312",
            "year": "2024",
            "sha256_source": "7b6d87cf01661670fac45c93126bed97b9843139ed510f975d047ea938b6fe96",
            "sha256_texmf": "c8eae2deaaf51e86d93baa6bbcc4e94c12aa06a0d92893df474cc7d2a012c7a7",
        },
        {
            "version": "20230313",
            "year": "2023",
            "sha256_source": "3878aa0e1ed0301c053b0e2ee4e9ad999c441345f4882e79bdd1c8f4ce9e79b9",
            "sha256_texmf": "4c4dc77a025acaad90fb6140db2802cdb7ca7a9a2332b5e3d66aa77c43a81253",
        },
        {
            "version": "20220321",
            "year": "2022",
            "sha256_source": "5ffa3485e51eb2c4490496450fc69b9d7bd7cb9e53357d92db4bcd4fd6179b56",
            "sha256_texmf": "372b2b07b1f7d1dd12766cfc7f6656e22c34a5a20d03c1fe80510129361a3f16",
        },
        {
            "version": "20210325",
            "year": "2021",
            "sha256_source": "7aefd96608d72061970f2d73f275be5648ea8ae815af073016d3106acc0d584b",
            "sha256_texmf": "ff12d436c23e99fb30aad55924266104356847eb0238c193e839c150d9670f1c",
        },
        {
            "version": "20200406",
            "year": "2020",
            "sha256_source": "e32f3d08cbbbcf21d8d3f96f2143b64a1f5e4cb01b06b761d6249c8785249078",
            "sha256_texmf": "0aa97e583ecfd488e1dc60ff049fec073c1e22dfe7de30a3e4e8c851bb875a95",
        },
        {
            "version": "20190410",
            "year": "2019",
            "sha256_source": "d2a29fef04e34dc3d2d2296c18995fc357aa7625e7a6bbf40fb92d83d3d0d7b5",
            "sha256_texmf": "c2ec974abc98b91995969e7871a0b56dbc80dd8508113ffcff6923e912c4c402",
        },
    ]

    for release in releases:
        version(
            release["version"],
            sha256=release["sha256_source"],
            url=base_url.format(year=release["year"], version=release["version"], dist="source"),
        )

        resource(
            name="texmf",
            url=base_url.format(year=release["year"], version=release["version"], dist="texmf"),
            sha256=release["sha256_texmf"],
            when="@{0}".format(release["version"]),
        )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("pkgconfig", type="build")

    depends_on("cairo+X")
    depends_on("freetype")
    depends_on("ghostscript")
    depends_on("gmp")
    depends_on("harfbuzz+graphite2")
    depends_on("icu4c")
    depends_on("libgd")
    depends_on("libpaper")
    depends_on("libpng")
    depends_on("libxaw")
    depends_on("libxt")
    depends_on("mpfr")
    depends_on("perl")
    depends_on("pixman")
    depends_on("poppler@:0.83", when="@:2019")
    depends_on("poppler", when="@:2020")
    depends_on("teckit")
    depends_on("zlib-api")
    depends_on("zziplib")
    depends_on("lua-lpeg", when="@20240312:")

    build_directory = "spack-build"

    def tex_arch(self):
        tex_arch = "{0}-{1}".format(platform.machine(), platform.system().lower())
        return tex_arch

    def configure_args(self):
        args = [
            "--bindir={0}".format(join_path(self.prefix.bin, self.tex_arch())),
            "--disable-dvisvgm",
            "--disable-native-texlive-build",
            "--disable-static",
            "--enable-shared",
            "--with-banner-add= - Spack",
            "--dataroot={0}".format(self.prefix),
            "--with-system-cairo",
            "--with-system-freetype2",
            "--with-system-gd",
            "--with-system-gmp",
            "--with-system-graphite2",
            "--with-system-harfbuzz",
            "--with-system-icu",
            "--with-system-libpaper",
            "--with-system-libpng",
            "--with-system-mpfr",
            "--with-system-pixman",
            "--with-system-poppler",
            "--with-system-teckit",
            "--with-system-zlib",
            "--with-system-zziplib",
        ]

        return args

    @run_after("install")
    def setup_texlive(self):
        mkdirp(self.prefix.tlpkg.TeXLive)
        install("texk/tests/TeXLive/*", self.prefix.tlpkg.TeXLive)

        with working_dir("spack-build"):
            make("texlinks")

        copy_tree("texlive-{0}-texmf".format(self.version.string), self.prefix)

        # Create and run setup utilities
        fmtutil_sys = Executable(join_path(self.prefix.bin, self.tex_arch(), "fmtutil-sys"))
        mktexlsr = Executable(join_path(self.prefix.bin, self.tex_arch(), "mktexlsr"))
        mktexlsr()
        fmtutil_sys("--all")
        if self.spec.satisfies("@:2023"):
            mtxrun = Executable(join_path(self.prefix.bin, self.tex_arch(), "mtxrun"))
        else:
            mtxrun_lua = join_path(
                self.prefix, "texmf-dist", "scripts", "context", "lua", "mtxrun.lua"
            )
            chmod = which("chmod")
            chmod("+x", mtxrun_lua)
            mtxrun = Executable(mtxrun_lua)
        mtxrun("--generate")

    def setup_build_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix.bin, self.tex_arch()))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix.bin, self.tex_arch()))

    executables = [r"^tex$"]

    @classmethod
    def determine_version(cls, exe):
        # https://askubuntu.com/questions/100406/finding-the-tex-live-version
        # Thanks to @michaelkuhn that told how to reuse the package releases
        # variable.
        releases = cls.releases
        # tex indicates the year only
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"TeX Live (\d+)", output)
        ver = match.group(1) if match else None
        # We search for the repo actual release
        if ver is not None:
            for release in releases:
                year = release["year"]
                if year == ver:
                    ver = release["version"]
                    break
        return ver
