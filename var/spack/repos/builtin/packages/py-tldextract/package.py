# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTldextract(PythonPackage):
    """
    Accurately separates a URL's subdomain, domain, and public suffix,
    using the Public Suffix List (PSL). By default, this includes the
    public ICANN TLDs and their exceptions. You can optionally support
    the Public Suffix List's private domains as well.
    """

    homepage = "https://github.com/john-kurkowski/tldextract"
    pypi = "tldextract/tldextract-3.4.1.tar.gz"

    maintainers("LydDeb")

    license("BSD-3-Clause")

    version("5.1.1", sha256="9b6dbf803cb5636397f0203d48541c0da8ba53babaf0e8a6feda2d88746813d4")
    version("3.4.1", sha256="fa9e50c4a03bede2a1d95dca620d661678484626858ccf388cf9671a0dd497a4")

    depends_on("py-setuptools@61.2:", when="@5.1.1", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", when="@5.1.1", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-idna", type=("build", "run"))
    depends_on("py-requests@2.1.0:", type=("build", "run"))
    depends_on("py-requests-file@1.4:", type=("build", "run"))
    depends_on("py-filelock@3.0.8:", type=("build", "run"))
