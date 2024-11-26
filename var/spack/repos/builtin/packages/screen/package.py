# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Screen(AutotoolsPackage, GNUMirrorPackage):
    """Screen is a full-screen window manager that multiplexes a physical
    terminal between several processes, typically interactive shells.
    """

    homepage = "https://www.gnu.org/software/screen/"
    gnu_mirror_path = "screen/screen-4.3.1.tar.gz"

    license("GPL-3.0-or-later")

    version("4.9.1", sha256="26cef3e3c42571c0d484ad6faf110c5c15091fbf872b06fa7aa4766c7405ac69")
    version("4.9.0", sha256="f9335281bb4d1538ed078df78a20c2f39d3af9a4e91c57d084271e0289c730f4")
    version("4.8.0", sha256="6e11b13d8489925fde25dfb0935bf6ed71f9eb47eff233a181e078fde5655aa1")
    version("4.6.2", sha256="1b6922520e6a0ce5e28768d620b0f640a6631397f95ccb043b70b91bb503fa3a")
    version("4.3.1", sha256="fa4049f8aee283de62e283d427f2cfd35d6c369b40f7f45f947dbfd915699d63")
    version("4.3.0", sha256="5164e89bcc60d7193177e6e02885cc42411d1d815c839e174fb9abafb9658c46")
    version("4.2.1", sha256="5468545047e301d2b3579f9d9ce00466d14a7eec95ce806e3834a3d6b0b9b080")
    version("4.2.0", sha256="7dc1b7a3e7669eefe7e65f32e201704d7a11cc688244fcf71757f7792a5ff413")
    version("4.0.3", sha256="78f0d5b1496084a5902586304d4a73954b2bfe33ea13edceecf21615c39e6c77")
    version("4.0.2", sha256="05d087656d232b38c82379dfc66bf526d08e75e1f4c626acea4a2dda1ebcc845")
    version("3.9.15", sha256="11ea131c224fa759feee3bc6ee2e3d6915a97d2d6da46db968dc24b41de054db")
    version("3.9.11", sha256="f0d6d2eae538688766381c1658e3d4a64c8b4afb3682c2bb33ce96edc840a261")
    version("3.9.10", sha256="3e8df4e1888e59267c37d2a24fa8365cd4d2081392f719579a347a2c6d1386a8")
    version("3.9.9", sha256="8e40931ee93387c6897307419befb9d9c39bf66cd42261231f6160ef6c54dccb")
    version("3.9.8", sha256="7c0593b5eec5191897e4293832cece08e4cbf362a2cf056d7d30e22727e7156b")
    version("3.9.4", sha256="a3d84f7e2ae97e6264a52bcc7e0717bc9cf6bb9dbbab8d1acd1e78eb35233f42")
    version("3.7.6", sha256="f30251dec5e23fac0d77922b5064e0b4db6d4d22a2a6534ebe4f3bae5ce22523")
    version("3.7.4", sha256="65d33ad60c7e18f0c527654574ba1e630a8d4da106f377264a0ec3fa953d22cf")
    version("3.7.2", sha256="6a882385d2810b8220b9e03c75c5fa184dcbd1afdb95974bbac396bb749a6cc0")
    version("3.7.1", sha256="0cd5b1a2cbba6bb2f2bc2145aec650abf02541fd3a2071117a99e4982f6e01da")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")
    depends_on("autoconf", type="build", when="@4.9.0:")
    depends_on("automake", type="build", when="@4.9.0:")
    depends_on("libtool", type="build", when="@4.9.0:")
