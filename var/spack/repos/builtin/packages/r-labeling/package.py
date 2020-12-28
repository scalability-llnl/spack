# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLabeling(RPackage):
    """Provides a range of axis labeling algorithms."""

    homepage = "https://cloud.r-project.org/package=labeling"
    url      = "https://cloud.r-project.org/src/contrib/labeling_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/labeling"

    version('0.3', sha256='0d8069eb48e91f6f6d6a9148f4e2dc5026cabead15dd15fc343eff9cf33f538f')
