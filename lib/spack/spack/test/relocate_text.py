# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io
from collections import OrderedDict

import pytest

import spack.relocate_text as relocate_text


def test_text_relocation_regex_is_safe():
    # Test whether prefix regex is properly escaped
    string = b"This does not match /a/, but this does: /[a-z]/."
    assert relocate_text.utf8_path_to_binary_regex("/[a-z]/").search(string).group(0) == b"/[a-z]/"


def test_utf8_paths_to_single_binary_regex():
    regex = relocate_text.utf8_paths_to_single_binary_regex(
        ["/first/path", "/second/path", "/safe/[a-z]"]
    )
    # Match nothing
    assert not regex.search(b"text /neither/first/path text /the/second/path text")

    # Match first
    string = b"contains both /first/path/subdir and /second/path/sub"
    assert regex.search(string).group(0) == b"/first/path/subdir"

    # Match second
    string = b"contains both /not/first/path/subdir but /second/path/subdir"
    assert regex.search(string).group(0) == b"/second/path/subdir"

    # Match "unsafe" dir name
    string = b"don't match /safe/a/path but do match /safe/[a-z]/file"
    assert regex.search(string).group(0) == b"/safe/[a-z]/file"


def test_ordered_replacement():
    # This tests whether binary text replacement respects order, so that
    # a long package prefix is replaced before a shorter sub-prefix like
    # the root of the spack store (as a fallback).
    def replace_and_expect(prefix_map, before, after=None, suffix_safety_size=7):
        f = io.BytesIO(before)
        relocater = relocate_text.BinaryFilePrefixReplacer(
            OrderedDict(prefix_map), suffix_safety_size
        )
        relocater.apply_to_file(f)
        f.seek(0)
        assert f.read() == after

    # The case of having a non-null terminated common suffix.
    replace_and_expect(
        [
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
            (b"/old-spack/opt", b"/sec/spack/opt"),
        ],
        b"Binary with /old-spack/opt/specific-package and /old-spack/opt",
        b"Binary with /////////first/specific-package and /sec/spack/opt",
        suffix_safety_size=7,
    )

    # The case of having a direct null terminated common suffix.
    replace_and_expect(
        [
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
            (b"/old-spack/opt", b"/sec/spack/opt"),
        ],
        b"Binary with /old-spack/opt/specific-package\0 and /old-spack/opt\0",
        b"Binary with /////////first/specific-package\0 and /sec/spack/opt\0",
        suffix_safety_size=7,
    )

    # Testing the order of operations (not null terminated, long enough common suffix)
    replace_and_expect(
        [
            (b"/old-spack/opt", b"/s/spack/opt"),
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
        ],
        b"Binary with /old-spack/opt/specific-package and /old-spack/opt",
        b"Binary with ///s/spack/opt/specific-package and ///s/spack/opt",
        suffix_safety_size=7,
    )

    # Testing the order of operations (null terminated, long enough common suffix)
    replace_and_expect(
        [
            (b"/old-spack/opt", b"/s/spack/opt"),
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
        ],
        b"Binary with /old-spack/opt/specific-package\0 and /old-spack/opt\0",
        b"Binary with ///s/spack/opt/specific-package\0 and ///s/spack/opt\0",
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix long enough
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/opt/specific-XXXXage")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with ///////////opt/specific-XXXXage/sub\0 data",
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix too short, but
    # shortening is enough to spare more than 7 bytes of old suffix.
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/opt/specific-XXXXXge")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with /opt/specific-XXXXXge/sub\0ckage/sub\0 data",  # ckage/sub = 9 bytes
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix too short,
    # shortening leaves exactly 7 suffix bytes untouched, amazing!
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/spack/specific-XXXXXge")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with /spack/specific-XXXXXge/sub\0age/sub\0 data",  # age/sub = 7 bytes
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix too short,
    # shortening doesn't leave space for 7 bytes, sad!
    error_msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
        b"/old-spack/opt/specific-package",
        b"/snacks/specific-XXXXXge",
        b"/old-spack/opt/specific-package/sub",
    )
    with pytest.raises(relocate_text.CannotShrinkCString, match=error_msg):
        replace_and_expect(
            [(b"/old-spack/opt/specific-package", b"/snacks/specific-XXXXXge")],
            b"Binary with /old-spack/opt/specific-package/sub\0 data",
            # expect failure!
            suffix_safety_size=7,
        )

    # Check that it works when changing suffix_safety_size.
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/snacks/specific-XXXXXXe")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with /snacks/specific-XXXXXXe/sub\0ge/sub\0 data",
        suffix_safety_size=6,
    )

    # Finally check the case of no shortening but a long enough common suffix.
    replace_and_expect(
        [(b"pkg-gwixwaalgczp6", b"pkg-zkesfralgczp6")],
        b"Binary with pkg-gwixwaalgczp6/config\0 data",
        b"Binary with pkg-zkesfralgczp6/config\0 data",
        suffix_safety_size=7,
    )

    # Too short matching suffix, identical string length
    error_msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
        b"pkg-gwixwaxlgczp6", b"pkg-zkesfrzlgczp6", b"pkg-gwixwaxlgczp6"
    )
    with pytest.raises(relocate_text.CannotShrinkCString, match=error_msg):
        replace_and_expect(
            [(b"pkg-gwixwaxlgczp6", b"pkg-zkesfrzlgczp6")],
            b"Binary with pkg-gwixwaxlgczp6\0 data",
            # expect failure
            suffix_safety_size=7,
        )

    # Finally, make sure that the regex is not greedily finding the LAST null byte
    # it should find the first null byte in the window. In this test we put one null
    # at a distance where we cant keep a long enough suffix, and one where we can,
    # so we should expect failure when the first null is used.
    error_msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
        b"pkg-abcdef", b"pkg-xyzabc", b"pkg-abcdef"
    )
    with pytest.raises(relocate_text.CannotShrinkCString, match=error_msg):
        replace_and_expect(
            [(b"pkg-abcdef", b"pkg-xyzabc")],
            b"Binary with pkg-abcdef\0/xx\0",  # def\0/xx is 7 bytes.
            # expect failure
            suffix_safety_size=7,
        )


