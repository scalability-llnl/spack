# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtShadertools(QtPackage):
    """APIs and tools in this module provide the producer functionality for the
    shader pipeline that allows Qt Quick to operate on Vulkan, Metal, and
    Direct3D, in addition to OpenGL."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    license("BSD-3-Clause")

    version("6.7.3", sha256="8ec6a48c41d49b6f9595659169b2c69aecd46e96a88131f19f6a4cda394fa3f4")
    version("6.7.2", sha256="256ff8199d9f6e97bef57f602c5fa7a32e3c7588bf7efe39e412b810c7ed4ffc")
    version("6.7.1", sha256="56cfba20c7e8f7a218cac68d237a63ea342ac9a67211ecdf3c7152572632448b")
    version("6.7.0", sha256="82d9ef04a470db30e90253ddc72fcbc8fea2ecad419a735ecf64bb965560197f")
    version("6.6.3", sha256="a0e44248cec9011166794da895952cc1f98ddbfa77180174da925c5f749391a8")
    version("6.6.2", sha256="c6d06a660779990f69b8b2e21eb01ada784f9144cbaeb718ee0da01c33ce2141")
    version("6.6.1", sha256="1206110464f8829e34ca7277bdcd2044e96a98078c9ab9f8b96ed526a4d81526")
    version("6.6.0", sha256="8b34908f8bbc7fb00a00babede91dbbeec9826f5138d390041f239d483e1162a")
    version("6.5.3", sha256="e6c627763db8c60799218947443efb90fb3511342f2212f5e99cd98f6942ed08")
    version("6.5.2", sha256="2b14cf982753f19cf48a4780bc7d96d8fc0ad3ed1049ae5d3292fc5fc1fd6aef")
    version("6.5.1", sha256="642bf97498d54b4471bf4cc227709c6b676dbd520765f82b0749a2b4ef833d25")
    version("6.5.0", sha256="ef2c71fac111a837914b7dc2b46c26579ea50b05fbd60022d430da88bdb211cb")
    version("6.4.3", sha256="a018883e889540ab828db0b0b49a3c5d810dd7283bb84abf43d1622daf474f7d")
    version("6.4.2", sha256="7f29a78769f454fe529595acb693aa67812e80d894162ddad3f0444f65a22268")
    version("6.4.1", sha256="d325724c4ed79c759ac8cbbca5f9fd4b0e6e8d61a9ac58921cb1dac75c104687")
    version("6.4.0", sha256="51bf312965bd673193221cd49019f504feb79c0bf0ff01d6a6ca5c8d15f9d7c1")
    version("6.3.2", sha256="ec73303e6c91cddae402b1ac0d18a0d35619f348785514be30cec2791cd63faa")
    version("6.3.1", sha256="1b8b18b6ece4d92d0bf60a3b2a9924b45c369968cc77217796434ac7c5c6628f")
    version("6.3.0", sha256="3c36d83fc036a144722ce056b2840260005dcbd338e11b9c527d7266a54afd45")
    version("6.2.4", sha256="c3332d91e0894086634d5f8d40638439e6e3653a3a185e1b5f5d23ae3b9f51a1")
    version("6.2.3", sha256="658c4acc2925e57d35bbd38cdf49c08297555ed7d632f9e86bfef76e6d861562")

    depends_on("cxx", type="build")  # generated

    depends_on("qt-base +gui")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
