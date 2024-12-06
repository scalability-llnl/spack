# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RequiresVirtual(Package):
    """Package that requires a virtual dependency and is registered
    as an external.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")

    depends_on("stuff")
