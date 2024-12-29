# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGleanParser(PythonPackage):
    """Parser tools for Mozilla's Glean telemetry."""

    homepage = "https://mozilla.github.io/glean_parser/"
    pypi = "glean_parser/glean_parser-14.3.0.tar.gz"

    license("MPL-2.0", checked_by="teaguesterling")

    version("14.3.0", sha256="b48d643029fb824b0b76adb2b4a00e88a49de4ec479ac9c5add52c511e9be481")
    version("14.0.1", sha256="3e9e5f99ad8592300e364b70d6247b21c445774a73a2ad274677fb58a0065809")

    depends_on("py-appdirs@1.4:")
    depends_on("py-click@7:")
    depends_on("py-diskcache@4:")
    depends_on("py-jinja2@2.10.1:")
    depends_on("py-jsonschema@3.0.2:")
    depends_on("py-pyyaml@5.3.1:")
    depends_on("py-pytest-runner", type="build")
    depends_on("py-setuptools-scm@7:", type="build")
