# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMarkdown(RPackage):
    """Render Markdown with the C Library 'Sundown'.

    Provides R bindings to the 'Sundown' 'Markdown' rendering library
    (https://github.com/vmg/sundown). 'Markdown' is a plain-text formatting
    syntax that can be converted to 'XHTML' or other formats. See
    https://en.wikipedia.org/wiki/Markdown for more information about
    'Markdown'."""

    cran = "markdown"

    license("MIT")

    version("1.13", sha256="385421c674cf5bf2ba04d1df7c16bb5d857bec03755a36321999ac37f5b3cfd9")
    version("1.6", sha256="46228b8d8161ae4b651b4662364eb35a3b91e6a7a457fe99d0e709f2a6f559ea")
    version("1.3", sha256="b1773e94e7b927c3a8540c2704b06e0f7721a0e3538a93abd58fff420ecb30f1")
    version("1.1", sha256="8d8cd47472a37362e615dbb8865c3780d7b7db694d59050e19312f126e5efc1b")
    version("1.0", sha256="172d8072d1829644ee6cdf54282a55718e2cfe9c9915d3589ca5f9a016f8d9a6")
    version("0.9", sha256="3068c6a41ca7a76cbedeb93b7371798f4d8437eea69a23c0ed5204c716d1bf23")
    version("0.8", sha256="538fd912b2220f2df344c6cca58304ce11e0960de7bd7bd573b3385105d48fed")
    version("0.7.7", sha256="0b86c3a4e42bbc425be229f70a4a0efdca0522f48c6ea1bf0285c6b122854102")

    depends_on("r@2.11.1:", type=("build", "run"))
    depends_on("r-commonmark", type=("build", "run"), when="@1.3:")
    depends_on("r-commonmark@1.9.0:", type=("build", "run"), when="@1.6:")
    depends_on("r-xfun", type=("build", "run"), when="@1.1:")
    depends_on("r-xfun@0.38:", type=("build", "run"), when="@1.6:")
    depends_on("r-mime@0.3:", type=("build", "run"), when="@:1.3")
