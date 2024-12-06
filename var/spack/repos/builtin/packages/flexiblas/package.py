# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flexiblas(CMakePackage):
    """A BLAS and LAPACK wrapper library with runtime exchangable backends"""

    homepage = "https://www.mpi-magdeburg.mpg.de/projects/flexiblas"
    url = "https://csc.mpi-magdeburg.mpg.de/mpcsc/software/flexiblas/flexiblas-3.0.3.tar.gz"

    license("GPL-3.0-or-later")

    version("3.4.2", sha256="be4bc95461ab4970aba39a0a2bbd0d03bcf802180f63be8eefc189eb2380227c")
    version("3.3.0", sha256="2696cd63d69b9a007f40f1f4a1ed83ad2fc46f6a930a22753bd221758c503ea2")
    version("3.2.1", sha256="5be7e508e2dbb751b3bf372639d8e82a11f79e9ef6cbf243b64981c24a5703cf")
    version("3.2.0", sha256="a3f4d66a30b6fa6473e492de86d34abc5f9d4e69d4d91ba23618388e8df05904")
    version("3.1.3", sha256="aac6175660e8475ce478b88673eee330671f8aecc0cb852a25833e23e29a0620")
    version("3.0.4", sha256="50a88f2e88994dda91b2a2621850afd9654b3b84820e737e335687a46751be5c")
    version("3.0.3", sha256="926ab31cf56f0618aec34da85314f3b48b6deb661b4e9d6e6a99dc37872b5341")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # virtual dependency
    provides("blas")
    provides("lapack")

    def cmake_args(self):
        return [self.define("SYSCONFDIR", self.prefix.etc)]
