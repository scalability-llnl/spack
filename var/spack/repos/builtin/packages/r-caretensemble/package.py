# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaretensemble(RPackage):
    """Ensembles of Caret Models.

    Functions for creating ensembles of caret models: caretList() and
    caretStack(). caretList() is a convenience function for fitting multiple
    caret::train() models to the same dataset. caretStack() will make linear or
    non-linear combinations of these models, using a caret::train() model as a
    meta-model, and caretEnsemble() will make a robust linear combination of
    models using a GLM."""

    cran = "caretEnsemble"

    license("MIT")

    version("4.0.0", sha256="9177ad477fd2872e944231764227bcf5e2eabc9916dabce91f1a2a2decc98f43")
    version("2.0.2", sha256="d8fcf3742beddc723b68677682708408cc11dcb8b36a0f70f03e7c4763e04f4d")
    version("2.0.1", sha256="7e595e604ce2d9d32afbc5404e6fcbcd7f80e687316e9ca3303aca3e44c3ef88")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@4.0.0:")
    depends_on("r-pbapply", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-patchwork", type=("build", "run"), when="@4.0.0:")
    depends_on("r-rlang", type=("build", "run"), when="@4.0.0:")
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-caret", type=("build", "run"))

    depends_on("r-digest", type=("build", "run"), when="@:2.0.3")
    depends_on("r-gridextra", type=("build", "run"), when="@:2.0.3")
    depends_on("r-plyr", type=("build", "run"), when="@:2.0.3")
