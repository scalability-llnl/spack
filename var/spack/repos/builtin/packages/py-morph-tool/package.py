# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/morph-tool"
    git = "https://github.com/BlueBrain/morph-tool.git"
    pypi = "morph-tool/morph-tool-2.9.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("2.9.1", sha256="305e9456c8047726588b23dfa070eb95ccbe5573e9fea3e0a83dc93eacdf61dc")
    version("2.9.0", sha256="c60d4010e17ddcc3f53c864c374fffee05713c8f8fd2ba4eed7706041ce1fa47")

    variant("nrn", default=False, description="Enable additional neuron support")
    variant("plot", default=False, description="Enable additional plotly support")
    variant("parallel", default=False, description="Enable additional parallel support")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-click@6.7:", type=("build", "run"))
    depends_on("py-deprecation@2.1.0:", type=("build", "run"))
    depends_on("py-more-itertools@8.6.0:", type=("build", "run"))
    depends_on("py-morphio@3", type=("build", "run"))
    depends_on("py-neurom@3", type=("build", "run"))
    depends_on("py-numpy@1.14:", type=("build", "run"))
    depends_on("py-pandas@1.0.3:", type=("build", "run"))
    depends_on("py-xmltodict@0.12.0:", type=("build", "run"))

    depends_on("py-plotly@4.1.0:", type=("build", "run"), when="+plot")
    depends_on("py-dask+bag@2.19.0:", type=("build", "run"), when="+parallel")
    depends_on("neuron+python@7.8:", type=("build", "run"), when="+nrn")
    depends_on("py-bluepyopt@1.9.37:", type=("build", "run"), when="+nrn")
