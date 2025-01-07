# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PkgB(Package):
    homepage = "http://www.example.com"
    has_code = False

    version("1.0")
