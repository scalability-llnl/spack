# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFracdiff(RPackage):
    """Maximum likelihood estimation of the parameters of a
    fractionally differenced ARIMA(p,d,q) model (Haslett and
    Raftery, Appl.Statistics, 1989)."""

    homepage = "https://cloud.r-project.org/package=fracdiff"
    url      = "https://cloud.r-project.org/src/contrib/fracdiff_1.4-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fracdiff"

    version('1.4-2', sha256='983781cedc2b4e3ba9fa020213957d5133ae9cd6710bc61d6225728e2f6e850e')
