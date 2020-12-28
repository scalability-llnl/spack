# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMapproj(RPackage):
    """Converts latitude/longitude into projected coordinates."""

    homepage = "https://cloud.r-project.org/package=mapproj"
    url      = "https://cloud.r-project.org/src/contrib/mapproj_1.2-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mapproj"

    version('1.2.6', sha256='62a5aa97837ae95ef9f973d95fe45fe43dbbf482dfa922e9df60f3c510e7efe5')
    version('1.2-5', sha256='f3026a3a69a550c923b44c18b1ccc60d98e52670a438250d13f3c74cf2195f66')
    version('1.2-4', sha256='cf8a1535f57e7cca0a71b3a551e77ad3e7a78f61a94bb19effd3de19dbe7dceb')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-maps@2.3:', type=('build', 'run'))
