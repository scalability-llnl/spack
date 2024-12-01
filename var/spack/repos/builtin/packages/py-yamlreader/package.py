# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYamlreader(PythonPackage):
    """Yamlreader merges YAML data from a directory, a list of files or a
    file glob."""

    homepage = "https://pyyaml.org/wiki/PyYAML"
    pypi = "yamlreader/yamlreader-3.0.4.tar.gz"

    version("3.0.4", sha256="765688036d57104ac26e4500ab088d42f4f2d06687ce3daa26543d7ae38c2470")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
