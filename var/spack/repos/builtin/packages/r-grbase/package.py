# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGrbase(RPackage):
    """A Package for Graphical Modelling in R.

    The 'gRbase' package provides graphical modelling features used by e.g. the
    packages 'gRain', 'gRim' and 'gRc'. 'gRbase' implements graph algorithms
    including (i) maximum cardinality search (for marked and unmarked graphs).
    (ii) moralization, (iii) triangulation, (iv) creation of junction tree.
    'gRbase' facilitates array operations, 'gRbase' implements functions for
    testing for conditional independence. 'gRbase' illustrates how hierarchical
    log-linear models may be implemented and describes concept of graphical
    meta data.  The facilities of the package are documented in the book by
    Hojsgaard, Edwards and Lauritzen (2012, <doi:10.1007/978-1-4614-2299-0>)
    and in the paper by  Dethlefsen and Hojsgaard, (2005,
    <doi:10.18637/jss.v014.i17>).  Please see 'citation("gRbase")' for citation
    details.  NOTICE  'gRbase' requires that the packages graph, 'Rgraphviz'
    and 'RBGL' are installed from 'bioconductor'; for installation instructions
    please refer to the web page given below."""

    cran = "gRbase"

    version("2.0.2", sha256="36720e49b82e360166386c9b3bf17838aeb6d9b921e7e01d48f8a115f9a02e97")
    version("1.8.9", sha256="dacab442d896e4593c6196e8446b75c4144a1c4ebc3f039dc624516038193d7e")
    version("1.8.8", sha256="fdd5d1ca8adb74e8bd2b210c9a652a10e60a90b40450cd8a295b06af41acf9db")
    version("1.8.7", sha256="01d77e1b029ac22b4e13f07384285f363733a42aba842eddfc5e1aceea99f808")
    version("1.8-6.7", sha256="aaafc7e1b521de60e1a57c0175ac64d4283850c3273bd14774cf24dabc743388")
    version("1.8-3.4", sha256="d35f94c2fb7cbd4ce3991570424dfe6723a849658da32e13df29f53b6ea2cc2c")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.8-6.7:")
    depends_on("r@4.2.0:", type=("build", "run"), when="@2.0.2:")
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"), when="@:2.0.1")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcpp@0.11.1:", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))

    depends_on("r-biocmanager", type=("build", "run"), when="@1.8.7:1.9")
    depends_on("r-graph", type=("build", "run"), when="@:1.9")
    depends_on("r-rbgl", type=("build", "run"), when="@:1.9")
    depends_on("r-rgraphviz", type=("build", "run"), when="@1.8-6.7:1.9")
