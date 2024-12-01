# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AuditUserspace(AutotoolsPackage):
    """Linux audit userspace"""

    homepage = "https://github.com/linux-audit/audit-userspace"
    url = "https://github.com/linux-audit/audit-userspace/archive/v2.8.5.tar.gz"

    license("LGPL-2.1-or-later")

    version("4.0.1", sha256="f964610dc0c1e68075d5ae4b14d6280d1164b6eca3a4a13721d1a711681403d9")
    version("3.1.2", sha256="4516dbfd1bea0eea10a30f907e50f17087673a536ec6322a2a568dff4ebe50f4")
    version("3.1.1", sha256="6a97cc472920639d736e9927353be05e323f351067fcf6e5d34439cafa0e9006")
    version("2.8.5", sha256="835ffdd65056ba0c26509dbf48882713b00dbe70e1d8cf25d538501136c2e3e9")
    version("2.8.4", sha256="089dfdceb38edf056202a6de4892fd0c9aaa964c08bd7806c5d0c7c33f09e18d")
    version("2.8.3", sha256="c239e3813b84bc264aaf2f796c131c1fe02960244f789ec2bd8d88aad4561b29")
    version("2.8.2", sha256="0a312a8487190d97715d46abb30aa2abd464b55f21d5c2d24428baa320ee4ce2")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("openldap")
    depends_on("swig")

    patch(
        "https://github.com/linux-audit/audit-userspace/commit/28a74a445d54932e1450b60d6148912344615b44.patch?full_index=1",
        sha256="63d4644c7037be21bcafa913f4c96fbaa37f388c170cf0344869a0dc2449fd65",
        when="@4.0.1",
    )
