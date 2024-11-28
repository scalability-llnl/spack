# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetproctitle(PythonPackage):
    """The setproctitle module allows a process to change its title (as
    displayed by system tools such as ps and top)."""

    homepage = "https://github.com/dvarrazzo/py-setproctitle"
    pypi = "setproctitle/setproctitle-1.1.10.tar.gz"

    license("BSD-3-Clause")

    version("1.1.10", sha256="6283b7a58477dd8478fbb9e76defb37968ee4ba47b05ec1c053cb39638bd7398")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
