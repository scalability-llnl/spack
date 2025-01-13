# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPanel(PythonPackage):
    """A high level app and dashboarding solution for Python."""

    homepage = "https://panel.holoviz.org/"
    pypi = "panel/panel-0.14.4.tar.gz"

    license("BSD-3-Clause")

    version("1.5.2", sha256="30a45f314716bdde2de5c002fbd3a0b4d6ff85459e2179284df559455ff1534b")
    version("0.14.4", sha256="b853d2f53d7738ec6372525360c5bf9427a71ed990685ccac703bc9b442e9951")

    with when("@0.14.4"):
        depends_on("py-param@1.12:", type=("build", "run"))
        depends_on("py-pyct@0.4.4:", type=("build", "run"))
        depends_on("py-setuptools@42:", type=("build", "run"))
        depends_on("py-bokeh@2.4.3:2.4", type=("build", "run"))
        depends_on("py-pyviz-comms@0.7.4:", type=("build", "run"))
        depends_on("py-requests", type=("build", "run"))
        depends_on("py-bleach", type=("build", "run"))
        depends_on("py-packaging", type="build")
        depends_on("py-tqdm@4.48:", type=("build", "run"))
        depends_on("py-markdown", type=("build", "run"))
        depends_on("py-typing-extensions", type=("build", "run"))

    with when("@1.5.2"):
        depends_on("python@3.10:", type=("build", "run"))
        depends_on("py-hatchling", type="build")
        depends_on("py-hatch-vcs", type="build")
        depends_on("py-param@2.1:2", type=("build", "run"))
        depends_on("py-bokeh@3.5:3.6", type=("build", "run"))
        depends_on("py-pyviz-comms@2:", type=("build", "run"))
        depends_on("py-requests", type=("build", "run"))
        depends_on("py-packaging", type=("build", "run"))
        # Version 18 or later are requested by py-panel
        depends_on("node-js@18:", type=("build", "run"))
        # Version 9 is not requested explicitly, it's
        # a guess that the more recent version of node-js
        # should go with a more recent version of npm
        depends_on("npm@9:", type=("build", "run"))

        depends_on("py-markdown", type="run")
        depends_on("py-markdown-it-py", type="run")
        depends_on("py-linkify-it-py", type="run")
        depends_on("py-mdit-py-plugins", type="run")
        depends_on("py-bleach", type="run")
        depends_on("py-typing-extensions", type="run")
        depends_on("py-pandas@1.2:", type="run")
        depends_on("py-tqdm", type="run")
