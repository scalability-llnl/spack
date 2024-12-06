# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geos(CMakePackage):
    """GEOS (Geometry Engine, Open Source).

    GEOS is a C/C++ library for computational geometry with a focus on algorithms used in
    geographic information systems (GIS) software. It implements the OGC Simple Features
    geometry model and provides all the spatial functions in that standard as well as many
    others. GEOS is a core dependency of PostGIS, QGIS, GDAL, and Shapely.
    """

    homepage = "https://libgeos.org/"
    url = "https://download.osgeo.org/geos/geos-3.8.1.tar.bz2"
    git = "https://github.com/libgeos/geos.git"

    license("LGPL-2.1-or-later")
    maintainers("adamjstewart")

    version("3.13.0", sha256="47ec83ff334d672b9e4426695f15da6e6368244214971fabf386ff8ef6df39e4")
    version("3.12.2", sha256="34c7770bf0090ee88488af98767d08e779f124fa33437e0aabec8abd4609fec6")
    version("3.12.1", sha256="d6ea7e492224b51193e8244fe3ec17c4d44d0777f3c32ca4fb171140549a0d03")
    version("3.12.0", sha256="d96db96011259178a35555a0f6d6e75a739e52a495a6b2aa5efb3d75390fbc39")
    version("3.11.4", sha256="364c88ccfc38aa50cf65c700e7b2ae4706ed103326128493dbf750c78d136d2c")
    version("3.11.3", sha256="80d60a2bbc0cde7745a3366b9eb8c0d65a142b03e063ea0a52c364758cd5ee89")
    version("3.11.2", sha256="b1f077669481c5a3e62affc49e96eb06f281987a5d36fdab225217e5b825e4cc")
    version("3.11.1", sha256="6d0eb3cfa9f92d947731cc75f1750356b3bdfc07ea020553daf6af1c768e0be2")
    version("3.11.0", sha256="79ab8cabf4aa8604d161557b52e3e4d84575acdc0d08cb09ab3f7aaefa4d858a")
    version("3.10.6", sha256="078403158da66cad8be39ad1ede5e2fe4b70dcf7bb292fb06a65bdfe8afa6daf")
    version("3.10.5", sha256="cc47d95e846e2745c493d8f9f3a9913b1c61f26717a1165898da64352aec4dde")
    version("3.10.4", sha256="d6fc11bcfd265cbf2714199174e4c3392d657551e5fd84c74c07c863b29357e3")
    version("3.10.3", sha256="3c141b07d61958a758345d5f54e3c735834b2f4303edb9f67fb26914f0d44770")
    version("3.10.2", sha256="50bbc599ac386b4c2b3962dcc411f0040a61f204aaef4eba7225ecdd0cf45715")
    version("3.10.1", sha256="a8148eec9636814c8ab0f8f5266ce6f9b914ed65b0d083fc43bb0bbb01f83648")
    version("3.10.0", sha256="097d70e3c8f688e59633ceb8d38ad5c9b0d7ead5729adeb925dbc489437abe13")
    version("3.9.5", sha256="c6c9aedfa8864fb44ba78911408442382bfd0690cf2d4091ae3805c863789036")
    version("3.9.4", sha256="70dff2530d8cd2dfaeeb91a5014bd17afb1baee8f0e3eb18e44d5b4dbea47b14")
    version("3.9.3", sha256="f8b2314e311456f7a449144efb5e3188c2a28774752bc50fc882a3cd5c89ee35")
    version("3.9.2", sha256="44a5a9be21d7d473436bf621c2ddcc3cf5a8bbe3c786e13229618a3b9d861297")
    version("3.9.1", sha256="7e630507dcac9dc07565d249a26f06a15c9f5b0c52dd29129a0e3d381d7e382a")
    version("3.9.0", sha256="bd8082cf12f45f27630193c78bdb5a3cba847b81e72b20268356c2a4fc065269")
    version("3.8.4", sha256="6de8c98c1ae7cb0cd2d726a8dc9b7467308c4b4e05f9df94742244e64e441499")
    version("3.8.3", sha256="f98315d1ba35c8d1a94a2947235f9e9dfb7057fdec343683f64ff9ad1061255c")
    version("3.8.2", sha256="5a102f4614b0c9291504bbefd847ebac18ea717843506bd251d015c7cf9726b4")
    version("3.8.1", sha256="4258af4308deb9dbb5047379026b4cd9838513627cb943a44e16c40e42ae17f7")
    version("3.8.0", sha256="99114c3dc95df31757f44d2afde73e61b9f742f0b683fd1894cbbee05dda62d5")
    version("3.7.2", sha256="2166e65be6d612317115bfec07827c11b403c3f303e0a7420a2106bc999d7707")
    version("3.6.2", sha256="045a13df84d605a866602f6020fc6cbf8bf4c42fb50de237a08926e1d7d7652a")
    version("3.6.1", sha256="4a2e4e3a7a09a7cfda3211d0f4a235d9fd3176ddf64bd8db14b4ead266189fc5")
    version("3.6.0", sha256="1fe7644f3240c8422b0143830ff142e44e8b01333c12f67681ccaab92142f2ea")
    version("3.5.1", sha256="e6bb0a7ba0e142b1e952fae9d946b2b532fa05a5c384e458f7cb8990e1fcac32")
    version("3.5.0", sha256="49982b23bcfa64a53333dab136b82e25354edeb806e5a2e2f5b8aa98b1d0ae02")
    version("3.4.3", sha256="cfbf68079117c1c2b76411636444ff41d73c31093c4cab9dcc9a8c1bbe7e3897")
    version("3.4.2", sha256="15e8bfdf7e29087a957b56ac543ea9a80321481cef4d4f63a7b268953ad26c53")
    version("3.4.1", sha256="d07ac375f3edd12425d6ce5a96db9739d5ff358cbdf60c6804f7a9e565af8ff2")
    version("3.4.0", sha256="3b2106d9baeede39d70e22672598d40cb63ee901f54436c774b250726d7bbdd5")
    version("3.3.9", sha256="3e2156165d593f3e85df9ac223170b2c11de3cb4697e4c7a761c3ffbf04fe0ee")
    version("3.3.8", sha256="ebecd4d1a71bcc28e5e883296cd8c52a80d5596335e74728f320989734fa503b")
    version("3.3.7", sha256="fd01c21b54a3c48cac3e7885f26d4ca10ea9944238776b8ce03489e5e45c592b")
    version("3.3.6", sha256="7ee6c1da9a1b87a3e29209e7cddbf19d36f9689d8e44fec2c9bcf6a1b1be3898")
    version("3.3.5", sha256="3b513fbe2d155364d61e76d9c250d6d8e75b5166783a233596c744373cb5874f")
    version("3.3.4", sha256="cd5400aa5f3fe32246dfed5d238c5017e1808162c865c016480b3e6c07271904")
    version("3.3.3", sha256="dfcf4bd70ab212a5b7bad21d01b84748f101a545092b56dafdc3882ef3bddec9")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    generator("ninja")
    depends_on("cmake@3.15:", when="@3.13:", type="build")
    depends_on("cmake@3.13:", when="@3.10:", type="build")
    depends_on("cmake@3.8:", type="build")

    variant("shared", default=True, description="Build shared library")

    patch(
        "https://github.com/libgeos/geos/pull/461.patch?full_index=1",
        sha256="ab78db7ff2e8fc89e899b8233cf77d90b24d88940dd202c4219decba479c8d35",
        when="@3.8:3.9",
    )

    @property
    def command(self):
        return Executable(self.prefix.bin.join("geos-config"))

    def cmake_args(self):
        args = []

        # https://github.com/libgeos/geos/issues/460
        if self.spec.satisfies("%intel"):
            args.append(self.define("BUILD_ASTYLE", False))

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return args
