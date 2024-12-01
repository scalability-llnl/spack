# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mysqlpp(AutotoolsPackage):
    """MySQL++ is a C++ wrapper for MySQL and MariaDB C APIs. It is built on
    the same principles as the Standard C++ Library to make dealing with the
    database as easy as dealing with std containers. MySQL++ also provides
    facilities that let you avoid the most repetitive sorts of SQL within your
    own code, providing native C++ interfaces for these common tasks."""

    homepage = "https://tangentsoft.com/mysqlpp/home"
    url = "https://tangentsoft.com/mysqlpp/releases/mysql++-3.2.5.tar.gz"

    version("3.3.0", sha256="449cbc46556cc2cc9f9d6736904169a8df6415f6960528ee658998f96ca0e7cf")
    version("3.2.5", sha256="839cfbf71d50a04057970b8c31f4609901f5d3936eaa86dab3ede4905c4db7a8")

    depends_on("cxx", type="build")  # generated

    depends_on("mysql-client")

    def configure_args(self):
        if "^mariadb-c-client" in self.spec:
            args = [
                "--with-mysql-include={0}".format(
                    self.spec["mysql-client"].prefix.include.mariadb
                ),
                "--with-mysql-lib={0}".format(self.spec["mysql-client"].prefix.lib.mariadb),
            ]
        else:
            args = ["--with-mysql={0}".format(self.spec["mysql-client"].prefix)]
        return args
