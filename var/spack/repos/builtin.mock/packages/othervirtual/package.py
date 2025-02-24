# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Othervirtual(Package):
    homepage = "http://somewhere.com"
    url = "http://somewhere.com/stuff-1.0.tar.gz"

    version("1.0", md5="67890abcdef1234567890abcdef12345")

    provides("stuff")
