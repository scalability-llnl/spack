# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTypesentry(PythonPackage):
    """Python library for run-time type checking for type-annotated functions."""

    homepage = "https://github.com/h2oai/typesentry"
    git = "https://github.com/h2oai/typesentry.git"

    license("Apache-2.0")

    # See the git history of __version__.py for versioning information
    version("0.2.7", commit="0ca8ed0e62d15ffe430545e7648c9a9b2547b49c")

    depends_on("py-setuptools", type="build")
    depends_on("py-colorama@0.3.0:", type=("build", "run"))
