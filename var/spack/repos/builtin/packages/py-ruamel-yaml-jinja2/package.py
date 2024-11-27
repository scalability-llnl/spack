# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRuamelYamlJinja2(PythonPackage):
    """jinja2 pre and post-processor to update with YAML."""

    homepage = "https://sourceforge.net/p/ruamel-yaml-jinja2/code/ci/default/tree"
    pypi = "ruamel.yaml.jinja2/ruamel.yaml.jinja2-0.2.7.tar.gz"

    license("MIT")

    version("0.2.7", sha256="8449be29d9a157fa92d1648adc161d718e469f0d38a6b21e0eabb76fd5b3e663")

    depends_on("py-setuptools", type="build")

    # __init__.py
    depends_on("py-ruamel-yaml@0.16.1:", type=("build", "run"))
