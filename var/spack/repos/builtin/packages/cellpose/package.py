# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cellpose(PythonPackage):
    """A generalist algorithm for cell and nucleus segmentation that can be optimized for
    your own data"""

    homepage = "https://cellpose.readthedocs.io/"
    pypi = "cellpose/cellpose-2.2.3.tar.gz"

    license("BSD-3-Clause", checked_by="A-N-Other")

    version("2.2.3", sha256="7ff63cb60a154ce3c0a17ff05ed27d2aaaa1a24a4c7a8160c0a4c15443366618")

    variant("gui", default=False, description="Build the GUI")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest-runner", type="build")

    depends_on("py-numpy@1.20.0:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-natsort", type=("build", "run"))
    depends_on("py-tifffile", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-numba@0.53.0:", type=("build", "run"))
    depends_on("py-llvmlite", type=("build", "run"))
    depends_on("py-torch@1.6:", type=("build", "run"))
    # `copencv` provides `cv2` in place of opencv-python-headless specified in setup.py
    # +ximgproc is required from the contrib modules
    depends_on("opencv +python3+ximgproc", type=("build", "run"))
    depends_on("py-fastremap", type=("build", "run"))
    depends_on("py-imagecodecs", type=("build", "run"))
    depends_on("py-roifile", type=("build", "run"))

    depends_on("py-pyqtgraph@0.11.0:", type=("build", "run"), when="+gui")
    depends_on("py-pyqt6", type=("build", "run"), when="+gui")
    depends_on("py-pyqt6-sip", type=("build", "run"), when="+gui")
    depends_on("py-qtpy", type=("build", "run"), when="+gui")
    depends_on("py-superqt", type=("build", "run"), when="+gui")
    depends_on("py-google-cloud-storage", type=("build", "run"), when="+gui")
