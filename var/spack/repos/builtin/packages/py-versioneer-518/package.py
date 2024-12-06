# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVersioneer518(PythonPackage):
    """Versioneer is a tool to automatically update version strings by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/python-versioneer/versioneer-518"
    pypi = "versioneer-518/versioneer-518-0.19.tar.gz"
    git = "https://github.com/python-versioneer/versioneer-518.git"

    # A workaround for invalid URL, most likely due to presence of 518 in the name.
    def url_for_version(self, version):
        return super().url_for_version(f"518-{version}")

    version("0.19", sha256="a287608997415f45401849d1227a42bb41b80a6e4a7da5776666f85ce6faec41")

    depends_on("py-setuptools", type="build")
