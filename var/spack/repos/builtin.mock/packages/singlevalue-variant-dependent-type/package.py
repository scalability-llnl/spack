# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class SinglevalueVariantDependentType(Package):
    """Simple package with one dependency that has a single-valued
    variant with values=str"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/archive-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("singlevalue-variant fum=nope")
