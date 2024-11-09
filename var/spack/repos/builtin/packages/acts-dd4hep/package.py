# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ActsDd4hep(CMakePackage):
    """Glue library to connect Acts to DD4hep"""

    homepage = "https://github.com/acts-project/acts-dd4hep"
    url = "https://github.com/acts-project/acts-dd4hep/archive/refs/tags/v1.0.0.tar.gz"

    maintainers("wdconinc")

    version("1.0.1", sha256="e40f34ebc30b3c33a6802c9d94136e65072d8dcee0b7db57a645f08a64ea5334")
    version("1.0.0", sha256="991f996944c88efa837880f919239e50d12c5c9361e220bc9422438dd608308c")

    depends_on("cxx", type="build")  # generated

    depends_on("dd4hep@1.11: +dddetectors")
