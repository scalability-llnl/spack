# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Openpa(AutotoolsPackage):
    """An open source, highly-portable library that provides atomic primitives
    (and related constructs) for high performance, concurrent software"""

    homepage = "https://github.com/pmodels/openpa"
    url = "https://github.com/pmodels/openpa/releases/download/v1.0.4/openpa-1.0.4.tar.gz"

    license("mpich2")

    version("1.0.5", sha256="4a18c054970970a1baf477504053a49149f962329b70b481c2ec93e157c9093b")
    version("1.0.4", sha256="9e5904b3bbdcb24e8429c12d613422e716a3479f3e0aeefbd9ce546852899e3a")
    version("1.0.3", sha256="b73943f341b0d4475109f8f341a5229258e43510b62cb5d488cf7f0e84fa5557")
    version("1.0.2", sha256="13b5ef8ea3502822ab03861bf9d047c3bda722b22605edf3f508fb355746db4f")
    version("1.0.1", sha256="63fae765d44e5741506b92cd0ff55c237c1e19d20bd5539c77cea1c67d5b4303")
    version("1.0.0", sha256="0f163da7fbe39a438c301b52bb876961bfedfe4ab6248a98297dd326fabee627")

    depends_on("c", type="build")  # generated
