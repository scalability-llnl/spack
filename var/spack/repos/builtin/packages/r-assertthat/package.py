# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertthat(RPackage):
    """assertthat is an extension to stopifnot() that makes it easy to declare
    the pre and post conditions that you code should satisfy, while also
    producing friendly error messages so that your users know what they've done
    wrong."""

    homepage = "https://cloud.r-project.org/package=assertthat"
    url      = "https://cloud.r-project.org/src/contrib/assertthat_0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertthat"

    version('0.2.1', sha256='85cf7fcc4753a8c86da9a6f454e46c2a58ffc70c4f47cac4d3e3bcefda2a9e9f')
    version('0.2.0', sha256='d73ef79b1e75293ed889a99571b237a95829c099f7da094d4763f83ea6fde5f2')
    version('0.1', sha256='1363645a9a128f615aa0641dc5f5c5abd960b1c38320492366dad1e7a5c29a37')
