# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpdb(PythonPackage):
    """ipdb is the iPython debugger and has many additional features, including
    a better interactive debugging experience via colorized output."""

    homepage = "https://pypi.python.org/pypi/ipdb"
    url      = "https://pypi.io/packages/source/i/ipdb/ipdb-0.10.1.tar.gz"

    version('0.10.1', sha256='bb2948e726dbfb2687f4a582088b3f170b2556ba8e54ae1231c783c97e99ec87')

    # :TODO:
    # There might be potential to add variants here, but at the time of writing
    # this the original packager does not know what they are. See the 3rd party
    # section on ipdb's GitHub:
    #     https://github.com/gotcha/ipdb#third-party-support
    depends_on('python@2.6:2.8,3.2:')

    # Dependencies gathered from:
    #     https://github.com/gotcha/ipdb/blob/master/setup.py
    # However additional dependencies added below were found via testing.
    depends_on('py-setuptools',      type='build')
    # ipdb needs iPython and others available at runtime
    depends_on('py-ipython@0.10.2:', type=('build', 'link'))
    depends_on('py-traitlets',       type=('build', 'link'))
    depends_on('py-six',             type=('build', 'link'))
    depends_on('py-pexpect',         type=('build', 'link'))
    depends_on('py-prompt-toolkit',  type=('build', 'link'))
