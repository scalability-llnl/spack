# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpytree(PythonPackage):
    """A Tree Widget using jsTree."""

    homepage = "https://github.com/martinRenou/ipytree"
    pypi = "ipytree/ipytree-0.2.2.tar.gz"

    license("MIT")

    version("0.2.2", sha256="d53d739bbaaa45415733cd06e0dc420a2af3d173438617db472a517bc7a61e56")

    with default_args(type="build"):
        depends_on("py-jupyter-packaging@0.7")
        depends_on("py-jupyterlab@3")
        depends_on("py-setuptools@40.8:")

    depends_on("py-ipywidgets@7.5:8", type=("build", "run"))
