# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDownloader(RPackage):
    """Download Files over HTTP and HTTPS.

    Provides a wrapper for the download.file function, making it possible to
    download files over HTTPS on Windows, Mac OS X, and other Unix-like
    platforms. The 'RCurl' package provides this functionality (and much more)
    but can be difficult to install because it must be compiled with external
    dependencies. This package has no external dependencies, so it is much
    easier to install."""

    cran = "downloader"

    license("GPL-2.0-only")

    version("0.4", sha256="1890e75b028775154023f2135cafb3e3eed0fe908138ab4f7eff1fc1b47dafab")

    depends_on("r-digest", type=("build", "run"))
