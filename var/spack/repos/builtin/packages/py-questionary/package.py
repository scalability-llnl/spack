# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQuestionary(PythonPackage):
    """Questionary is a Python library for effortlessly building pretty
    command line interfaces."""

    homepage = "https://github.com/tmbo/questionary"
    pypi     = "questionary/questionary-1.9.0.tar.gz"

    version('1.9.0', sha256='a050fdbb81406cddca679a6f492c6272da90cb09988963817828f697cf091c55')

    depends_on('python@3.6:3.9.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-prompt-toolkit@2.0:3.99', type=('build', 'run'))
