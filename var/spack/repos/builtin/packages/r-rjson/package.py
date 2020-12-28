# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRjson(RPackage):
    """Converts R object into JSON objects and vice-versa."""

    homepage = "https://cloud.r-project.org/package=rjson"
    url      = "https://cloud.r-project.org/src/contrib/rjson_0.2.15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rjson"

    version('0.2.20', sha256='3a287c1e5ee7c333ed8385913c0a307daf99335fbdf803e9dcca6e3d5adb3f6c')
    version('0.2.19', sha256='5c2672461986f2b715416cab92ed262abe9875f31299bc8a1a072ef7c6dd49bc')
    version('0.2.15', sha256='77d00d8f6a1c936329b46f3b8b0be79a165f8c5f1989497f942ecc53dcf6f2ef')

    depends_on('r@3.1.0:', type=('build', 'run'))
