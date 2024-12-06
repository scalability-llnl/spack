# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VersionTestDependencyPreferred(AutotoolsPackage):
    """Dependency of version-test-pkg, which has a multi-valued
    variant with two default values (a very low priority optimization
    criterion for clingo is to maximize their number)
    """

    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/xz-1.0.tar.gz"

    version("5.2.5", sha256="5117f930900b341493827d63aa910ff5e011e0b994197c3b71c08a20228a42df")

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
