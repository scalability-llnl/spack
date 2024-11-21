# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

from spack.package import *


class PyMosek(PythonPackage):
    """MOSEK is a package for large-scale convex and mixed-integer optimization, including LP, QP, SOCP, exponential and power cone problems, SDP, QCQP and MIP. Documentation and examples can be found at the https://www.mosek.com/documentation. MOSEK requires a license. Free of charge trial licenses as well as licenses for non-commercial academic use can be obtained from https://www.mosek.com."""

    homepage = "https://www.mosek.com"

    url = "https://pypi.org/project/Mosek/"

    maintainers("bourdin")

    license("https://mosek.com/products/license-agreement", checked_by="bourdin")

    arch = platform.machine()
    os = sys.platform

    if os == "darwin":
        version(
            "10.2.8",
            url="https://files.pythonhosted.org/packages/c8/e8/277d457303360f7e9a226915b98df8537fcf9565d9d86c7e4dc2edb8f795/Mosek-10.2.8-cp38-abi3-macosx_11_0_arm64.whl",
            sha256="3f73f6c4a0617da43fb9ba566d28c1a464d62b858c87829a5e6c4b4b6d1d01f7",
        )
    elif os == "windows":
        version(
            "10.2.8",
            url="https://files.pythonhosted.org/packages/da/08/ff270463ddc1360aa8ea4eba0454c99d5d28bfe829648be92fe95c477ecf/Mosek-10.2.8-cp37-abi3-win_amd64.whl",
            sha256="1ec167c406e2d3a2cc2c701d079b8d431f36c3f2332828a2276edc88927aa33d",
        )
    elif os.startswith("linux"):
        if arch == "aarch64":
            version(
                "10.2.8",
                url="https://files.pythonhosted.org/packages/c0/87/7741f57f6fe616483bb57b2a05e1c543faf31e7c03b579214614467d49fe/Mosek-10.2.8-cp37-abi3-manylinux_2_29_aarch64.whl",
                sha256="6ec484caa8f2255636617aea4c09f4bba991325b3b4df46ba30a1b0f4849d719",
            )
        elif arch == "x86_64":
            version(
                "10.2.8",
                url="https://files.pythonhosted.org/packages/8a/ee/f591ed3e896035f9af7227708cb209eecdf6e6898b7276e1cb5a9cfe027e/Mosek-10.2.8-cp37-abi3-manylinux2014_x86_64.whl",
                sha256="e1aa87d962299178728ed60f963e3d1ad088322d02f46f621fa56bed545b5b17",
            )

    depends_on("python@3.7:3.12", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
