# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JansiNative(MavenPackage):
    """Jansi is a small ASl 2.0 licensed Java library that allows you to
    use ANSI escape sequences to format your console output which works even
    on windows."""

    homepage = "https://fusesource.github.io/jansi/"
    url = "https://github.com/fusesource/jansi-native/archive/jansi-native-1.8.tar.gz"

    license("Apache-2.0")

    version("1.8", sha256="053808f58495a5657c7e7f388008b02065fbbb3f231454bfcfa159adc2e2fcea")

    depends_on("c", type="build")  # generated

    depends_on("java@8", type=("build", "run"))
