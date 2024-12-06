# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.pkg.builtin.mock.simple_inheritance as si
from spack.package import *


class MultimoduleInheritance(si.BaseWithDirectives):
    """Simple package which inherits a method and several directives"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/multimodule-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("openblas", when="+openblas")
