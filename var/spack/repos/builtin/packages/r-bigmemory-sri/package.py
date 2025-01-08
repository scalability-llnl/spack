# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBigmemorySri(RPackage):
    """A shared resource interface for Bigmemory Project packages.

    This package provides a shared resource interface for the bigmemory and
    synchronicity packages."""

    cran = "bigmemory.sri"

    version("0.1.8", sha256="029a4ed24aa17636a20b83857d55fe6a9283acb8b647cbc75280dea8ec987771")
    version("0.1.6", sha256="3bfa6ac966ce0ea93283f5856a853d0ee5ff85aedd7a7d1ca8a93d0aa642860c")
    version("0.1.3", sha256="55403252d8bae9627476d1f553236ea5dc7aa6e54da6980526a6cdc66924e155")
