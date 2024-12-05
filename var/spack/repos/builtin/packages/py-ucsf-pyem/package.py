# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class PyUcsfPyem(PythonPackage):
    """UCSF pyem is a collection of Python modules and command-line
    utilities for electron microscopy of biological samples."""

    homepage = "https://github.com/asarnow/pyem"
    git = "https://github.com/asarnow/pyem.git"

    maintainers("dorton21")

    license("GPL-3.0-only", checked_by="A-N-Other")

    # Using commits as releases haven't been updated in since 2019
    version("2024-02-01", commit="e92cd4d40087c44945bce867a359838a806bd31f")
    version("2021-04-07", commit="ed0527f98657d21d887357426b74e5240d477fae")

    depends_on("py-setuptools", type="build")

    # Requirement versions taken from requirements.txt
    depends_on("py-future@0.15:", type=("build", "run"))
    depends_on("py-numba@0.41:", type=("build", "run"))
    depends_on("py-numpy@1.14:", type=("build", "run"))
    depends_on("py-scipy@1.2:", type=("build", "run"))
    depends_on("py-matplotlib@2.2:", type=("build", "run"))
    depends_on("py-seaborn@0.9:", type=("build", "run"))
    depends_on("py-pandas@0.23.4:", type=("build", "run"))
    depends_on("py-pathos@0.2.1:", type=("build", "run"))
    depends_on("py-pyfftw@0.10:", type=("build", "run"))
    depends_on("py-healpy@1.11:", type=("build", "run"))
    depends_on("py-natsort@6.0:", type=("build", "run"))

    # Extracts scripts into bin for proper usage, ensures +x where not set
    @run_after("install")
    def install_scripts(self):
        mkdir(self.prefix.bin)
        for script in glob.glob("*.py"):
            if script != "setup.py":
                os.chmod(script, 0o755)
                install(script, self.prefix.bin)
