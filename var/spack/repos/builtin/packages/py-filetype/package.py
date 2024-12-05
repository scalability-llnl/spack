# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFiletype(PythonPackage):
    """Small and dependency free Python package to infer file type and MIME
    type checking the magic numbers signature of a file or buffer.
    """

    homepage = "https://github.com/h2non/filetype.py"
    pypi = "filetype/filetype-1.2.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="66b56cd6474bf41d8c54660347d37afcc3f7d1970648de365c102ef77548aadb")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
