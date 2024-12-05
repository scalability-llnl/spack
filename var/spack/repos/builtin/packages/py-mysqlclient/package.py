# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMysqlclient(PythonPackage):
    """Python interface to MySQL"""

    # Note: _mysql module can be imported via "from MySQLdb import _mysql"
    # The documentation is misleading about this.

    homepage = "https://github.com/PyMySQL/mysqlclient-python"
    pypi = "mysqlclient/mysqlclient-1.4.4.tar.gz"

    license("GPL-2.0-or-later")

    version("2.2.4", sha256="33bc9fb3464e7d7c10b1eaf7336c5ff8f2a3d3b88bab432116ad2490beb3bf41")
    version("1.4.6", sha256="f3fdaa9a38752a3b214a6fe79d7cae3653731a53e577821f9187e67cbecb2e16")
    version("1.4.5", sha256="e80109b0ae8d952b900b31b623181532e5e89376d707dcbeb63f99e69cefe559")
    version("1.4.4", sha256="9c737cc55a5dc8dd3583a942d5a9b21be58d16f00f5fefca4e575e7d9682e98c")
    version("1.3.13", sha256="ff8ee1be84215e6c30a746b728c41eb0701a46ca76e343af445b35ce6250644f")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("mysql")

    # Fix "library not found for -lzlib" as described in
    # https://github.com/PyMySQL/mysqlclient/issues/584 by backporting the
    # patch from @2.2.0rc1 that uses pkg-config instead of mysql_config
    # https://github.com/PyMySQL/mysqlclient/pull/586/files
    patch("use-pkg-config.patch", when="@1.4:2.1")
