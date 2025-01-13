# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SecondDependencyFooBarFee(Package):
    """This package has a variant "foo", which is True by default, a variant "bar" which
    is False by default, and variant "foo" which is True by default.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/second-dependency-foo-bar-fee-1.0.tar.gz"

    version("1.0", md5="2101234567890abcdefg1234567890abc")

    variant("foo", default=True, description="")
    variant("bar", default=False, description="")
    variant("fee", default=False, description="")
