# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class WrongVariantInConflicts(Package):
    """This package has a wrong variant spelled in a conflict."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/b-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    conflicts("+foo", when="@1.0")
