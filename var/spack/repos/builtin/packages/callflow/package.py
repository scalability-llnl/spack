# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Callflow(PythonPackage):
    """CallFlow is an interactive visual analysis tool that provides a
    high-level overview of CCTs together with semantic refinement
    operations to progressively explore the CCTs."""

    homepage = "https://github.com/LLNL/CallFlow"
    url = "https://github.com/LLNL/CallFlow/archive/v1.1.0.tar.gz"
    git = "https://github.com/LLNL/CallFlow.git"

    maintainers("bhatiaharsh", "jarusified")

    license("MIT")

    version("develop", branch="develop")
    version("1.1.2", sha256="60d2327843469f42be9366ff31d7a6afc85021af4e38b7d6704b2d8c3da7ed36")
    version("1.1.1", sha256="a52e6e0697a406dfe391225d3cc3c5c5a12a6c86b68f0f8e47777c79fd45cb28")
    version("1.1.0", sha256="f8b875eb62fbac04b117e3c23fccff99d768158226a9b7fa222a2b2a6acafa44")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-hatchet", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))

    depends_on("py-colorlog", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))

    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))

    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-flask-socketio", type=("build", "run"))
    depends_on("py-flask-cors", type=("build", "run"))
