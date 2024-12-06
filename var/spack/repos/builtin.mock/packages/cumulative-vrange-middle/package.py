# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class CumulativeVrangeMiddle(Package):
    """Test that creating cumulative version ranges of the
    form X.Y:X works and allows for the selection of all the
    versions >= X.Y with major == X
    """

    homepage = "https://www.example.org"
    url = "https://example.org/files/v3.4/cmake-3.4.3.tar.gz"

    version("1.0", md5="4cb3ff35b2472aae70f542116d616e63")

    depends_on("cumulative-vrange-bottom@2.1:")
