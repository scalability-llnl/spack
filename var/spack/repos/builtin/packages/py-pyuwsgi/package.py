# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyuwsgi(PythonPackage):
    """The uWSGI server"""

    homepage = "https://uwsgi-docs.readthedocs.io"
    pypi = "pyuwsgi/pyuwsgi-2.0.21.tar.gz"

    license("GPL-2.0-or-later")

    version("2.0.21", sha256="211e8877f5191e347ba905232d04ab30e05ce31ba7a6dac4bfcb48de9845bb52")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
