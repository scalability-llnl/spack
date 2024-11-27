# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jstorm(Package):
    """
    JStorm is an enterprise fast and stable streaming process engine.
    """

    homepage = "https://github.com/alibaba/jstorm"
    url = "https://github.com/alibaba/jstorm/releases/download/2.4.0/jstorm-2.4.0.tgz"

    license("Apache-2.0")

    version("2.4.0", sha256="8a3965cb51ff95395a40e8d9fd83f12b0aad15c2726c74a796d8085cccc9d69f")

    def install(self, spec, prefix):
        install_tree(".", prefix)
