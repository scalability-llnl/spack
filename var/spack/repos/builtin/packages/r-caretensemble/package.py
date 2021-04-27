# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCaretensemble(RPackage):
    """caretEnsemble: Ensembles of Caret Models

    Functions for creating ensembles of caret models: caretList() and
    caretStack(). caretList() is a convenience function for fitting multiple
    caret::train() models to the same dataset. caretStack() will make linear or
    non-linear combinations of these models, using a caret::train() model as a
    meta-model, and caretEnsemble() will make a robust linear combination of
    models using a GLM."""

    homepage = "https://github.com/zachmayer/caretEnsemble"
    url      = "https://cloud.r-project.org/src/contrib/caretEnsemble_2.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/caretEnsemble"

    version('2.0.1', sha256='7e595e604ce2d9d32afbc5404e6fcbcd7f80e687316e9ca3303aca3e44c3ef88')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-pbapply', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-caret', type=('build', 'run'))
