# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStorm(PythonPackage):
    """Storm is an object-relational mapper (ORM) for Python"""

    homepage = "https://storm.canonical.com/"
    pypi = "storm/storm-0.25.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.25", sha256="ec7cc8897638f94f6b75c6a2af74aa9b31f5492d7a2f9482c08a8dd7b46adb14")
    version(
        "0.23",
        sha256="01c59f1c898fb9891333abd65519ba2dd5f68623ac8e67b54932e99ce52593d3",
        url="https://files.pythonhosted.org/packages/source/s/storm/storm-0.23.tar.bz2",
    )

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-zope-interface@4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
