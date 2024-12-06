# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyArgparseDataclass(PythonPackage):
    """An immutable mapping type for Python."""

    homepage = "https://github.com/mivade/argparse_dataclass"
    pypi = "argparse_dataclass/argparse_dataclass-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="09ab641c914a2f12882337b9c3e5086196dbf2ee6bf0ef67895c74002cc9297f")

    depends_on("py-setuptools", type="build")
