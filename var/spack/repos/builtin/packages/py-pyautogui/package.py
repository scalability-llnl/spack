# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyautogui(PythonPackage):
    """PyAutoGUI lets your Python scripts control the mouse and
    keyboard to automate interactions with other
    applications."""

    homepage = "https://pyautogui.readthedocs.io/en/latest/"
    pypi = "PyAutoGUI/PyAutoGUI-0.9.52.tar.gz"

    license("BSD-3-Clause")

    version("0.9.53", sha256="d31de8f712218d90be7fc98091fce1a12a3e9196e0c814eb9afd73bb2ec97035")
    version("0.9.52", sha256="a486cb6b818bcbcdf98b48d010c7cee964134fa394b756e8ce6e50d43b58ecc8")

    depends_on("py-setuptools", type="build")
    depends_on("py-pymsgbox", type=("build", "run"))
    depends_on("py-pytweening@1.0.1:", type=("build", "run"))
    depends_on("py-pyscreeze@0.1.21:", type=("build", "run"))
    depends_on("py-pygetwindow@0.0.5:", type=("build", "run"))
    depends_on("py-mouseinfo", type=("build", "run"))

    depends_on("py-python3-xlib", when="platform=linux", type=("build", "run"))

    # Missing packages; commented out for now
    # depends_on('py-pyobjc-core', when='platform=darwin', type=('build', 'run'))
    # depends_on('py-pyobjc', when='platform=darwin', type=('build', 'run'))
    conflicts("platform=darwin")
