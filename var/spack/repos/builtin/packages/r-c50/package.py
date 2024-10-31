# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RC50(RPackage):
    """C5.0 Decision Trees and Rule-Based Models.

    C5.0 decision trees and rule-based models for pattern recognition that
    extend the work of Quinlan (1993, ISBN:1-55860-238-0)."""

    cran = "C50"

    version("0.1.8", sha256="bbd1bd5ed0ed5257529396697bea2a5841c8159470ba09d2066411d4aeda9c15")
    version("0.1.6", sha256="cc20c0e2656287e6ca76ea341a703c816798b212ea4658f249ec047dbbf18cb4")
    version("0.1.5", sha256="f0c17b4830371832ca64f5fcc702351a394ee90b384e0865307de9447f3f16d7")
    version("0.1.3.1", sha256="0b151ba8deef50ab2e2ad8469d87f54f0c6ab862f5c790ed8bb16cb3b8027546")
    version("0.1.2", sha256="8f459856e0309274bee24462b7145db4eba1d71031c236db39000a5375bdfaba")
    version("0.1.1", sha256="03bc1fc2f64bcd5c680568a24902deafab1965074a66f8802bc4cd0335bd01df")
    version("0.1.0-24", sha256="617ee8ae617a075213414c07739ce92d9e6927783d01588fd0e2315157065e9d")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-partykit", type=("build", "run"))
    depends_on("r-cubist@0.2.1:", type=("build", "run"))
    depends_on("r-cubist@0.2.3:", type=("build", "run"), when="@0.1.3.1:")
    depends_on("r-cubist@0.3.0:", type=("build", "run"), when="@0.1.5:")
