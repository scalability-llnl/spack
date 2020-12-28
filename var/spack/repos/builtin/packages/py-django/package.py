# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDjango(PythonPackage):
    """The Web framework for perfectionists with deadlines."""

    homepage = "https://www.djangoproject.com/"
    url      = "https://github.com/django/django/archive/3.0.5.tar.gz"

    version('3.0.5',  sha256='ef2d4f26414dc9598afce9c56cee4578313b88861cedfc5b3d9a71078e5cc79b')
    version('3.0.4',  sha256='99699643d83acfab51d3ad73c2c2904173e03a4f59fe24c3d494e4fafc0b679f')
    version('3.0.3',  sha256='d953c950f0c395db065c8bc39d20e87faded376632a3aacf889ae92d5adaac8b')
    version('3.0.2',  sha256='ca316b1179a16931ed872ce970aabefcf3d41fe0d4b1a8e1301ec59e1e0ab45b')
    version('3.0.1',  sha256='85349b9366364847264b2b707ffcff5a27a022afa29aac0e904ca672cbe5ee65')
    version('2.2.12', sha256='ec490c67bd2780b4ec4f5355cd99fa2fa6007f81695dd45a9e8f7ccc5ff17772')
    version('2.2.11', sha256='f4274181973f0f021cc00419cfa342f1a6f862406e766ae93e7fbba9d84c680c')
    version('2.2.10', sha256='3741536cf122d6695e8575b2fcf67c18812751fd3143393ea75c01a277afdacc')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.6:',   type=('build', 'run'))
    depends_on('py-pytz',       type=('build', 'run'))
    depends_on('py-sqlparse',   type=('build', 'run'))
    depends_on('py-asgiref',    type=('build', 'run'))
