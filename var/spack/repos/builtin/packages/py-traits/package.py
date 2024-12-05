# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTraits(PythonPackage):
    """Observable typed attributes for Python classes."""

    homepage = "https://docs.enthought.com/traits"
    pypi = "traits/traits-6.0.0.tar.gz"
    git = "https://github.com/enthought/traits.git"

    license("CC-BY-3.0")

    version("6.4.2", sha256="5be7cc5fb7a99cba7e9014786373e3ad2f75efb445eeced094654bbaf3b0fa82")
    version("6.4.1", sha256="78bb2ccafd60aff606515aac46de64668a0a81cb5c54c650b9877a841aa9e812")
    version("6.3.1", sha256="ebdd9b067a262045840a85e3ff34e1567ce4e9b6548c716cdcc82b5884ed9100")
    version("6.2.0", sha256="16fa1518b0778fd53bf0547e6a562b1787bf68c8f6b7995a13bd1902529fdb0c")
    version("6.0.0", sha256="dbcd70166feca434130a1193284d5819ca72ffbc8dbce8deeecc0cebb41a3bfb")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
