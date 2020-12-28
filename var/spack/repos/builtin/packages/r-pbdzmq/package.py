# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPbdzmq(RPackage):
    """'ZeroMQ' is a well-known library for high-performance asynchronous
    messaging in scalable, distributed applications. This package provides
    high level R wrapper functions to easily utilize 'ZeroMQ'. We mainly focus
    on interactive client/server programming frameworks. For convenience, a
    minimal 'ZeroMQ' library (4.1.0 rc1) is shipped with 'pbdZMQ', which can
    be used if no system installation of 'ZeroMQ' is available. A few wrapper
    functions compatible with 'rzmq' are also provided."""

    homepage = "http://r-pbd.org/"
    url      = "https://cloud.r-project.org/src/contrib/pbdZMQ_0.2-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pbdZMQ"

    version('0.3-3', sha256='ae26c13400e2acfb6463ff9b67156847a22ec79f3b53baf65119efaba1636eca')
    version('0.3-2', sha256='ece2a2881c662f77126e4801ba4e01c991331842b0d636ce5a2b591b9de3fc37')
    version('0.2-4', sha256='bfacac88b0d4156c70cf63fc4cb9969a950693996901a4fa3dcd59949ec065f6')

    depends_on('r@3.0.0:', when='@:0.2-5', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@0.2-6:', type=('build', 'run'))
    depends_on('r-r6', when='@:0.2-6', type=('build', 'run'))
    depends_on('libzmq@4.0.4:')
