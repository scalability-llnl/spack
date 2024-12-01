# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReindent(PythonPackage):
    """Change Python (.py) files to use 4-space indents and no hard tab
    characters. Also trim excess spaces and tabs from ends of lines, and remove
    empty lines at the end of files. Also ensure the last line ends with a
    newline."""

    pypi = "reindent/reindent-3.5.1.tar.gz"

    version("3.5.1", sha256="59aeb8fbc16e45686f65df23b91896a17eb14ace7a7546860f50d2bb5ec4c9c0")

    depends_on("py-setuptools", type="build")
