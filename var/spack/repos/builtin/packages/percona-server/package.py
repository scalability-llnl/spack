# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class PerconaServer(CMakePackage):
    """Percona Server is a branch of MySQL 8.0 bringing higher performance,
    reliability and more features."""

    homepage = "https://www.percona.com"
    url = "https://github.com/percona/percona-server/archive/Percona-Server-5.7.31-34.tar.gz"

    license("Unicode-TOU")

    version("8.0.20-11", sha256="454ba8b64d447f477a70888903949ce6f64c57d3e15e9054d17d156c88693670")
    version("8.0.19-10", sha256="f2f979bd7dfb4d62aef79b7c488070d5d599341a6acbb295400f1d68257cbd80")
    version("8.0.18-9", sha256="e79a8c1ae5f2271c0b344494a299a9bbbada88d3bce87449b7de274d17d1ccd0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.70.0")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("openssl")
    depends_on("ncurses")
    depends_on("readline")
    # Links to libldap_r, which was merged with libldap in OpenLDAP 2.5
    depends_on("openldap@:2.4")
    depends_on("libtirpc")
    depends_on("curl")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("rpcsvc-proto")
