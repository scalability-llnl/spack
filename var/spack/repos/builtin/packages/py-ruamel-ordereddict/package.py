# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRuamelOrdereddict(PythonPackage):
    """This is an implementation of an ordered dictionary with Key Insertion
    Order (KIO: updates of values do not affect the position of the key), Key
    Value Insertion Order (KVIO, an existing key's position is removed and put
    at the back). The standard library module OrderedDict, implemented later,
    implements a subset of ordereddict functionality."""

    homepage = "https://sourceforge.net/projects/ruamel-ordereddict/"
    pypi = "ruamel.ordereddict/ruamel.ordereddict-0.4.14.tar.gz"

    license("MIT")

    version("0.4.14", sha256="281051d26eb2b18ef3d920e1e260716a52bd058a6b1a2f324102fc6a15cb8d4a")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
