# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFs(RPackage):
    """Cross-Platform File System Operations Based on 'libuv'.

    A cross-platform interface to file system operations, built on top of the
    'libuv' C library."""

    cran = "fs"

    license("MIT")

    version("1.6.4", sha256="7e06290f2dbe36f54fdf51b748a4b00b8b0f68967b5754e37e0c83df7fea5ac8")
    version("1.6.2", sha256="548b7c0ed5ab26dc4fbd88707ae12987bcaef834dbc6de4e17d453846dc436b2")
    version("1.5.2", sha256="35cad1781d6d17c1feb56adc4607079c6844b63794d0ce1e74bb18dbc11e1987")
    version("1.5.0", sha256="36df1653571de3c628a4f769c4627f6ac53d0f9e4106d9d476afb22ae9603897")
    version("1.3.1", sha256="d6934dca8f835d8173e3fb9fd4d5e2740c8c04348dd2bcc57df1b711facb46bc")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.6.2:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.6.4:")
    depends_on("gmake", type="build")

    depends_on("r-rcpp", type=("build", "run"), when="@:1.3.1")
