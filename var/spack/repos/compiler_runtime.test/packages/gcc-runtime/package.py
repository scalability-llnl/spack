# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GccRuntime(Package):
    homepage = "https://example.com"
    has_code = False
    tags = ["runtime"]
    requires("%gcc")
