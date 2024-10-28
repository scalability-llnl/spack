# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ast
import os

import pytest

import spack.directives
import spack.directives_meta
import spack.paths
import spack.repo
import spack.util.package_hash as ph
from spack.spec import Spec
from spack.util.unparse import unparse

datadir = os.path.join(spack.paths.test_path, "data", "unparse")


def compare_sans_name(eq, spec1, spec2):
    content1 = ph.canonical_source(spec1)
    content1 = content1.replace(spack.repo.PATH.get_pkg_class(spec1.name).__name__, "TestPackage")
    content2 = ph.canonical_source(spec2)
    content2 = content2.replace(spack.repo.PATH.get_pkg_class(spec2.name).__name__, "TestPackage")
    if eq:
        assert content1 == content2
    else:
        assert content1 != content2


def compare_hash_sans_name(eq, spec1, spec2):
    content1 = ph.canonical_source(spec1)
    pkg_cls1 = spack.repo.PATH.get_pkg_class(spec1.name)
    content1 = content1.replace(pkg_cls1.__name__, "TestPackage")
    hash1 = pkg_cls1(spec1).content_hash(content=content1)

    content2 = ph.canonical_source(spec2)
    pkg_cls2 = spack.repo.PATH.get_pkg_class(spec2.name)
    content2 = content2.replace(pkg_cls2.__name__, "TestPackage")
    hash2 = pkg_cls2(spec2).content_hash(content=content2)

    assert (hash1 == hash2) == eq


def test_hash(mock_packages, config):
    ph.package_hash(Spec("hash-test1@=1.2"))


def test_different_variants(mock_packages, config):
    spec1 = Spec("hash-test1@=1.2 +variantx")
    spec2 = Spec("hash-test1@=1.2 +varianty")
    assert ph.package_hash(spec1) == ph.package_hash(spec2)


def test_all_same_but_name(mock_packages, config):
    spec1 = Spec("hash-test1@=1.2")
    spec2 = Spec("hash-test2@=1.2")
    compare_sans_name(True, spec1, spec2)

    spec1 = Spec("hash-test1@=1.2 +varianty")
    spec2 = Spec("hash-test2@=1.2 +varianty")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_archive_hash(mock_packages, config):
    """
    Archive hash is not intended to be reflected in Package hash.
    """
    spec1 = Spec("hash-test1@=1.3")
    spec2 = Spec("hash-test2@=1.3")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_patch_contents(mock_packages, config):
    spec1 = Spec("hash-test1@=1.1")
    spec2 = Spec("hash-test2@=1.1")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_patches_to_apply(mock_packages, config):
    spec1 = Spec("hash-test1@=1.4")
    spec2 = Spec("hash-test2@=1.4")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_install(mock_packages, config):
    spec1 = Spec("hash-test1@=1.5")
    spec2 = Spec("hash-test2@=1.5")
    compare_sans_name(False, spec1, spec2)


def test_content_hash_all_same_but_patch_contents(mock_packages, config):
    spec1 = Spec("hash-test1@1.1").concretized()
    spec2 = Spec("hash-test2@1.1").concretized()
    compare_hash_sans_name(False, spec1, spec2)


def test_content_hash_not_concretized(mock_packages, config):
    """Check that Package.content_hash() works on abstract specs."""
    # these are different due to the package hash
    spec1 = Spec("hash-test1@=1.1")
    spec2 = Spec("hash-test2@=1.3")
    compare_hash_sans_name(False, spec1, spec2)

    # at v1.1 these are actually the same package when @when's are removed
    # and the name isn't considered
    spec1 = Spec("hash-test1@=1.1")
    spec2 = Spec("hash-test2@=1.1")
    compare_hash_sans_name(True, spec1, spec2)

    # these end up being different b/c we can't eliminate much of the package.py
    # without a version.
    spec1 = Spec("hash-test1")
    spec2 = Spec("hash-test2")
    compare_hash_sans_name(False, spec1, spec2)


def test_content_hash_different_variants(mock_packages, config):
    spec1 = Spec("hash-test1@1.2 +variantx").concretized()
    spec2 = Spec("hash-test2@1.2 ~variantx").concretized()
    compare_hash_sans_name(True, spec1, spec2)


def test_content_hash_cannot_get_details_from_ast(mock_packages, config):
    """Packages hash-test1 and hash-test3 would be considered the same
    except that hash-test3 conditionally executes a phase based on
    a "when" directive that Spack cannot evaluate by examining the
    AST. This test ensures that Spack can compute a content hash
    for hash-test3. If Spack cannot determine when a phase applies,
    it adds it by default, so the test also ensures that the hashes
    differ where Spack includes a phase on account of AST-examination
    failure.
    """
    spec3 = Spec("hash-test1@1.7").concretized()
    spec4 = Spec("hash-test3@1.7").concretized()
    compare_hash_sans_name(False, spec3, spec4)


