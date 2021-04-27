# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPySpy(PythonPackage):
    """A Sampling Profiler for Python."""

    homepage = "https://github.com/benfred/py-spy"
    url      = "https://github.com/benfred/py-spy/archive/v0.3.3.tar.gz"

    version('0.3.3', sha256='41454d3d9132da45c72f7574faaff65f40c757720293a277ffa5ec5a4b44f902')

    depends_on('py-setuptools', type='build')
    # TODO: uses cargo to download and build dozens of dependencies.
    # Need to figure out how to manage these with Spack once we have a
    # CargoPackage base class.
    depends_on('rust', type='build')
    depends_on('unwind')
