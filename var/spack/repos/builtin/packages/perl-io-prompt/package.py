# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoPrompt(PerlPackage):
    """By default, this module exports a single function prompt. It prompts the
    user to enter some input, and returns an object that represents the user
    input.

    You may specify various flags to the function to affect its behaviour; most
    notably, it defaults to automatically chomp the input, unless the -line
    flag is specified.

    Two other functions are exported at request: hand_print, which simulates
    hand-typing to the console; and get_input, which is the lower-level
    function that actually prompts the user for a suitable input.

    Note that this is an interim re-release. A full release with better
    documentation will follow in the near future. Meanwhile, please consult the
    examples directory from this module's CPAN distribution to better
    understand how to make use of this module."""

    homepage = "https://metacpan.org/pod/IO::Prompt"
    url = "https://cpan.metacpan.org/authors/id/D/DC/DCONWAY/IO-Prompt-0.997004.tar.gz"

    version("0.997004", sha256="f17bb305ee6ac8b5b203e6d826eb940c4f3f6d6f4bfe719c3b3a225f46f58615")

    depends_on("perl-module-build", type="build")

    depends_on("perl-termreadkey", type=("build", "run"))
    depends_on("perl-want", type=("build", "run"))