def test_inplace_text_replacement():
    def replace_and_expect(prefix_to_prefix, before: bytes, after: bytes):
        f = io.BytesIO(before)
        replacer = relocate_text.TextFilePrefixReplacer(OrderedDict(prefix_to_prefix))
        replacer.apply_to_file(f)
        f.seek(0)
        assert f.read() == after

    replace_and_expect(
        [
            (b"/first/prefix", b"/first-replacement/prefix"),
            (b"/second/prefix", b"/second-replacement/prefix"),
        ],
        b"Example: /first/prefix/subdir and /second/prefix/subdir",
        b"Example: /first-replacement/prefix/subdir and /second-replacement/prefix/subdir",
    )

    replace_and_expect(
        [
            (b"/replace/in/order", b"/first"),
            (b"/replace/in", b"/second"),
            (b"/replace", b"/third"),
        ],
        b"/replace/in/order/x /replace/in/y /replace/z",
        b"/first/x /second/y /third/z",
    )

    replace_and_expect(
        [
            (b"/replace", b"/third"),
            (b"/replace/in", b"/second"),
            (b"/replace/in/order", b"/first"),
        ],
        b"/replace/in/order/x /replace/in/y /replace/z",
        b"/third/in/order/x /third/in/y /third/z",
    )

    replace_and_expect(
        [(b"/my/prefix", b"/replacement")],
        b"/dont/replace/my/prefix #!/dont/replace/my/prefix",
        b"/dont/replace/my/prefix #!/dont/replace/my/prefix",
    )

    replace_and_expect(
        [(b"/my/prefix", b"/replacement")],
        b"Install path: /my/prefix.",
        b"Install path: /replacement.",
    )

    replace_and_expect([(b"/my/prefix", b"/replacement")], b"#!/my/prefix", b"#!/replacement")


def test_relocate_text_filters_redundant_entries():
    # Test that we're filtering identical old / new paths, since that's a waste.
    mapping = OrderedDict([("/hello", "/hello"), ("/world", "/world")])
    replacer_1 = relocate_text.BinaryFilePrefixReplacer.from_strings_or_bytes(mapping)
    replacer_2 = relocate_text.TextFilePrefixReplacer.from_strings_or_bytes(mapping)
    assert not replacer_1.prefix_to_prefix
    assert not replacer_2.prefix_to_prefix
