# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonBox(PythonPackage):
    """Advanced Python dictionaries with dot notation access

    Box will automatically make otherwise inaccessible keys safe to access as
    an attribute. You can always pass conversion_box=False to Box to disable
    that behavior. Also, all new dict and lists added to a Box or BoxList
    object are converted automatically."""

    homepage = "https://github.com/cdgriffith/Box"
    pypi = "python-box/python-box-5.3.0.tar.gz"

    license("MIT")

    version("5.3.0", sha256="4ed4ef5d34de505a65c01e3f1911de8cdb29484fcae0c035141dce535c6c194a")

    variant("extras", default=False, description='install the "extras" packages')

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-ruamel-yaml", when="+extras")
    depends_on("py-toml", when="+extras")
    depends_on("py-msgpack", when="+extras")