def test_content_hash_all_same_but_archive_hash(mock_packages, config):
    spec1 = Spec("hash-test1@1.3").concretized()
    spec2 = Spec("hash-test2@1.3").concretized()
    compare_hash_sans_name(False, spec1, spec2)


def test_content_hash_parse_dynamic_function_call(mock_packages, config):
    spec = Spec("hash-test4").concretized()
    spec.package.content_hash()


many_strings = '''\
"""ONE"""
"""TWO"""

var = "THREE"  # make sure this is not removed

"FOUR"

class ManyDocstrings:
    """FIVE"""
    """SIX"""

    x = "SEVEN"

    def method1():
        """EIGHT"""

        print("NINE")

        "TEN"
        for i in range(10):
            print(i)

    def method2():
        """ELEVEN"""
        return "TWELVE"
'''

many_strings_no_docstrings = """\
var = 'THREE'

class ManyDocstrings:
    x = 'SEVEN'

    def method1():
        print('NINE')
        for i in range(10):
            print(i)

    def method2():
        return 'TWELVE'
"""


def test_remove_docstrings():
    tree = ast.parse(many_strings)
    tree = ph.RemoveDocstrings().visit(tree)

    unparsed = unparse(tree, py_ver_consistent=True)
    assert unparsed == many_strings_no_docstrings


many_directives = """\

class HasManyDirectives:
{directives}

    def foo():
        # just a method to get in the way
        pass

{directives}
""".format(
    directives="\n".join("    %s()" % name for name in spack.directives_meta.directive_names)
)


def test_remove_all_directives():
    """Ensure all directives are removed from packages before hashing."""
    for name in spack.directives_meta.directive_names:
        assert name in many_directives

    tree = ast.parse(many_directives)
    spec = Spec("has-many-directives")
    tree = ph.RemoveDirectives(spec).visit(tree)
    unparsed = unparse(tree, py_ver_consistent=True)

    for name in spack.directives_meta.directive_names:
        assert name not in unparsed


many_attributes = """\
class HasManyMetadataAttributes:
    homepage = "https://example.com"
    url = "https://example.com/foo.tar.gz"
    git = "https://example.com/foo/bar.git"

    maintainers("alice", "bob")
    tags = ["foo", "bar", "baz"]

    depends_on("foo")
    conflicts("foo")
"""


many_attributes_canonical = """\
class HasManyMetadataAttributes:
    pass
"""


def test_remove_spack_attributes():
    tree = ast.parse(many_attributes)
    spec = Spec("has-many-metadata-attributes")
    tree = ph.RemoveDirectives(spec).visit(tree)
    unparsed = unparse(tree, py_ver_consistent=True)

    assert unparsed == many_attributes_canonical


complex_package_logic = """\
class ComplexPackageLogic:
    for variant in ["+foo", "+bar", "+baz"]:
        conflicts("quux" + variant)

    for variant in ["+foo", "+bar", "+baz"]:
        # logic in the loop prevents our dumb analyzer from having it removed. This
        # is uncommon so we don't (yet?) implement logic to detect that spec is unused.
        print("oops can't remove this.")
        conflicts("quux" + variant)

        # Hard to make a while loop that makes sense, so ignore the infinite loop here.
        # Likely nobody uses while instead of for, but we test it just in case.
        while x <= 10:
            depends_on("garply@%d.0" % x)

    # all of these should go away, as they only contain directives
    with when("@10.0"):
        depends_on("foo")
        with when("+bar"):
            depends_on("bar")
            with when("+baz"):
                depends_on("baz")

    # this whole statement should disappear
    if sys.platform == "linux":
        conflicts("baz@9.0")

    # the else block here should disappear
    if sys.platform == "linux":
        print("foo")
    else:
        conflicts("foo@9.0")

    # both blocks of this statement should disappear
    if sys.platform == "darwin":
        conflicts("baz@10.0")
    else:
        conflicts("bar@10.0")

    # This one is complicated as the body goes away but the else block doesn't.
    # Again, this could be optimized, but we're just testing removal logic here.
    if sys.platform() == "darwin":
        conflicts("baz@10.0")
    else:
        print("oops can't remove this.")
        conflicts("bar@10.0")
"""


complex_package_logic_filtered = """\
class ComplexPackageLogic:
    for variant in ['+foo', '+bar', '+baz']:
        print("oops can't remove this.")
    if sys.platform == 'linux':
        print('foo')
    if sys.platform() == 'darwin':
        pass
    else:
        print("oops can't remove this.")
"""


def test_remove_complex_package_logic_filtered():
    tree = ast.parse(complex_package_logic)
    spec = Spec("has-many-metadata-attributes")
    tree = ph.RemoveDirectives(spec).visit(tree)
    unparsed = unparse(tree, py_ver_consistent=True)

    assert unparsed == complex_package_logic_filtered


