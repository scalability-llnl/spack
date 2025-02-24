# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPromises(RPackage):
    """Abstractions for Promise-Based Asynchronous Programming.

    Provides fundamental abstractions for doing asynchronous programming in R
    using promises. Asynchronous programming is useful for allowing a single R
    process to orchestrate multiple tasks in the background while also
    attending to something else. Semantics are similar to 'JavaScript'
    promises, but with a syntax that is idiomatic R."""

    cran = "promises"

    license("MIT")

    version("1.3.0", sha256="f8209df3bab33340c1bc8c0d26caee2890fafb93129ff1423302abae5931fad3")
    version("1.2.0.1", sha256="8d3a8217909e91f4c2a2eebba5ac8fc902a9ac1a9e9d8a30815c9dc0f162c4b7")
    version("1.1.1", sha256="3718c6eb2c3362cbe89389e613118f783f9977dbf24757f85026e661199c5800")
    version("1.0.1", sha256="c2dbc7734adf009377a41e570dfe0d82afb91335c9d0ca1ef464b9bdcca65558")

    depends_on("r-r6", type=("build", "run"))
    depends_on("r-fastmap@1.1.0:", type=("build", "run"), when="@1.2.1:")
    depends_on("r-later", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-magrittr@1.5:", type=("build", "run"), when="@1.2.1:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
