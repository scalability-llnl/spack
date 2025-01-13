# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ParentFooBar(Package):
    """This package has a variant "bar", which is True by default, and depends on another
    package which has the same variant defaulting to False.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/parent-foo-bar-1.0.tar.gz"

    version("1.0", md5="abcdefg0123456789abcdefghfedcba0")

    variant("foo", default=True, description="")
    variant("bar", default=True, description="")

    depends_on("direct-dep-foo-bar")
    depends_on("dependency-foo-bar")
