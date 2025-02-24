# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DependsOnDevelop(Package):
    homepage = "example.com"
    url = "fake.com"

    version("main", branch="main")
    version("0.0.0", sha256="0123456789abcdef0123456789abcdef")

    depends_on("develop-branch-version@develop")
