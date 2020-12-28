# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RModeltools(RPackage):
    """A collection of tools to deal with statistical models."""

    homepage = "https://cloud.r-project.org/package=modeltools"
    url      = "https://cloud.r-project.org/src/contrib/modeltools_0.2-21.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/modeltools"

    version('0.2-22', sha256='256a088fc80b0d9182f984f9bd3d6207fb7c1e743f72e2ecb480e6c1d4ac34e9')
    version('0.2-21', sha256='07b331475625674ab00e6ddfc479cbdbf0b22d5d237e8c25d83ddf3e0ad1cd7a')
