# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyParsley(PythonPackage):
    """Parsing and pattern matching made easy."""

    homepage = "https://launchpad.net/parsley"
    pypi = "Parsley/Parsley-1.3.tar.gz"

    license("MIT")

    version("1.3", sha256="9444278d47161d5f2be76a767809a3cbe6db4db822f46a4fd7481d4057208d41")

    depends_on("py-setuptools", type="build")
