# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gmtsar(CMakePackage):
    """GMTSAR is an open source (GNU General Public License) InSAR processing
    system designed for users familiar with Generic Mapping Tools (GMT).
    """

    homepage = "https://topex.ucsd.edu/gmtsar/"
    url = "https://elenacreinisch.com/gmtsar/GMTSAR-5.6.tar.gz"

    version("5.6", sha256="0f7326f46aedf1e8e4dc80dd03f1ae8681f52a8253dc4a00a943aec14562994b")

    depends_on("c", type="build")  # generated

    depends_on("gmt")
