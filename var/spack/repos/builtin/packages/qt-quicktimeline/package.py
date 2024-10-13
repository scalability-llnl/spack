# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtQuicktimeline(QtPackage):
    """Module for keyframe-based timeline construction."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    license("BSD-3-Clause")

    version("6.7.3", sha256="81ce374a22bf00d53d0a9d5293d6495a224137e9427e4d4913d87f2f0adc5a58")
    version("6.7.2", sha256="ad5370a3b193c5d30a824a1def0608e12fb735c4ff20ae55161a6f6e202e091d")
    version("6.7.1", sha256="98766368b4650eef583f76d257573e6785938b89c9eb2fc57577f4c199b12a1f")
    version("6.7.0", sha256="9c8d953d4dfbe2a42dbbd88c26b4b01f6caab4d525ec01eb66edc71e9ee39172")
    version("6.6.3", sha256="6dccea9ebc8a6507ffb046cada1dd339b8187923bb74b938f8ccdcb0a5590095")
    version("6.6.2", sha256="76e629f019f6bdd9d46efbde2704dfe104231879ad60eebd81d9585250aa618b")
    version("6.6.1", sha256="fe77555566bd6bb0ef0cb67b6ad09e225399fba3d2ec388de84e8a6200c0e2fc")
    version("6.6.0", sha256="06b94443da3f81153f04dca0cce781481462310d51f97d5550f81322a7a88cd0")
    version("6.5.3", sha256="fddd90cdb15af093673c6da924e18e22ebd364b9ab215356e1b40db28ac66640")
    version("6.5.2", sha256="96389af740fde3b2a655bf994001b94fd6e151ef84958ff9982e2ae799f1c3a2")
    version("6.5.1", sha256="d7d845f877f9b990e63ab14c9152f18e290611e760719a9c22f7740b91bd2ed1")
    version("6.5.0", sha256="ff862aad1aa4327c39c071ad1ca6eea6c64d4937521f9ed5d022a70cb3df92a7")
    version("6.4.3", sha256="e0f8f616a9c7d150dc73eccf7546ab4db041a05b85eafcb44b999cb41549dbed")
    version("6.4.2", sha256="af7449bf5954d2309081d6d65af7fd31cb11a5f8dc5f414163120d582f82353f")
    version("6.4.1", sha256="20450687941e6e12e1adf428114776c304d14447d61a4e8b08050c7c18463ee7")
    version("6.4.0", sha256="b5f88beaa726032141fab91b84bc3b268f6213518301c4ddcfa7d116fd08bdab")
    version("6.3.2", sha256="ca6e53a92b022b49098c15f2cc5897953644de8477310696542a03bbbe5666aa")
    version("6.3.1", sha256="ba1e808d4c0fce899c235942df34ae5d349632f61a302d14feeae7465cf1f197")
    version("6.3.0", sha256="09e27bbdefbbf50d15525d26119a00d86eba76d2d1bc9421557d1ed86edcacdf")
    version("6.2.4", sha256="d73cb33e33f0b7a1825b863c22e6b552ae86aa841bcb805a41aca02526a4e8bc")
    version("6.2.3", sha256="bbb913398d8fb6b5b20993b5e02317de5c1e4b23a5357dd5d08a237ada6cc7e2")

    depends_on("cxx", type="build")  # generated

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)
