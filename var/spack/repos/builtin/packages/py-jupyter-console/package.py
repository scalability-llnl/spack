# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterConsole(PythonPackage):
    """Jupyter Terminal Console"""

    homepage = "https://github.com/jupyter/jupyter_console"
    pypi = "jupyter_console/jupyter_console-6.4.0.tar.gz"

    version("6.4.4", sha256="172f5335e31d600df61613a97b7f0352f2c8250bbd1092ef2d658f77249f89fb")
    version("6.4.3", sha256="55f32626b0be647a85e3217ddcdb22db69efc79e8b403b9771eb9ecc696019b5")
    version("6.4.0", sha256="242248e1685039cd8bff2c2ecb7ce6c1546eb50ee3b08519729e6e881aec19c7")
    version("6.1.0", sha256="6f6ead433b0534909df789ea64f0a14cdf9b6b2360757756f08182be4b9e431b")
    version("5.2.0", sha256="545dedd3aaaa355148093c5609f0229aeb121b4852995c2accfa64fe3e0e55cd")
    version("5.0.0", sha256="7ddfc8cc49921b0ed852500928922e637f9188358c94b5c76339a5a8f9ac4c11")
    version("4.1.1", sha256="d754cfd18d258fa9e7dde39a36e589c4a7241075b5d0f420691fa3d50e4c4ae3")
    version("4.1.0", sha256="3f9703b632e38d68713fc2ea1f546edc4db2a8f925c94b6dd91a8d0c13816ce9")
    version("4.0.3", sha256="555be6963a8f6431fbe1d424c7ffefee90824758058e4c9a2ab3aa045948eb85")
    version("4.0.2", sha256="97e27e1c27a6dd04d166b7a4c81d717becdd979a0879a628e08f295a43a2bc58")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"), when="@6:")
    depends_on("python@3.6:", type=("build", "run"), when="@6.2:")
    depends_on("python@3.7:", type=("build", "run"), when="@6.4.4:")
    depends_on("py-setuptools@40.8.0:", type="build", when="@6.2:")
    depends_on("py-jupyter-client@7.0.0:", type=("build", "run"), when="@6.4.3:")
    depends_on("py-jupyter-client", type=("build", "run"))
    depends_on("py-ipython@:5.8.0", type=("build", "run"), when="@:5")
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-ipykernel", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-prompt-toolkit@1.0.0:1", type=("build", "run"), when="@:5")
    depends_on("py-prompt-toolkit@2.0.0:2,3.0.2:3.0", type=("build", "run"), when="@6:")
