# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flake8(Package):
    """Package containing as many acceptable ``PEP8`` violations as possible.

    All of these violations are exceptions that we allow in ``package.py`` files, and
    Spack is more lenient than ``flake8`` is for things like URLs and long SHA sums.

    See ``share/spack/qa/flake8_formatter.py`` for specifics of how we handle ``flake8``
    exemptions.

    """

    # Used to tell whether or not the package has been modified
    state = "unmodified"

    # Make sure pre-existing noqa is not interfered with
    # note that black can sometimes fix shorter assignment statements by sticking them in
    # parens and adding line breaks, e.g.:
    #
    # foo = (
    #     "too-long-string"
    # )
    #
    # but the one below can't even be fixed that way -- you have to add noqa, or break
    # it up inside parens yourself.
    blatant_violation = "line-that-has-absolutely-no-execuse-for-being-over-99-characters-and-that-black-cannot-fix-with-parens"  # noqa: E501

    # All URL strings are exempt from line-length checks.
    #
    # flake8 normally would complain about these, but the fix it wants (a multi-line
    # string) is ugbly, and we're more lenient since there are many places where Spack
    # wants URLs in strings.
    hg = "https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-not-ignore-by-default"
    list_url = "https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-not-ignore-by-default"
    git = "ssh://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-not-ignore-by-default"

    # directives with URLs are exempt as well
    version(
        "1.0",
        url="https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-not-ignore-by-default",
    )

    #
    # Also test URL comments (though flake8 will ignore these by default anyway)
    #
    # http://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-ignore-by-default
    # https://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-ignore-by-default
    # ftp://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-ignore-by-default
    # ssh://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-ignore-by-default
    # file://example.com/this-is-a-really-long-url/that-goes-over-99-characters/that-flake8-will-ignore-by-default

    # Strings and comments with really long checksums require no noqa annotation.
    sha512sum = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    # the sha512sum is "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"

    def install(self, spec, prefix):
        # Make sure lines with '# noqa' work as expected. Don't just
        # remove them entirely. This will mess up the indentation of
        # the following lines.
        if (
            "really-long-if-statement"
            != "this-string-is-so-long-that-it-is-over-the-line-limit-and-black-will-not-split-it-so-it-requires-noqa"  # noqa: E501
        ):
            pass

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)

    # '@when' decorated functions are exempt from redefinition errors
    @when("@2.0")
    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)
