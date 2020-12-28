# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHumanize(PythonPackage):
    """This modest package contains various common humanization utilities, like
    turning a number into a fuzzy human readable duration ('3 minutes ago') or
    into a human readable size or throughput. It works with python 2.7 and 3.3
    and is localized to Russian, French, Korean and Slovak.
    """

    homepage = "https://github.com/jmoiron/humanize"
    url      = "https://pypi.io/packages/source/h/humanize/humanize-0.5.1.tar.gz"

    version('0.5.1', sha256='a43f57115831ac7c70de098e6ac46ac13be00d69abbf60bdcac251344785bb19')

    depends_on('py-setuptools', type='build')
