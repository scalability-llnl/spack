# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Mvdefaults(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/mvdefaults-1.0.tar.gz"

    version("1.0", md5="abcdef1234567890abcdef1234567890")

    variant("foo", values=("a", "b", "c"), default=("a", "b", "c"), multi=True, description="")
