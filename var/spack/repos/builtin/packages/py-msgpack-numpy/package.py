# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMsgpackNumpy(PythonPackage):
    """This package provides encoding and decoding routines
    that enable the serialization and deserialization of
    numerical and array data types provided by numpy using the
    highly efficient msgpack format. Serialization of Python's
    native complex data types is also supported."""

    homepage = "https://github.com/lebedov/msgpack-numpy"
    pypi = "msgpack-numpy/msgpack-numpy-0.4.7.1.tar.gz"

    license("BSD-3-Clause")

    version("0.4.7.1", sha256="7eaf51acf82d7c467d21aa71df94e1c051b2055e54b755442051b474fa7cf5e1")
    version("0.4.7", sha256="8e975dd7dd9eb13cbf5e8cd90af1f12af98706bbeb7acfcbd8d558fd005a85d7")
    version("0.4.6", sha256="ef3c5fe3d6cbab5c9db97de7062681c18f82d32a37177aaaf58b483d0336f135")
    version("0.4.5", sha256="4e88a4147db70f69dce1556317291e04e5107ee7b93ea300f92f1187120da7ec")
    version("0.4.4.3", sha256="c7db37ce01e268190568cf66a6a65d1ad81e3bcfa55dd824103c9b324608a44e")
    version("0.4.4.2", sha256="ac3db232710070ac64d8e1c5123550a1c1fef45d77b6789d2170cbfd2ec711f3")
    version("0.4.4.1", sha256="b7641ccf9f0f4e91a533e8c7be5e34d3f12ff877480879b252113d65c510eeef")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.9:", type=("build", "run"))
    depends_on("py-msgpack@0.5.2:", type=("build", "run"))
