# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAse(PythonPackage):
    """The Atomic Simulation Environment (ASE) is a set of tools
    and Python modules for setting up, manipulating, running,
    visualizing and analyzing atomistic simulations."""

    homepage = "https://wiki.fysik.dtu.dk/ase/"
    pypi = "ase/ase-3.13.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.23.0", sha256="91a2aa31d89bd90b0efdfe4a7e84264f32828b2abfc9f38e65e041ad76fec8ae")
    version("3.21.1", sha256="78b01d88529d5f604e76bc64be102d48f058ca50faad72ac740d717545711c7b")
    version("3.21.0", sha256="2c561e9b767cf16fc8ce198ea9326d77c6b67d33a85f44b68455e23466a64608")
    version("3.20.1", sha256="72c81f21b6adb907595fce8d883c0231301cbd8e9f6e5ce8e98bab927054daca")
    version("3.19.3", sha256="27c378b983dfacd49398236e7232c28590c218c31bb2205695818552c772bc4b")
    version("3.19.2", sha256="89446a3d194d90f0758f0c7248a5095a5a05a16f2a0f7d53db4d3103ca516e62")
    version("3.19.1", sha256="839029ed5ad9590b40c74773b9aef4733bfd9f8300cf998011584cad6ebdbf0f")
    version("3.19.0", sha256="a8378ab57e91cfe1ba09b3639d8409bb7fc1a40b59479c7822d206e673ad93f9")
    version("3.18.2", sha256="3930a561380dc3e4aa97f013933e68f858349abf9b4dbb0a035a4f2107b37ba4")
    version("3.18.1", sha256="e21948dbf79011cc796d772885a8aafb255a6f365d112fe6a3bd26198c6cac7f")
    version("3.18.0", sha256="39d45f12def2669605bffc82926acfb13a0d0610e6d82740fa316aafa70f97f9")
    version("3.15.0", sha256="5e22d961b1311ef4ba2d83527f7cc7448abac8cf9bddd1593bee548459263fe8")
    version("3.13.0", sha256="c4046c50debac28415b36616d79aa28e68ae2cd03c013c2aed6a1e3d465c0ee1")

    depends_on("python@2.6:", type=("build", "run"), when="@:3.15.0")
    depends_on("python@3.5:", type=("build", "run"), when="@3.18.0:")
    depends_on("python@3.6:", type=("build", "run"), when="@3.20.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@3.23.0:")
    depends_on("py-numpy@1.11.3:", type=("build", "run"))
    depends_on("py-numpy@1.18.5:", type=("build", "run"), when="@3.23.0:")
    depends_on("py-matplotlib@2.0.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.3.4:", type=("build", "run"), when="@3.23.0:")
    depends_on("py-scipy@0.18.1:", type=("build", "run"))
    depends_on("py-scipy@1.6.0:", type=("build", "run"), when="@3.23.0:")
    depends_on("py-flask", type=("build", "run"), when="@:3.18.0")
    depends_on("py-setuptools", type="build")
