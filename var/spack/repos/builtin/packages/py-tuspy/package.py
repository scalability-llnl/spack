# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTuspy(PythonPackage):
    """A Python client for the tus resumable upload protocol -> http://tus.io"""

    homepage = "https://github.com/tus/tus-py-client/"
    pypi = "tuspy/tuspy-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="09a81eba7b0ce4da7870961721892c62f1d62570913bcef6727ef5599e3f4181")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-future@0.16.0:", type=("build", "run"))
    depends_on("py-requests@2.18.4:", type=("build", "run"))
    depends_on("py-six@1.11.0:", type=("build", "run"))
    depends_on("py-tinydb@3.5.0:", type=("build", "run"))
    depends_on("py-aiohttp@3.6.2:", type=("build", "run"))
