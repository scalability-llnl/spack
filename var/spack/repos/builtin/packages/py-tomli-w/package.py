# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomliW(PythonPackage):
    """A lil' TOML writer."""

    homepage = "https://github.com/hukkin/tomli-w"
    pypi = "tomli_w/tomli_w-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="f463434305e0336248cac9c2dc8076b707d8a12d019dd349f5c1e382dd1ae1b9")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.2.0:3", type="build")
