# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXmlrunner(PythonPackage):
    """PyUnit-based test runner with JUnit like XML reporting."""

    homepage = "https://github.com/pycontribs/xmlrunner"
    pypi = "xmlrunner/xmlrunner-1.7.7.tar.gz"

    version("1.7.7", sha256="5a6113d049eca7646111ee657266966e5bbfb0b5ceb2e83ee0772e16d7110f39")

    depends_on("py-setuptools", type="build")
