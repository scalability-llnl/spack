# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyShellescape(PythonPackage):
    """Shell escape a string to safely use it as a token in a shell command"""

    homepage = "https://github.com/chrissimpkins/shellescape"
    pypi = "shellescape/shellescape-3.8.1.tar.gz"

    version("3.8.1", sha256="40b310b30479be771bf3ab28bd8d40753778488bd46ea0969ba0b35038c3ec26")

    depends_on("py-setuptools", type="build")
