# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVgam(RPackage):
    """Vector Generalized Linear and Additive Models.

    An implementation of about 6 major classes of statistical regression
    models. The central algorithm is Fisher scoring and iterative reweighted
    least squares. At the heart of this package are the vector generalized
    linear and additive model (VGLM/VGAM) classes. VGLMs can be loosely thought
    of as multivariate GLMs. VGAMs are data-driven VGLMs that use smoothing.
    The book "Vector Generalized Linear and Additive Models: With an
    Implementation in R" (Yee, 2015) <DOI:10.1007/978-1-4939-2818-7> gives
    details of the statistical framework and the package. Currently only
    fixed-effects models are implemented. Many (150+) models and distributions
    are estimated by maximum likelihood estimation (MLE) or penalized MLE. The
    other classes are RR-VGLMs (reduced-rank VGLMs), quadratic RR-VGLMs,
    reduced-rank VGAMs, RCIMs (row-column interaction models)---these classes
    perform constrained and unconstrained quadratic ordination (CQO/UQO) models
    in ecology, as well as constrained additive ordination (CAO). Hauck-Donner
    effect detection is implemented. Note that these functions are subject to
    change; see the NEWS and ChangeLog files for latest changes."""

    cran = "VGAM"

    version("1.1-11", sha256="de9d909bd2bcfccf55d24f96999e0780ca45ec29030e227a722eb24e378b33a5")
    version("1.1-8", sha256="d4c0f1d4e356d88ab6f39c05076ff97ebef6d20b7fbf1b0fa31d40c73d0ad1cc")
    version("1.1-7", sha256="a4c52d392332477eac557c84b732f3c03dd48f75db3884e23c71cf99d991757e")
    version("1.1-6", sha256="446a61bac5dd4794e05d20c2f3901eec54afac52c6e23ce2787c5575170dd417")
    version("1.1-5", sha256="30190b150f3e5478137d288a45f575b2654ad7c29254b0a1fe5c954ee010a1bb")
    version("1.1-1", sha256="de192bd65a7e8818728008de8e60e6dd3b61a13616c887a43e0ccc8147c7da52")
    version("1.0-6", sha256="121820a167411e847b41bdcb0028b55842d0ccc0c3471755c67449837e0fe3b9")
    version("1.0-4", sha256="e581985f78ef8b866d0e810b2727061bb9c9bc177b2c9090aebb3a35ae87a964")
    version("1.0-3", sha256="23bb6690ae15e9ede3198ef55d5d3236c279aa8fa6bd4f7350242379d9d72673")
    version("1.0-2", sha256="03561bf484f97b616b1979132c759c5faa69c5d5a4cfd7aea2ea6d3612ac0961")
    version("1.0-1", sha256="c066864e406fcee23f383a28299dba3cf83356e5b68df16324885afac87a05ea")
    version("1.0-0", sha256="6acdd7db49c0987c565870afe593160ceba72a6ca4a84e6da3cf6f74d1fa02e1")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"), when="@1.0-2:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0-4:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.1-5:")
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.1-8:")
