# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUwsgi(PythonPackage):
    """Web Application framework for low overhead web services"""

    homepage = "https://github.com/unbit/uwsgi/"
    pypi = "uwsgi/uwsgi-2.0.18.tar.gz"

    license("GPL-2.0-only")

    version("2.0.27", sha256="3ee5bfb7e6e9c93478c22aa8183eef35b95a2d5b14cca16172e67f135565c458")
    version("2.0.18", sha256="4972ac538800fb2d421027f49b4a1869b66048839507ccf0aa2fda792d99f583")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("python", type=("build", "link", "run"))
