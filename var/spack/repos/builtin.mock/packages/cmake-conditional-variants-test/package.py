# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CmakeConditionalVariantsTest(CMakePackage):
    homepage = "https://dev.null"
    version("1.0")
    variant("example", default=True, description="nope", when="@2.0:")
