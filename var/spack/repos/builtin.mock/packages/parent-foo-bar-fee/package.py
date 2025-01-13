# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ParentFooBarFee(Package):
    """This package has a variant "bar", which is True by default, and depends on another
    package which has the same variant defaulting to False.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/parent-foo-bar-fee-1.0.tar.gz"

    version("1.0", md5="abcdefg01234567890123abcdefghfed")

    variant("foo", default=True, description="")
    variant("bar", default=True, description="")
    variant("fee", default=False, description="")

    depends_on("dependency-foo-bar")
