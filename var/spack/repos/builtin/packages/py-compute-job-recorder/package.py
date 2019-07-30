# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install py-compute-job-recorder
#
# You can edit this file again by typing:
#
#     spack edit py-compute-job-recorder
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyComputeJobRecorder(PythonPackage):
    """A tool for recording a compute job progress when undertaking batch processing tasks."""

    homepage = "https://www.remotesensing.info/compute_job_recorder"
    url      = "https://bitbucket.org/petebunting/compute_job_recorder/downloads/ComputeJobRecorder-0.0.1.tar.gz"

    version('0.0.1', sha256='0347c8a51829b1f8bae2bcaf370dc4c78dfa2e6340ad2489e9e15aaa3981a165')

    depends_on('py-setuptools', type='build')
    depends_on('sqlite',        type=('build', 'run'))
    depends_on('py-sqlalchemy', type=('build', 'run'))

    def install(self, spec, prefix):
        import subprocess
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)

