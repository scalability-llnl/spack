# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PythonVenv(Package):
    """A Spack managed Python virtual environment"""

    homepage = "https://docs.python.org/3/library/venv.html"
    has_code = False

    version("1.0")

    extends("python")

    def install(self, spec, prefix):
        pass
