# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RFracdiff(RPackage):
    """Fractionally Differenced ARIMA aka ARFIMA(P,d,q) Models

    Maximum likelihood estimation of the parameters of a fractionally
    differenced ARIMA(p,d,q) model (Haslett and Raftery, Appl.Statistics,
    1989); including inference and basic methods.  Some alternative algorithms
    to estimate "H"."""

    homepage = "https://cloud.r-project.org/package=fracdiff"
    url      = "https://cloud.r-project.org/src/contrib/fracdiff_1.4-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fracdiff"

    version('1.5-1', sha256='b8103b32a4ca3a59dda1624c07da08ecd144c7a91a747d1f4663e99421950eb6')
    version('1.4-2', sha256='983781cedc2b4e3ba9fa020213957d5133ae9cd6710bc61d6225728e2f6e850e')
