# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGower(RPackage):
    """Gower's Distance

    Compute Gower's distance (or similarity) coefficient between records.
    Compute the top-n matches between records. Core algorithms are executed in
    parallel on systems supporting OpenMP."""

    homepage = "https://github.com/markvanderloo/gower"
    url      = "https://cloud.r-project.org/src/contrib/gower_0.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gower"

    version('0.2.2', sha256='3f022010199fafe34f6e7431730642a76893e6b4249b84e5a61012cb83483631')
    version('0.2.1', sha256='af3fbe91cf818c0841b2c0ec4ddf282c182a588031228c8d88f7291b2cdff100')
