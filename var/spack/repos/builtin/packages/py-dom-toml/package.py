# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDomToml(PythonPackage):
    """Dom's tools for Tom's Obvious, Minimal Language."""

    homepage = "https://github.com/domdfcoding/dom_toml"
    pypi = "dom_toml/dom_toml-0.6.1.tar.gz"

    license("MIT")

    version("0.6.1", sha256="a0bfc204ae32c72ed36e526dce56108a3b20741ac3c055207206ce3b2f302868")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-domdf-python-tools@2.8:", type=("build", "run"))
    depends_on("py-toml@0.10.2:", type=("build", "run"))