@pytest.mark.parametrize(
    "package_spec,expected_hash",
    [
        ("amdfftw", "tivb752zddjgvfkogfs7cnnvp5olj6co"),
        ("grads", "rrlmwml3f2frdnqavmro3ias66h5b2ce"),
        ("llvm", "nufffum5dabmaf4l5tpfcblnbfjknvd3"),
        # has @when("@4.1.0") and raw unicode literals
        ("mfem", "whwftpqbjvzncmb52oz6izkanbha2uji"),
        ("mfem@4.0.0", "whwftpqbjvzncmb52oz6izkanbha2uji"),
        ("mfem@4.1.0", "bpi7of3xelo7fr3ta2lm6bmiruijnxcg"),
        # has @when("@1.5.0:")
        ("py-torch", "qs7djgqn7dy7r3ps4g7hv2pjvjk4qkhd"),
        ("py-torch@1.0", "qs7djgqn7dy7r3ps4g7hv2pjvjk4qkhd"),
        ("py-torch@1.6", "p4ine4hc6f2ik2f2wyuwieslqbozll5w"),
        # has a print with multiple arguments
        ("legion", "bq2etsik5l6pbryxmbhfhzynci56ruy4"),
        # has nested `with when()` blocks and loops
        ("trilinos", "vqrgscjrla4hi7bllink7v6v6dwxgc2p"),
    ],
)
def test_package_hash_consistency(package_spec, expected_hash):
    """Ensure that that package hash is consistent python version to version.

    We assume these tests run across all supported Python versions in CI, and we ensure
    consistency with recorded hashes for some well known inputs.

    If this fails, then something about the way the python AST works has likely changed.
    If Spack is running in a new python version, we might need to modify the unparser to
    handle it. If not, then something has become inconsistent about the way we unparse
    Python code across versions.

    """
    spec = Spec(package_spec)
    filename = os.path.join(datadir, "%s.txt" % spec.name)
    with open(filename) as f:
        source = f.read()
    h = ph.package_hash(spec, source=source)
    assert expected_hash == h


many_multimethods = """\
class Pkg:
    def foo(self):
        print("ONE")

    @when("@1.0")
    def foo(self):
        print("TWO")

    @when("@2.0")
    @when(sys.platform == "darwin")
    def foo(self):
        print("THREE")

    @when("@3.0")
    def foo(self):
        print("FOUR")

    # this one should always stay
    @run_after("install")
    def some_function(self):
        print("FIVE")
"""


more_dynamic_multimethods = """\
class Pkg:
    @when(sys.platform == "darwin")
    def foo(self):
        print("ONE")

    @when("@1.0")
    def foo(self):
        print("TWO")

    # this one isn't dynamic, but an int fails the Spec parse,
    # so it's kept because it has to be evaluated at runtime.
    @when("@2.0")
    @when(1)
    def foo(self):
        print("THREE")

    @when("@3.0")
    def foo(self):
        print("FOUR")

    # this one should always stay
    @run_after("install")
    def some_function(self):
        print("FIVE")
"""


@pytest.mark.parametrize(
    "spec_str,source,expected,not_expected",
    [
        # all are false but the default
        ("pkg@4.0", many_multimethods, ["ONE", "FIVE"], ["TWO", "THREE", "FOUR"]),
        # we know first @when overrides default and others are false
        ("pkg@1.0", many_multimethods, ["TWO", "FIVE"], ["ONE", "THREE", "FOUR"]),
        # we know last @when overrides default and others are false
        ("pkg@3.0", many_multimethods, ["FOUR", "FIVE"], ["ONE", "TWO", "THREE"]),
        # we don't know if default or THREE will win, include both
        ("pkg@2.0", many_multimethods, ["ONE", "THREE", "FIVE"], ["TWO", "FOUR"]),
        # we know the first one is the only one that can win.
        ("pkg@4.0", more_dynamic_multimethods, ["ONE", "FIVE"], ["TWO", "THREE", "FOUR"]),
        # now we have to include ONE and TWO because ONE may win dynamically.
        ("pkg@1.0", more_dynamic_multimethods, ["ONE", "TWO", "FIVE"], ["THREE", "FOUR"]),
        # we know FOUR is true and TWO and THREE are false, but ONE may
        # still win dynamically.
        ("pkg@3.0", more_dynamic_multimethods, ["ONE", "FOUR", "FIVE"], ["TWO", "THREE"]),
        # TWO and FOUR can't be satisfied, but ONE or THREE could win
        ("pkg@2.0", more_dynamic_multimethods, ["ONE", "THREE", "FIVE"], ["TWO", "FOUR"]),
    ],
)
def test_multimethod_resolution(spec_str, source, expected, not_expected):
    filtered = ph.canonical_source(Spec(spec_str), source=source)
    for item in expected:
        assert item in filtered
    for item in not_expected:
        assert item not in filtered
