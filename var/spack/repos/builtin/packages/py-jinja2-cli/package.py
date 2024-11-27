# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJinja2Cli(PythonPackage):
    """A CLI interface to Jinja2"""

    homepage = "https://github.com/mattrobenolt/jinja2-cli"
    pypi = "jinja2-cli/jinja2-cli-0.6.0.tar.gz"

    license("BSD-2-Clause")

    version("0.8.2", sha256="a16bb1454111128e206f568c95938cdef5b5a139929378f72bb8cf6179e18e50")
    version("0.6.0", sha256="4b1be17ce8a8f133df02205c3f0d3ebfc3a68e795d26987f846a2316636427b7")

    depends_on("py-setuptools", type="build")

    depends_on("py-jinja2", type=("build", "run"))
