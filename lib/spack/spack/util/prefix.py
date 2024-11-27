# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains utilities for managing the installation prefix of a package.
"""
import os
from typing import Dict


class Prefix(str):
    """This class represents an installation prefix, but provides useful attributes for referring
    to directories inside the prefix.

    Attributes of this object are created on the fly when you request them, so any of the following
    are valid:

    >>> prefix = Prefix("/usr")
    >>> prefix.bin
    /usr/bin
    >>> prefix.lib64
    /usr/lib64
    >>> prefix.share.man
    /usr/share/man
    >>> prefix.foo.bar.baz
    /usr/foo/bar/baz
    >>> prefix.join("dashed-directory").bin64
    /usr/dashed-directory/bin64

    Prefix objects behave identically to strings. In fact, they subclass ``str``, so operators like
    ``+`` are legal::

        print("foobar " + prefix)

    This prints ``foobar /usr``. All of this is meant to make custom installs easy.
    """

    def __getattr__(self, name: str) -> "Prefix":
        """Concatenate a string to a prefix.

        Useful for strings that are valid variable names.

        Args:
            name: the string to append to the prefix

        Returns:
            the newly created installation prefix
        """
        return Prefix(os.path.join(self, name))

    def join(self, string: str) -> "Prefix":  # type: ignore[override]
        """Concatenate a string to a prefix.

        Useful for strings that are not valid variable names. This includes strings containing
        characters like ``-`` and ``.``.

        Args:
            string: the string to append to the prefix

        Returns:
            the newly created installation prefix
        """
        return Prefix(os.path.join(self, string))

    def __getstate__(self) -> Dict[str, str]:
        """Control how object is pickled.

        Returns:
            current state of the object
        """
        return self.__dict__

    def __setstate__(self, state: Dict[str, str]) -> None:
        """Control how object is unpickled.

        Args:
            new state of the object
        """
        self.__dict__.update(state)
