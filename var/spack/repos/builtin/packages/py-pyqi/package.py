# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqi(PythonPackage):
    """pyqi (canonically pronounced pie chee) is a Python framework designed
    to support wrapping general commands in multiple types of interfaces,
    including at the command line, HTML, and API levels."""

    homepage = "https://pyqi.readthedocs.io"
    pypi = "pyqi/pyqi-0.3.2.tar.gz"

    version("0.3.2", sha256="8f1711835779704e085e62194833fed9ac2985e398b4ceac6faf6c7f40f5d15f")

    depends_on("py-setuptools", type="build")
