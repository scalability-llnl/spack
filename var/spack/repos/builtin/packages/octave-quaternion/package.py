# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveQuaternion(OctavePackage, SourceforgePackage):
    """Quaternion package for GNU Octave,
    includes a quaternion class with overloaded operators."""

    homepage = "https://octave.sourceforge.io/quaternion/"
    sourceforge_mirror_path = "octave/quaternion-2.4.0.tar.gz"

    license("GPL-3.0-or-later")

    version("2.4.0", sha256="4c2d4dd8f1d213f080519c6f9dfbbdca068087ee0411122b16e377e0f4641610")
    version("2.2.2", sha256="261d51657bc729c8f9fe915532d91e75e48dce2af2b298781e78cc93a5067cbd")

    conflicts("^octave@6:")
    extends("octave@3.8.0:5.2.0")
