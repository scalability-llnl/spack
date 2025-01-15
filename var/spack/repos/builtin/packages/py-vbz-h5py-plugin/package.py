# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVbzH5pyPlugin(PythonPackage):
    """
    This module provides a plugin to H5Py for the VBZ (de)compression library.
    """

    homepage = "https://github.com/nanoporetech/vbz_compression"
    pypi = "vbz_h5py_plugin/vbz_h5py_plugin-1.0.1.tar.gz"

    maintainers("Pandapip1")

    license("MPL-2.0", checked_by="Pandapip1")

    version("1.0.1", sha256="c784458bb0aad6303474cb2f10956179116b35555803fd1154eb4ef362519341")

    depends_on("py-setuptools@61.0:", type="build")

    depends_on("py-h5py", type=("build", "run"))
