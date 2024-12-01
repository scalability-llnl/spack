# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeyboard(PythonPackage):
    """Take full control of your keyboard with this small
    Python library. Hook global events, register hotkeys,
    simulate key presses and much more."""

    homepage = "https://github.com/boppreh/keyboard"
    pypi = "keyboard/keyboard-0.13.5.zip"

    license("MIT")

    version("0.13.5", sha256="63ed83305955939ca5c9a73755e5cc43e8242263f5ad5fd3bb7e0b032f3d308b")

    depends_on("py-setuptools", type="build")
    # depends_on('py-pyobjc', when='platform=darwin', type=('build', 'run'))

    # Until py-pyobjc can be created, specifying conflict with platform=darwin
    conflicts("platform=darwin")
