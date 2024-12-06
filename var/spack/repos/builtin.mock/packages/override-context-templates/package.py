# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OverrideContextTemplates(Package):
    """This package updates the context for Tcl modulefiles.

    And additional lines that shouldn't be in the short description.
    """

    homepage = "http://www.fake-spack-example.org"
    url = "http://www.fake-spack-example.org/downloads/fake-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    tcl_template = "extension.tcl"
    tcl_context = {"sentence": "sentence from package"}
