# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurom(PythonPackage):
    """Python library neuron morphology analysis"""

    homepage = "https://github.com/BlueBrain/NeuroM"
    git = "https://github.com/BlueBrain/NeuroM.git"
    pypi = "neurom/neurom-2.2.1.tar.gz"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("3.2.4", sha256="a584e0979b54deee906dd716ea90de20773e20b527d83960d0fe655b0905eb4a")

    variant("plotly", default=False, description="Enable plotly support")

    depends_on("py-setuptools@42:", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")
    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.2.1:", type=("build", "run"))
    depends_on("py-morphio@3.3.6:", type=("build", "run"))
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
    depends_on("py-pandas@1.0.5:", type=("build", "run"))
    depends_on("py-pyyaml@3.10:", type=("build", "run"))
    depends_on("py-scipy@1.2.0:", type=("build", "run"))
    depends_on("py-tqdm@4.8.4:", type=("build", "run"))

    depends_on("py-plotly@3.6.0:", type=("build", "run"), when="+plotly")
    depends_on("py-psutil@5.5.1:", type=("build", "run"), when="+plotly")
