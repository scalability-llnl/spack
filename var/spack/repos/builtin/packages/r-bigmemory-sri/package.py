# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBigmemorySri(RPackage):
    """This package provides a shared resource interface
       for the bigmemory and synchronicity packages."""

    homepage = "https://cloud.r-project.org/web/packages/bigmemory.sri/index.html"
    url      = "https://cloud.r-project.org/src/contrib/bigmemory.sri_0.1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bigmemory.sri"

    version('0.1.3', sha256='55403252d8bae9627476d1f553236ea5dc7aa6e54da6980526a6cdc66924e155')
