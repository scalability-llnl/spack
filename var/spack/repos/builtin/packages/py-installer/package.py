# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyInstaller(Package, PythonExtension):
    """A library for installing Python wheels."""

    homepage = "https://github.com/pypa/installer"
    url = (
        "https://files.pythonhosted.org/packages/py3/i/installer/installer-0.6.0-py3-none-any.whl"
    )
    list_url = "https://pypi.org/simple/installer/"

    version("0.7.0", sha256="05d1933f0a5ba7d8d6296bb6d5018e7c94fa473ceb10cf198a92ccea19c27b53")
    version("0.6.0", sha256="ae7c62d1d6158b5c096419102ad0d01fdccebf857e784cee57f94165635fe038")

    extends("python")

    def install(self, spec, prefix):
        # To build and install installer from source, you need flit-core, build, and installer
        # already installed. We get around this by using a pre-built wheel to install itself.
        # See https://github.com/pypa/installer/issues/150 for details.

        # We can't do this in setup_build_environment because self.stage.archive_file is undefined
        wheel = self.stage.archive_file
        path = os.environ.get("PYTHONPATH", "")
        os.environ["PYTHONPATH"] = os.pathsep.join([wheel, path])

        args = ["-m", "installer", "--prefix", prefix, wheel]
        python(*args)

    def setup_dependent_package(self, module, dependent_spec):
        setattr(module, "installer", python.with_default_args("-m", "installer"))
