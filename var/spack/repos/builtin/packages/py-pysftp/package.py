# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPysftp(PythonPackage):
    """A simple interface to SFTP."""

    pypi = "pysftp/pysftp-0.2.9.tar.gz"

    version("0.2.9", sha256="fbf55a802e74d663673400acd92d5373c1c7ee94d765b428d9f977567ac4854a")

    depends_on("py-paramiko@1.17:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
