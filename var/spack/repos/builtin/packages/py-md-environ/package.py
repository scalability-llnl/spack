# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdEnviron(PythonPackage):
    """This is an extension to Python-Markdown which allows environment variables
    to be used in the text."""

    pypi = "md-environ/md-environ-0.1.0.tar.gz"

    maintainers("wscullin")

    version("0.1.0", sha256="fe3c2a255af523d6f522831c699336cd71f9d543714067d93206ed35836f1793")

    depends_on("py-setuptools", type="build")

    depends_on("py-markdown", type=("build", "run"))
