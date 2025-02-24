# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWebshot(RPackage):
    """Take Screenshots of Web Pages.

    Takes screenshots of web pages, including Shiny applications and R Markdown
    documents."""

    cran = "webshot"

    license("GPL-2.0-only")

    version("0.5.5", sha256="d675913ccac80e0af8ee396f95a24124eae6c42d80aed9f47f7a88218ecbb913")
    version("0.5.4", sha256="3dc2b9baef7855e1deea060276b9ccc6375eee36b7100987cbb1f8e5cd7a8f24")
    version("0.5.3", sha256="b7c4f2be61c8c4730202a9c3604072478e30cb85b423b7497cd703cc3f49dbc0")
    version("0.5.2", sha256="f183dc970157075b51ac543550a7a48fa3428b9c6838abb72fe987c21982043f")
    version("0.5.1", sha256="b9750d206c6fa0f1f16cc212b0a34f4f4bfa916962d2c877f0ee9a33620f4b23")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-callr", type=("build", "run"))
    depends_on("imagemagick", type="run")

    # need a phantomjs package to make this actually work.
