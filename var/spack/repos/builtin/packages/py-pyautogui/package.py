# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-pyautogui
#
# You can edit this file again by typing:
#
#     spack edit py-pyautogui
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPyautogui(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    pypi     = "PyAutoGUI/PyAutoGUI-0.9.52.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.9.52', sha256='a486cb6b818bcbcdf98b48d010c7cee964134fa394b756e8ce6e50d43b58ecc8')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pymsgbox', type=('build', 'run'))
    depends_on('py-pytweening@1.0.1:', type=('build', 'run'))
    depends_on('py-pyscreeze@0.1.21:', type=('build', 'run'))
    depends_on('py-pygetwindow@0.0.5:', type=('build', 'run'))
    depends_on('py-mouseinfo', type=('build', 'run'))
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
