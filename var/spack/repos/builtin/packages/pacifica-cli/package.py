# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PacificaCli(PythonPackage):
    """Python CLI for Pacifica Core Services"""

    homepage = "https://github.com/pacifica/pacifica-cli/"
    pypi = "pacifica-cli/pacifica-cli-0.5.2.tar.gz"

    license("LGPL-3.0-only")

    version("0.5.2", sha256="fee5fa8ac38ffec2e9199bff23afbbae697c4f7554f13e340104f8b20a62843f")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-pacifica-uploader@0.3.1:", type=("build", "run"))
    depends_on("py-pacifica-downloader@0.4.1:", type=("build", "run"))
    depends_on("py-pacifica-namespace", type=("build", "run"))
    depends_on("py-pager", type=("build", "run"))
