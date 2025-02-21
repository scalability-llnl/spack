# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDbplyr(RPackage):
    """A 'dplyr' Back End for Databases.

    A 'dplyr' back end for databases that allows you to work with remote
    database tables as if they are in-memory data frames. Basic features works
    with any database that has a 'DBI' back end; more advanced features require
    'SQL' translation to be provided by the package author."""

    cran = "dbplyr"

    license("MIT")

    version("2.5.0", sha256="bb475bdbe89487b189ecc257b5c92007a7458803c81aa77bfc4ed46f5f24bcff")
    version("2.3.2", sha256="0ddc00595ec6b21962d0bb6f470f5f7c9d61c74a4f92681a37e94e1295707fac")
    version("2.2.1", sha256="a6f3f644c068fe1a3b3e99a3a10de55a150d43ef20b5130e6724d142afcb0df7")
    version("2.1.1", sha256="aba4cf47b85ab240fd3ec4cd8d512f6e1958201e151577c1a2ebc3d6ebc5bc08")
    version("2.0.0", sha256="ecd71936ecfefbdda0fad24e52653ac9c0913e01126e467c92c8ba9de37b4069")
    version("1.4.2", sha256="b783f0da2c09a1e63f41168b02c0715b08820f02a351f7ab0aaa688432754de0")
    version("1.4.1", sha256="cfe829f56acdc785c5af21bf3927cf08327504d78c4ae1477c405c81b131da95")
    version("1.2.2", sha256="9d410bb0055fffe10f1f8da55a5b24d98322c7b571d74df61427d5888332bc48")
    version("1.2.1", sha256="b348e7a02623f037632c85fb11be16c40c01755ae6ca02c8c189cdc192a699db")
    version("1.2.0", sha256="02a5fa8dcf8a81c061fdaefa74f17896bee913720418b44dbd226a0d6b30799d")
    version("1.1.0", sha256="7b1e456a2d1056fa6284582cd82d2df66d06b3eea92e9995f5a91a45f246f69d")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.6:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-blob@1.2.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-cli@3.3.0:", type=("build", "run"), when="@2.2.1:")
    depends_on("r-cli@3.4.1:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-cli@3.6.1:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-dbi@1.0.0:", type=("build", "run"))
    depends_on("r-dbi@1.1.3:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-dplyr@0.8.0:", type=("build", "run"))
    depends_on("r-dplyr@1.0.3:", type=("build", "run"), when="@2.1.0")
    depends_on("r-dplyr@1.0.4:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-dplyr@1.0.9:", type=("build", "run"), when="@2.2.1:")
    depends_on("r-dplyr@1.1.0:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-dplyr@1.1.2:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-glue@1.2.0:", type=("build", "run"))
    depends_on("r-glue@1.6.2:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@2.0.0:")
    depends_on("r-lifecycle@1.0.0:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-magrittr", type=("build", "run"), when="@2.0.0:")
    depends_on("r-pillar@1.5.0:", type=("build", "run"), when="@2.2.1:")
    depends_on("r-pillar@1.9.0:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-purrr@0.2.5:", type=("build", "run"))
    depends_on("r-purrr@1.0.1:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-r6@2.2.2:", type=("build", "run"))
    depends_on("r-rlang@0.2.0:", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@2.2.1:")
    depends_on("r-rlang@1.0.6:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-rlang@1.1.1:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-tibble@1.4.2:", type=("build", "run"))
    depends_on("r-tibble@3.2.1:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-tidyr@1.3.0:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-tidyselect@0.2.4:", type=("build", "run"))
    depends_on("r-tidyselect@1.2.0:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-tidyselect@1.2.1:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-vctrs", type=("build", "run"), when="@2.1:")
    depends_on("r-vctrs@0.4.1:", type=("build", "run"), when="@2.2.1:")
    depends_on("r-vctrs@0.5.0:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-vctrs@0.6.3:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-withr", type=("build", "run"), when="@2.0.0:")
    depends_on("r-withr@2.5.0:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-ellipsis", type=("build", "run"), when="@2.1.1")
    depends_on("r-assertthat", type=("build", "run"), when="@:2.2.1")
