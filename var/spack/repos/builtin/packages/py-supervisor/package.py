# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySupervisor(PythonPackage):
    """A system for controlling process state under UNIX"""

    homepage = "http://supervisord.org"
    pypi = "supervisor/supervisor-4.2.4.tar.gz"

    version("4.2.4", sha256="40dc582ce1eec631c3df79420b187a6da276bbd68a4ec0a8f1f123ea616b97a2")

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
