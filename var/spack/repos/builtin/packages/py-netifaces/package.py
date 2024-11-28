# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetifaces(PythonPackage):
    """Portable network interface information"""

    homepage = "https://github.com/al45tair/netifaces"
    pypi = "netifaces/netifaces-0.10.5.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("0.11.0", sha256="043a79146eb2907edf439899f262b3dfe41717d34124298ed281139a8b93ca32")
    version("0.10.9", sha256="2dee9ffdd16292878336a58d04a20f0ffe95555465fee7c9bd23b3490ef2abf3")
    version("0.10.5", sha256="59d8ad52dd3116fcb6635e175751b250dc783fb011adba539558bd764e5d628b")

    depends_on("c", type="build")

    depends_on("py-setuptools", type="build")
