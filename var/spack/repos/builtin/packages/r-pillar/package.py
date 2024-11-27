# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPillar(RPackage):
    """Coloured Formatting for Columns.

    Provides a 'pillar' generic designed for formatting columns of data using
    the full range of colours provided by modern terminals."""

    cran = "pillar"

    license("MIT")

    version("1.9.0", sha256="f23eb486c087f864c2b4072d5cba01d5bebf2f554118bcba6886d8dbceb87acc")
    version("1.8.1", sha256="2f06a7cc9e5638390c9b98a6ec9a9ec1beec0f2b9dbdfa42e39a5ab2456d87ec")
    version("1.7.0", sha256="7841f89658cc8935568c0ff24dc480b4481bac896de2f6447050abc4360a13bb")
    version("1.6.5", sha256="22fbf1ba0677fbd15cb35729fe4e97fab751a4c1de3eb8a4694f86b2be411bdb")
    version("1.6.4", sha256="033a92a271ddeec2a17323d070de8257b9ca4d57f5be6181e2ad35fe7e1ea19e")
    version("1.4.7", sha256="cdedb2b2a4854e917f43b0c6379efefda9d7ff4e58dec2a3159a80ee8288f298")
    version("1.4.2", sha256="bababb76b6db06dc32ccd947dbad6c164a1749ff5b558c6783ad03570f010825")
    version("1.4.1", sha256="f571ca7a3ef0927747510b972da31a26da24b9da68990fe1bbc9d4ae58028c55")
    version("1.3.1", sha256="b338b55f956dd7134f379d39bb94dfb25e13cf27999d6a6e6dc9f292755acbf6")
    version("1.3.0", sha256="aed845ae4888be9a7340eed57536e3fe6cb46e89d905897fb9b0635797cfcae0")
    version("1.2.3", sha256="c81d1b5c6b55d789a6717dc3c7be1200eb0efbcfc5013db00d553d9cafd6f0e7")
    version("1.2.2", sha256="676d6e64754ce42c2789ca3521eeb576c873afc3b09adfdf2c97f03cbcddb8ce")
    version("1.2.1", sha256="6de997a43416f436039f2b8b47c46ea08d2508f8ad341e0e1fd878704a3dcde7")
    version("1.2.0", sha256="fd042b525b27e5f700e5299f50d25710501a4f35556b6a04b430776568962416")
    version("1.1.0", sha256="58a29e8d0d3a47150caf8cb1aba5dc5eca233ac8d4626f4b23beb8b5ae9003be")
    version("1.0.1", sha256="7b37189ab9ab0bbf2e6f49e9d5e678acb31500739d3c3ea2b5326b457716277d")
    version("1.0.0", sha256="7478d0765212c5f0333b8866231a6fe350393b7fa49840e6fed3516ac64540dc")

    depends_on("r-cli", type=("build", "run"))
    depends_on("r-cli@2.3.0:", type=("build", "run"), when="@1.7.0:")
    depends_on("r-fansi", type=("build", "run"))
    depends_on("r-glue", type=("build", "run"), when="@1.6.5:")
    depends_on("r-lifecycle", type=("build", "run"), when="@1.4.7:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"))
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-utf8@1.1.0:", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"), when="@1.4.0:")
    depends_on("r-vctrs@0.2.0:", type=("build", "run"), when="@1.4.7:")
    depends_on("r-vctrs@0.3.8:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-vctrs@0.5.0:", type=("build", "run"), when="@1.9.0:")

    depends_on("r-crayon@1.3.4:", type=("build", "run"), when="@:1.7.0")
    depends_on("r-ellipsis", type=("build", "run"), when="@1.4.7:1.7.0")
    depends_on("r-ellipsis@0.3.2", type=("build", "run"), when="@1.6.1:1.7.0")
