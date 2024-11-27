# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RGistr(RPackage):
    """Work with 'GitHub' 'Gists'.

    Work with 'GitHub' 'gists' from 'R' (e.g.,
    <https://en.wikipedia.org/wiki/GitHub#Gist>,
    <https://docs.github.com/en/github/writing-on-github/creating-gists/>). A
    'gist' is simply one or more files with code/text/images/etc. This package
    allows the user to create new 'gists', update 'gists' with new files,
    rename files, delete files, get and delete 'gists', star and 'un-star'
    'gists', fork 'gists', open a 'gist' in your default browser, get embed
    code for a 'gist', list 'gist' 'commits', and get rate limit information
    when 'authenticated'. Some requests require authentication and some do not.
    'Gists' website:  <https://gist.github.com/>."""

    cran = "gistr"

    license("MIT")

    version("0.9.0", sha256="170ae025151ee688e7d31b9e49112086a8ddf4fef10155e9ee289ad7f28c8929")
    version("0.4.2", sha256="43c00c7f565732125f45f6c067724771ba1b337d6dd3a6e301639fe16e11032e")
    version("0.4.0", sha256="51771a257379a17552d0c88ada72ca6263954bbe896997f8a66cde3bf0b83ce0")
    version("0.3.6", sha256="ab22523b79510ec03be336e1d4600ec8a3a65afe57c5843621a4cf8f966b52e5")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-jsonlite@1.4:", type=("build", "run"))
    depends_on("r-crul", type=("build", "run"), when="@0.9.0:")
    depends_on("r-httr@1.2.0:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-assertthat", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-rmarkdown", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
