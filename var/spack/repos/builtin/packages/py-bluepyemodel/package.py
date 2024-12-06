# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyemodel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://github.com/BlueBrain/BluePyEModel"
    pypi = "bluepyemodel/bluepyemodel-0.0.46.tar.gz"

    license("Apache-2.0")

    version("0.0.64", sha256="14fec4f77fb79295ce7cfe1711cd32f66e5d3e0ebc8da9404491ab7f59da1e71")
    version("0.0.59", sha256="5e8869522d82e719f9775c2d95cfe953cedc66bc44355765a6f406289baf6791")
    version("0.0.58", sha256="327de9d2c49e7ff83cc77850873293299d4eacf95b3cf33716e5a8501685f08c")
    version("0.0.57", sha256="0b91e39e5066ab4a996bd932577b49648169e549c5f05bb3f93e345b4b186093")
    version("0.0.46", sha256="ad4c125e491f3337fcc341a4f389b8a616d883ce50fd77d9fb0ea6e13be5da61")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-ipyparallel@6.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-bluepyopt@1.12.12:", type=("build", "run"))
    depends_on("py-bluepyefe@2.2.0:", type=("build", "run"))
    depends_on("py-neurom@3.0:3", type=("build", "run"))
    depends_on("py-efel@3.1:", type=("build", "run"))
    depends_on("py-configparser", type=("build", "run"))
    depends_on("py-morph-tool@2.8:", type=("build", "run"))
    depends_on("py-fasteners@0.16:", type=("build", "run"))
    depends_on("neuron+python@8.0:", type=("build", "run"))
    depends_on("py-jinja2@3.0.3", when="@0.0.11:", type=("build", "run"))
    depends_on("py-currentscape@0.0.11:", type=("build", "run"))
