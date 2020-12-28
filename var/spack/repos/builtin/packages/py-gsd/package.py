# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGsd(PythonPackage):
    """The GSD file format is the native file format for HOOMD-blue. GSD files
    store trajectories of the HOOMD-blue system state in a binary file with
    efficient random access to frames. GSD allows all particle and topology
    properties to vary from one frame to the next. Use the GSD Python API to
    specify the initial condition for a HOOMD-blue simulation or analyze
    trajectory output with a script. Read a GSD trajectory with a visualization
    tool to explore the behavior of the simulation."""

    homepage = "https://gsd.readthedocs.io/en/stable/#"
    url      = "https://pypi.io/packages/source/g/gsd/gsd-1.9.3.tar.gz"

    version('1.9.3', sha256='c6b37344e69020f69fda2b8d97f894cb41fd720840abeda682edd680d1cff838')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy@1.9.3:1.999999', type=('build', 'run'))
