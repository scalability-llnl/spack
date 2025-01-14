# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbdime(PythonPackage):
    """Diff and merge of Jupyter Notebooks"""

    homepage = "https://nbdime.readthedocs.io/"
    pypi = "nbdime/nbdime-3.1.1.tar.gz"

    version("3.2.1", sha256="31409a30f848ffc6b32540697e82d5a0a1b84dcc32716ca74e78bcc4b457c453")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2021-41134
        version("3.1.1", sha256="67767320e971374f701a175aa59abd3a554723039d39fae908e72d16330d648b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@40.8.0:", type="build")
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-tornado", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-gitpython@:2.1.3,2.1.7:", type=("build", "run"))
    depends_on("py-jupyter-server", type=("build", "run"))
    depends_on("py-jupyter-server-mathjax@0.2.2:", type=("build", "run"))
    depends_on("py-jinja2@2.9:", type=("build", "run"))
    # From pyproject.toml
    depends_on("py-jupyterlab@3.0:3", type=("build", "run"))
    depends_on("py-wheel", type="build")
