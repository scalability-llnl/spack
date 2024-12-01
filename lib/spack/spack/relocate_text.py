# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains pure-Python classes and functions for replacing
paths inside text files and binaries."""

import re
from collections import OrderedDict
from typing import Dict, Union

import spack.error

Prefix = Union[str, bytes]


def encode_path(p: Prefix) -> bytes:
    return p if isinstance(p, bytes) else p.encode("utf-8")


def _prefix_to_prefix_as_bytes(prefix_to_prefix) -> Dict[bytes, bytes]:
    return OrderedDict((encode_path(k), encode_path(v)) for (k, v) in prefix_to_prefix.items())


def utf8_path_to_binary_regex(prefix: str):
    """Create a binary regex that matches the input path in utf8"""
    prefix_bytes = re.escape(prefix).encode("utf-8")
    return re.compile(b"(?<![\\w\\-_/])([\\w\\-_]*?)%s([\\w\\-_/]*)" % prefix_bytes)


def _byte_strings_to_single_binary_regex(prefixes):
    all_prefixes = b"|".join(re.escape(p) for p in prefixes)
    return re.compile(b"(?<![\\w\\-_/])([\\w\\-_]*?)(%s)([\\w\\-_/]*)" % all_prefixes)


def utf8_paths_to_single_binary_regex(prefixes):
    """Create a (binary) regex that matches any input path in utf8"""
    return _byte_strings_to_single_binary_regex(p.encode("utf-8") for p in prefixes)


def filter_identity_mappings(prefix_to_prefix):
    """Drop mappings that are not changed."""
    # NOTE: we don't guard against the following case:
    # [/abc/def -> /abc/def, /abc -> /x] *will* be simplified to
    # [/abc -> /x], meaning that after this simplification /abc/def will be
    # mapped to /x/def instead of /abc/def. This should not be a problem.
    return OrderedDict((k, v) for (k, v) in prefix_to_prefix.items() if k != v)


class PrefixReplacer:
    """Base class for applying a prefix to prefix map
    to a list of binaries or text files.
    Child classes implement _apply_to_file to do the
    actual work, which is different when it comes to
    binaries and text files."""

    def __init__(self, prefix_to_prefix: Dict[bytes, bytes]):
        """
        Arguments:

            prefix_to_prefix (OrderedDict):

                A ordered mapping from prefix to prefix. The order is
                relevant to support substring fallbacks, for example
                [("/first/sub", "/x"), ("/first", "/y")] will ensure
                /first/sub is matched and replaced before /first.
        """
        self.prefix_to_prefix = filter_identity_mappings(prefix_to_prefix)

    @property
    def is_noop(self) -> bool:
        """Returns true when the prefix to prefix map
        is mapping everything to the same location (identity)
        or there are no prefixes to replace."""
        return not self.prefix_to_prefix

    def apply(self, filenames: list):
        """Returns a list of files that were modified"""
        changed_files = []
        if self.is_noop:
            return []
        for filename in filenames:
            if self.apply_to_filename(filename):
                changed_files.append(filename)
        return changed_files

    def apply_to_filename(self, filename):
        if self.is_noop:
            return False
        with open(filename, "rb+") as f:
            return self.apply_to_file(f)

    def apply_to_file(self, f):
        if self.is_noop:
            return False
        return self._apply_to_file(f)


class TextFilePrefixReplacer(PrefixReplacer):
    """This class applies prefix to prefix mappings for relocation
    on text files.

    Note that UTF-8 encoding is assumed."""

    def __init__(self, prefix_to_prefix: Dict[bytes, bytes]):
        """
        prefix_to_prefix (OrderedDict): OrderedDictionary where the keys are
            bytes representing the old prefixes and the values are the new.
        """
        super().__init__(prefix_to_prefix)
        # Single regex for all paths.
        self.regex = _byte_strings_to_single_binary_regex(self.prefix_to_prefix.keys())

    @classmethod
    def from_strings_or_bytes(
        cls, prefix_to_prefix: Dict[Prefix, Prefix]
    ) -> "TextFilePrefixReplacer":
        """Create a TextFilePrefixReplacer from an ordered prefix to prefix map."""
        return cls(_prefix_to_prefix_as_bytes(prefix_to_prefix))

    def _apply_to_file(self, f):
        """Text replacement implementation simply reads the entire file
        in memory and applies the combined regex."""
        replacement = lambda m: m.group(1) + self.prefix_to_prefix[m.group(2)] + m.group(3)
        data = f.read()
        new_data = re.sub(self.regex, replacement, data)
        if id(data) == id(new_data):
            return False
        f.seek(0)
        f.write(new_data)
        f.truncate()
        return True


class BinaryFilePrefixReplacer(PrefixReplacer):
    def __init__(self, prefix_to_prefix, suffix_safety_size=7):
        """
        prefix_to_prefix (OrderedDict): OrderedDictionary where the keys are
            bytes representing the old prefixes and the values are the new
        suffix_safety_size (int): in case of null terminated strings, what size
            of the suffix should remain to avoid aliasing issues?
        """
        assert suffix_safety_size >= 0
        super().__init__(prefix_to_prefix)
        self.suffix_safety_size = suffix_safety_size
        self.regex = self.binary_text_regex(self.prefix_to_prefix.keys(), suffix_safety_size)

    @classmethod
    def binary_text_regex(cls, binary_prefixes, suffix_safety_size=7):
        """
        Create a regex that looks for exact matches of prefixes, and also tries to
        match a C-string type null terminator in a small lookahead window.

        Arguments:
            binary_prefixes (list): List of byte strings of prefixes to match
            suffix_safety_size (int): Sizeof the lookahed for null-terminated string.

        Returns: compiled regex
        """
        return re.compile(
            b"("
            + b"|".join(re.escape(p) for p in binary_prefixes)
            + b")([^\0]{0,%d}\0)?" % suffix_safety_size
        )

    @classmethod
    def from_strings_or_bytes(
        cls, prefix_to_prefix: Dict[Prefix, Prefix], suffix_safety_size: int = 7
    ) -> "BinaryFilePrefixReplacer":
        """Create a BinaryFilePrefixReplacer from an ordered prefix to prefix map.

        Arguments:
            prefix_to_prefix (OrderedDict): Ordered mapping of prefix to prefix.
            suffix_safety_size (int): Number of bytes to retain at the end of a C-string
                to avoid binary string-aliasing issues.
        """
        return cls(_prefix_to_prefix_as_bytes(prefix_to_prefix), suffix_safety_size)

    def _apply_to_file(self, f):
        """
        Given a file opened in rb+ mode, apply the string replacements as
        specified by an ordered dictionary of prefix to prefix mappings. This
        method takes special care of null-terminated C-strings. C-string constants
        are problematic because compilers and linkers optimize readonly strings for
        space by aliasing those that share a common suffix (only suffix since all
        of them are null terminated). See https://github.com/spack/spack/pull/31739
        and https://github.com/spack/spack/pull/32253 for details. Our logic matches
        the original prefix with a ``suffix_safety_size + 1`` lookahead for null bytes.
        If no null terminator is found, we simply pad with leading /, assuming that
        it's a long C-string; the full C-string after replacement has a large suffix
        in common with its original value.
        If there *is* a null terminator we can do the same as long as the replacement
        has a sufficiently long common suffix with the original prefix.
        As a last resort when the replacement does not have a long enough common suffix,
        we can try to shorten the string, but this only works if the new length is
        sufficiently short (typically the case when going from large padding -> normal path)
        If the replacement string is longer, or all of the above fails, we error out.

        Arguments:
            f: file opened in rb+ mode

        Returns:
            bool: True if file was modified
        """
        assert f.tell() == 0

        # We *could* read binary data in chunks to avoid loading all in memory,
        # but it's nasty to deal with matches across boundaries, so let's stick to
        # something simple.

        modified = True

        for match in self.regex.finditer(f.read()):
            # The matching prefix (old) and its replacement (new)
            old = match.group(1)
            new = self.prefix_to_prefix[old]

            # Did we find a trailing null within a N + 1 bytes window after the prefix?
            null_terminated = match.end(0) > match.end(1)

            # Suffix string length, excluding the null byte
            # Only makes sense if null_terminated
            suffix_strlen = match.end(0) - match.end(1) - 1

            # How many bytes are we shrinking our string?
            bytes_shorter = len(old) - len(new)

            # We can't make strings larger.
            if bytes_shorter < 0:
                raise CannotGrowString(old, new)

            # If we don't know whether this is a null terminated C-string (we're looking
            # only N + 1 bytes ahead), or if it is and we have a common suffix, we can
            # simply pad with leading dir separators.
            elif (
                not null_terminated
                or suffix_strlen >= self.suffix_safety_size  # == is enough, but let's be defensive
                or old[-self.suffix_safety_size + suffix_strlen :]
                == new[-self.suffix_safety_size + suffix_strlen :]
            ):
                replacement = b"/" * bytes_shorter + new

            # If it *was* null terminated, all that matters is that we can leave N bytes
            # of old suffix in place. Note that > is required since we also insert an
            # additional null terminator.
            elif bytes_shorter > self.suffix_safety_size:
                replacement = new + match.group(2)  # includes the trailing null

            # Otherwise... we can't :(
            else:
                raise CannotShrinkCString(old, new, match.group()[:-1])

            f.seek(match.start())
            f.write(replacement)
            modified = True

        return modified


class BinaryStringReplacementError(spack.error.SpackError):
    def __init__(self, file_path, old_len, new_len):
        """The size of the file changed after binary path substitution

        Args:
            file_path (str): file with changing size
            old_len (str): original length of the file
            new_len (str): length of the file after substitution
        """
        super().__init__(
            "Doing a binary string replacement in %s failed.\n"
            "The size of the file changed from %s to %s\n"
            "when it should have remanined the same." % (file_path, old_len, new_len)
        )


class BinaryTextReplaceError(spack.error.SpackError):
    def __init__(self, msg):
        msg += (
            " To fix this, compile with more padding "
            "(config:install_tree:padded_length), or install to a shorter prefix."
        )
        super().__init__(msg)


class CannotGrowString(BinaryTextReplaceError):
    def __init__(self, old, new):
        msg = "Cannot replace {!r} with {!r} because the new prefix is longer.".format(old, new)
        super().__init__(msg)


class CannotShrinkCString(BinaryTextReplaceError):
    def __init__(self, old, new, full_old_string):
        # Just interpolate binary string to not risk issues with invalid
        # unicode, which would be really bad user experience: error in error.
        # We have no clue if we actually deal with a real C-string nor what
        # encoding it has.
        msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
            old, new, full_old_string
        )
        super().__init__(msg)
