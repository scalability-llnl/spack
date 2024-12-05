# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHypercorn(PythonPackage):
    """A ASGI Server based on Hyper libraries and inspired by
    Gunicorn."""

    homepage = "https://gitlab.com/pgjones/hypercorn/"
    pypi = "Hypercorn/Hypercorn-0.13.2.tar.gz"

    license("MIT")

    version("0.13.2", sha256="6307be5cbdf6ba411967d4661202dc4f79bd511b5d318bc4eed88b09418427f8")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-h11", type=("build", "run"))
    depends_on("py-h2@3.1.0:", type=("build", "run"))
    depends_on("py-priority", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-wsproto@0.14.0:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"), when="^python@:3.7")
