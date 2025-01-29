# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyfilechooser(PythonPackage):
    """Python file chooser widget for use in Jupyter/IPython in conjunction with ipywidgets."""

    homepage = "https://github.com/crahan/ipyfilechooser"
    pypi = "ipyfilechooser/ipyfilechooser-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="41df9e4395a924f8e1b78e2804dbe5066dc3fdc233fb07fecfcdc2a0c9a7d8d3")

    depends_on("py-setuptools", type="build")
    depends_on("py-ipywidgets", type=("build", "run"))
