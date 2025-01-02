# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PkgA(Package):
    homepage = "http://www.example.com"
    has_code = False

    version("1.0")
    depends_on("pkg-b")
