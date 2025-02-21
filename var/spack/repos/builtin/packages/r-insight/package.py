# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInsight(RPackage):
    """Easy Access to Model Information for Various Model Objects.

    A tool to provide an easy, intuitive and consistent access to information
    contained in various R models, like model formulas, model terms,
    information about random effects, data that was used to fit the model or
    data from response variables. 'insight' mainly revolves around two types of
    functions: Functions that find (the names of) information, starting with
    'find_', and functions that get the underlying data, starting with 'get_'.
    The package has a consistent syntax and works with many different model
    objects, where otherwise functions to access these information are
    missing."""

    cran = "insight"

    license("GPL-3.0-only")

    version("0.20.3", sha256="b60e189849cd3c368e9c2b2174e89c2dfbba3b34e84feb8a20af1bb758116bb2")
    version("0.19.1", sha256="1042629644c66b1a372fd4471d38adccc0c3a329879ef685b14b65575c1c98eb")
    version("0.18.6", sha256="ab0dc3c8ec765f2e93f7bcc3a7abb05140f71db24d50bf8cdd595a5a4e771cae")
    version("0.18.4", sha256="6e3f378bc2eb30c0300103bdd8a3e74371199b36867b45978ec9690a6fda0c5f")
    version("0.17.1", sha256="653c5542a0c953ad4b75800e2ab52eed244e1e698aa5bc9fc64dc657a3cece35")
    version("0.16.0", sha256="7944d7a386c99ea06d9d9e2b5f4aeb98fded7ec90b1cb908d03e278480be9e3d")
    version("0.15.0", sha256="d6a148c3e1cfcb3829e2f8950bcbf98f500ee88bebd7e2482f9b085542e93fee")
    version("0.14.1", sha256="0e7761997a46ee33039cdeff1779dbc210de3644e4444c6e893e4ef2f12cc129")

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@0.18.4:")
    depends_on("r@3.6:", type=("build", "run"), when="@0.19.2:")
