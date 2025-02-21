# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatialreg(RPackage):
    """Spatial Regression Analysis.

    A collection of all the estimation functions for spatial cross-sectional
    models (on lattice/areal data using spatial weights matrices) contained up
    to now in 'spdep', 'sphet' and 'spse'. These model fitting functions
    include maximum likelihood methods for cross-sectional models proposed by
    'Cliff' and 'Ord' (1973, ISBN:0850860369) and (1981, ISBN:0850860814),
    fitting methods initially described by 'Ord' (1975)
    <doi:10.1080/01621459.1975.10480272>. The models are further described by
    'Anselin' (1988) <doi:10.1007/978-94-015-7799-1>. Spatial two stage least
    squares and spatial general method of moment models initially proposed by
    'Kelejian' and 'Prucha' (1998) <doi:10.1023/A:1007707430416> and (1999)
    <doi:10.1111/1468-2354.00027> are provided. Impact methods and MCMC fitting
    methods proposed by 'LeSage' and 'Pace' (2009) <doi:10.1201/9781420064254>
    are implemented for the family of cross-sectional spatial regression
    models. Methods for fitting the log determinant term in maximum likelihood
    and MCMC fitting are compared by 'Bivand et al.' (2013)
    <doi:10.1111/gean.12008>, and model fitting methods by 'Bivand' and 'Piras'
    (2015) <doi:10.18637/jss.v063.i18>; both of these articles include
    extensive lists of references. 'spatialreg' >= 1.1-* correspond to 'spdep'
    >= 1.1-1, in which the model fitting functions are deprecated and pass
    through to 'spatialreg', but will mask those in 'spatialreg'. From versions
    1.2-*, the functions will be made defunct in 'spdep'."""

    cran = "spatialreg"

    license("GPL-2.0-only")

    version("1.3-5", sha256="eefeaa2f22d3652a23c30c8ff81364f419634e466cdb0c2d9c7bcef9287b00c4")
    version("1.2-8", sha256="150cb77ca09800d93af7de37440072d59ac7e41acb45ab42fc1c0e59edd7f9de")
    version("1.2-6", sha256="9b384117a31ab5fe830325b3eacbec5eb9d40bf0e9ca3c75ea15ca6b78fbd41d")
    version("1.2-3", sha256="09e0e65f043975d5c1d4be99ef9f29cf0790e962dcde9b7e45a7027d268fce22")
    version("1.2-1", sha256="4c40b6b331aa8818254633cfb80d4b9a03b2b6fac2c0104b3b99201d447ba081")
    version("1.1-5", sha256="ddbf0773bad2e99b306116ae99a57bf29eecf723d1735820935a6fb7f331b27d")
    version("1.1-3", sha256="7609cdfcdfe427d2643a0db6b5360be3f6d60ede8229436ab52092d1c9cf0480")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-spdata", type=("build", "run"))
    depends_on("r-spdata@2.3.1:", type=("build", "run"), when="@1.3-4:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"), when="@1.2-1:")
    depends_on("r-spdep", type=("build", "run"))
    depends_on("r-spdep@1.3-1:", type=("build", "run"), when="@1.3-1:")
    depends_on("r-expm", type=("build", "run"), when="@:1.2-10")
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-multcomp", type=("build", "run"), when="@1.2-9:")
    depends_on("r-boot", type=("build", "run"))
    depends_on("r-learnbayes", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-gmodels", type=("build", "run"), when="@:1.2-3")
