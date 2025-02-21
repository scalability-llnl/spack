# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaracas(RPackage):
    """Computer Algebra.

    Computer algebra via the 'SymPy' library (<https://www.sympy.org/>). This
    makes it possible to solve equations symbolically, find symbolic integrals,
    symbolic sums and other important quantities."""

    cran = "caracas"

    license("GPL-2.0-or-later")

    version("2.1.1", sha256="3b31b5b1c2fa038e5a6df12cfe62390f9af0461873a38921d6c26468363c2661")
    version("2.0.0", sha256="9271239bf7457787371cbd44be74cb9909d67ab7c975b1744d8cf60d8b044b95")
    version("1.1.2", sha256="9c726c77508617e74d1a11ac6e276973df42e1ad81145db455cc6e420526c757")
    version("1.1.1", sha256="e14487c9492417cf5c7d7373c37dbb4fea4d91180a1a03154e51eaa7878b2769")
    version("1.0.1", sha256="2482dd7b77791243b8174cb41b80b735c3ebd7db837bbf991127514f492af594")
    version("1.0.0", sha256="0da6f1d94d1dacb1c11a3635bdff8f7cd8f84373deffa7126636d0876d48e42b")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-reticulate@1.14:", type=("build", "run"))
    depends_on("r-doby@4.6.15:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-matrix", type=("build", "run"), when="@2.0.0:")
    depends_on("r-magrittr", type=("build", "run"), when="@1.1.1:")
    depends_on("python@3.6:", type=("build", "run"))
