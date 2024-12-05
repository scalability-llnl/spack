# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycortex(PythonPackage):
    """Python Cortical mapping software for fMRI data."""

    # When pycortex is started it creates a user config file (on linux located
    # in ~/.config/pycortex) which can be problematic when reinstalling a newer
    # version with spack due to hardscoded absolute paths of the pycortex module

    homepage = "https://github.com/gallantlab/pycortex"
    pypi = "pycortex/pycortex-1.2.2.tar.gz"

    license("BSD-2-Clause")

    version("1.2.2", sha256="ac46ed6a1dc727c3126c2b5d7916fc0ac21a6510c32a5edcd3b8cfb7b2128414")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-future", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-tornado@4.3:", type=("build", "run"))
    depends_on("py-shapely", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-html5lib", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numexpr", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))  # is in install_requires
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-networkx@2.1:", type=("build", "run"))
    depends_on("py-imageio", type=("build", "run"))
    depends_on("py-wget", type=("build", "run"))

    # inkscape is not in spack
    # TODO remove this patch and add inkscape dependency once it is in
    def patch(self):
        # remove inkscape dependency
        filter_file(
            "from .testing_utils import INKSCAPE_VERSION", "", "cortex/utils.py", string=True
        )
        filter_file("open_inkscape=True", "open_inkscape=False", "cortex/utils.py", string=True)
        filter_file(
            "from .testing_utils import INKSCAPE_VERSION",
            "INKSCAPE_VERSION = None",
            "cortex/svgoverlay.py",
            string=True,
        )
