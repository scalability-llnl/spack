# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWidgetsnbextension(PythonPackage):
    """IPython HTML widgets for Jupyter"""

    pypi = "widgetsnbextension/widgetsnbextension-1.2.6.tar.gz"

    license("BSD-3-Clause")

    version("4.0.3", sha256="34824864c062b0b3030ad78210db5ae6a3960dfb61d5b27562d6631774de0286")
    version("3.6.0", sha256="e84a7a9fcb9baf3d57106e184a7389a8f8eb935bf741a5eb9d60aa18cc029a80")
    version("3.5.1", sha256="079f87d87270bce047512400efd70238820751a11d2d8cb137a5a5bdbaf255c7")
    version("3.4.2", sha256="fa618be8435447a017fd1bf2c7ae922d0428056cfc7449f7a8641edf76b48265")
    version("3.4.0", sha256="c9d6e426a1d79d132b57b93b368feba2c66eb7b0fd34bdb901716b4b88e94497")
    version("3.3.0", sha256="c5280a62d293735cdadc7b8884e2affcfb0488420ee09963577f042359726392")
    version("1.2.6", sha256="c618cfb32978c9517caf0b4ef3aec312f8dd138577745e7b0d4abfcc7315ce51")

    depends_on("py-setuptools", type="build")
    depends_on("py-jupyter-packaging@0.10:0", when="@4.0.3:", type="build")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("python@3.7:", when="@4.0.3:", type=("build", "run"))
    depends_on("py-notebook@4.2.0:", when="@1.2.6", type=("build", "run"))
    depends_on("py-notebook@4.4.1:", type=("build", "run"), when="@3.3.0:3")
