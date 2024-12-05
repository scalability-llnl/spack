# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGoogle(PythonPackage):
    """Python bindings to the Google search engine."""

    homepage = "https://breakingcode.wordpress.com/"
    pypi = "google/google-3.0.0.tar.gz"

    version("3.0.0", sha256="143530122ee5130509ad5e989f0512f7cb218b2d4eddbafbad40fd10e8d8ccbe")

    depends_on("py-setuptools", type="build")
    depends_on("py-beautifulsoup4", type=("build", "run"))
