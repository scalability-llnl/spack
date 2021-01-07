# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install py-deeplabcut
#
# You can edit this file again by typing:
#
#     spack edit py-deeplabcut
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyDeeplabcut(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/DeepLabCut/DeepLabCut/archive/v2.2b8.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2.2b8',   sha256='eb6180741bb7eab173e09118bad60551b3c9ab2c8d4ed68460979105137fe72e')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on("py-bayesian-optimization", type=('build', 'run'))
    depends_on("py-certifi", type=('build', 'run'))
    depends_on("py-chardet", type=('build', 'run'))
    depends_on("py-click", type=('build', 'run'))
    depends_on("py-cython", type=('build', 'run'))
    depends_on("py-easydict", type=('build', 'run'))
    depends_on("py-filterpy", type=('build', 'run'))
    depends_on("py-h5py", type=('build', 'run'))
    depends_on("py-intel-openmp", type=('build', 'run'))
    depends_on("py-imgaug", type=('build', 'run'))
    depends_on("py-ipython", type=('build', 'run'))
    depends_on("py-ipython-genutils", type=('build', 'run'))
    depends_on("py-numba@0.51.1", type=('build', 'run'))
    depends_on("py-matplotlib@3.1.3", type=('build', 'run'))
    depends_on("py-moviepy@:1.0.1", type=('build', 'run'))
    depends_on("py-numpy@1.16.4", type=('build', 'run'))
    depends_on("py-opencv-python-headless", type=('build', 'run'))
    depends_on("py-pandas@1.0.1:", type=('build', 'run'))
    depends_on("py-patsy", type=('build', 'run'))
    depends_on("py-python-dateutil", type=('build', 'run'))
    depends_on("py-pyyaml", type=('build', 'run'))
    depends_on("py-requests", type=('build', 'run'))
    depends_on("py-ruamel-yaml@0.15.0:", type=('build', 'run'))
    depends_on("py-setuptools", type=('build', 'run'))
    depends_on("py-scikit-image", type=('build', 'run'))
    depends_on("py-scikit-learn", type=('build', 'run'))
    depends_on("py-scipy@1.4:", type=('build', 'run'))
    depends_on("py-six", type=('build', 'run'))
    depends_on("py-statsmodels@0.11:", type=('build', 'run'))
    depends_on("py-tables", type=('build', 'run'))
    depends_on("py-tensorpack@0.9.8", type=('build', 'run'))
    depends_on("py-tqdm", type=('build', 'run'))
    depends_on("py-wheel", type=('build', 'run'))


    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
