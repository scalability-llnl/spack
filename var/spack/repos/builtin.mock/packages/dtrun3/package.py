# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dtrun3(Package):
    """Simple package which acts as a run dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtrun3-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("dtbuild3", type="build")
