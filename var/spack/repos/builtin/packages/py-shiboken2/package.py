# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyShiboken2(PythonPackage):
    """Python / C++ bindings helper module."""

    homepage = "https://www.pyside.org/"

    skip_version_audit = ["platform=windows"]

    if sys.platform.startswith("linux"):
        version(
            "5.15.2",
            url="https://files.pythonhosted.org/packages/cp35.cp36.cp37.cp38.cp39/s/shiboken2/shiboken2-5.15.2-5.15.2-cp35.cp36.cp37.cp38.cp39-abi3-manylinux1_x86_64.whl",
            sha256="4aee1b91e339578f9831e824ce2a1ec3ba3a463f41fda8946b4547c7eb3cba86",
        )
    elif sys.platform == "darwin":
        version(
            "5.15.2",
            url="https://files.pythonhosted.org/packages/cp35.cp36.cp37.cp38.cp39/s/shiboken2/shiboken2-5.15.2-5.15.2-cp35.cp36.cp37.cp38.cp39-abi3-macosx_10_13_intel.whl",
            sha256="edc12a4df2b5be7ca1e762ab94e331ba9e2fbfe3932c20378d8aa3f73f90e0af",
        )

    depends_on("python@3.5:3.9", type=("build", "run"))
