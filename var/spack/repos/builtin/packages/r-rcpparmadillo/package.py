# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpparmadillo(RPackage):
    """'Rcpp' Integration for the 'Armadillo' Templated Linear Algebra Library.

    'Armadillo' is a templated C++ linear algebra library (by Conrad;
    Sanderson) that aims towards a good balance between speed and ease of; use.
    Integer, floating point and complex numbers are supported, as; well as a
    subset of trigonometric and statistics functions. Various; matrix
    decompositions are provided through optional integration with; LAPACK and
    ATLAS libraries.  The 'RcppArmadillo' package includes the; header files
    from the templated 'Armadillo' library. Thus users do; not need to install
    'Armadillo' itself in order to use; 'RcppArmadillo'. From release 7.800.0
    on, 'Armadillo' is licensed; under Apache License 2; previous releases were
    under licensed as MPL; 2.0 from version 3.800.0 onwards and LGPL-3 prior to
    that"""

    cran = "RcppArmadillo"

    version("14.0.0-1", sha256="80c4d4fadc3ed92712affc50279de4c5f2e1f7ee777ad1f1b3f9f3e94a64ba90")
    version(
        "0.12.4.0.0", sha256="f6db54c465abc0a570a0da6f737d9fdf2187287fb235ce487b1903b5177482cb"
    )
    version(
        "0.12.2.0.0", sha256="8f9ce8413f12582fa5f04e33d7ba85dae7bd22c4567e87e146fffa349e2d78b7"
    )
    version(
        "0.11.4.0.1", sha256="0ce4ddf5f3ca23e729437084240b352118cf2275525082239c2bd9cda86a37e3"
    )
    version(
        "0.11.1.1.0", sha256="eb0bfc484c41543e766441b4c8c4a3061d8633540914ed2bbf363da047a74897"
    )
    version(
        "0.10.8.1.0", sha256="efa415afb38514648456d1feab247c556735573673986a4fb0f512960b9af5f4"
    )
    version(
        "0.10.7.5.0", sha256="7c061e6371c3c068d17744fd7f764dfd02f25393c3f5d534aa7d9e62ac912614"
    )
    version(
        "0.10.7.3.0", sha256="3710b767708e3b9408723eedb98391daa8651fda53a2c6b033273265512f6262"
    )
    version(
        "0.10.1.2.2", sha256="38323703fcf2b61f46f2984aafdd3ddf17c3c993d1d27a8f0f4ba5012b99d069"
    )
    version(
        "0.9.600.4.0", sha256="2057b7aa965a4c821dd734276d8e6a01cd59a1b52536b65cb815fa7e8c114f1e"
    )
    version(
        "0.9.400.3.0", sha256="56936d501fe8e6f8796ae1a6badb9294d7dad98a0b557c3b3ce6bd4ecaad13b0"
    )
    version(
        "0.8.100.1.0", sha256="97ca929b34d84d99d7cadc3612b544632cdd0c43ed962933a3d47caa27854fa7"
    )

    depends_on("r@3.3.0:", type=("build", "run"), when="@0.8.500.0:")
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-rcpp@1.0.8:", type=("build", "run"), when="@0.12.8.4.0:")
