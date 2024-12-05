# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRefgenie(PythonPackage):
    """Refgenie manages storage, access, and transfer of reference genome resources."""

    homepage = "http://refgenie.databio.org"
    pypi = "refgenie/refgenie-0.12.1.tar.gz"

    license("BSD-2-Clause")

    version("0.12.1", sha256="cfd007ed0981e00d019deb49aaea896952341096494165cb8378488850eec451")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-logmuse@0.2.6:", type=("build", "run"))
    depends_on("py-piper@0.12.1:", type=("build", "run"))
    depends_on("py-pyfaidx@0.5.5.2:", type=("build", "run"))
    depends_on("py-refgenconf@0.12.2:", type=("build", "run"))
    depends_on("py-yacman@0.8.3:", type=("build", "run"))
