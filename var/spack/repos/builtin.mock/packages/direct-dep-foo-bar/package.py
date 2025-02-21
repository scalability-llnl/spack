# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DirectDepFooBar(Package):
    """This package has a variant "bar", which is False by default, and
    variant "foo" which is True by default.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/direct-dep-foo-bar-1.0.tar.gz"

    version("1.0", md5="567890abcdefg12345678900987654321")

    variant("foo", default=True, description="")
    variant("bar", default=False, description="")

    depends_on("second-dependency-foo-bar-fee")
