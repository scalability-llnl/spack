# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
These tests check Spec DAG operations using dummy packages.
"""
import pytest

import spack.deptypes as dt
import spack.error
import spack.repo
import spack.util.hash as hashutil
import spack.version
from spack.dependency import Dependency
from spack.spec import Spec


def check_links(spec_to_check):
    for spec in spec_to_check.traverse():
        for dependent in spec.dependents():
            assert dependent.edges_to_dependencies(name=spec.name)

        for dependency in spec.dependencies():
            assert dependency.edges_from_dependents(name=spec.name)


@pytest.fixture()
def saved_deps():
    """Returns a dictionary to save the dependencies."""
    return {}


@pytest.fixture()
def set_dependency(saved_deps, monkeypatch):
    """Returns a function that alters the dependency information
    for a package in the ``saved_deps`` fixture.
    """

    def _mock(pkg_name, spec):
        """Alters dependence information for a package.

        Adds a dependency on <spec> to pkg. Use this to mock up constraints.
        """
        spec = Spec(spec)
        # Save original dependencies before making any changes.
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        if pkg_name not in saved_deps:
            saved_deps[pkg_name] = (pkg_cls, pkg_cls.dependencies.copy())

        cond = Spec(pkg_cls.name)
        dependency = Dependency(pkg_cls, spec)
        monkeypatch.setitem(pkg_cls.dependencies, cond, {spec.name: dependency})

    return _mock


@pytest.mark.usefixtures("config")
def test_test_deptype(tmpdir):
    """Ensure that test-only dependencies are only included for specified
    packages in the following spec DAG::

            w
           /|
          x y
            |
            z

    w->y deptypes are (link, build), w->x and y->z deptypes are (test)
    """
    builder = spack.repo.MockRepositoryBuilder(tmpdir)
    builder.add_package("x")
    builder.add_package("z")
    builder.add_package("y", dependencies=[("z", "test", None)])
    builder.add_package("w", dependencies=[("x", "test", None), ("y", None, None)])

    with spack.repo.use_repositories(builder.root):
        spec = Spec("w").concretized(tests=("w",))
        assert "x" in spec
        assert "z" not in spec


@pytest.mark.usefixtures("config")
def test_installed_deps(monkeypatch, mock_packages):
    """Ensure that concrete specs and their build deps don't constrain solves.

    Preinstall a package ``c`` that has a constrained build dependency on ``d``, then
    install ``a`` and ensure that neither:

      * ``c``'s package constraints, nor
      * the concrete ``c``'s build dependencies

    constrain ``a``'s dependency on ``d``.

    """
    # see installed-deps-[abcde] test packages.
    #     a
    #    / \
    #   b   c   b --> d build/link
    #   |\ /|   b --> e build/link
    #   |/ \|   c --> d build
    #   d   e   c --> e build/link
    #
    a, b, c, d, e = ["installed-deps-%s" % s for s in "abcde"]

    # install C, which will force d's version to be 2
    # BUT d is only a build dependency of C, so it won't constrain
    # link/run dependents of C when C is depended on as an existing
    # (concrete) installation.
    c_spec = Spec(c)
    c_spec.concretize()
    assert c_spec[d].version == spack.version.Version("2")

    installed_names = [s.name for s in c_spec.traverse()]

    def _mock_installed(self):
        return self.name in installed_names

    monkeypatch.setattr(Spec, "installed", _mock_installed)

    # install A, which depends on B, C, D, and E, and force A to
    # use the installed C.  It should *not* force A to use the installed D
    # *if* we're doing a fresh installation.
    a_spec = Spec(a)
    a_spec._add_dependency(c_spec, depflag=dt.BUILD | dt.LINK, virtuals=())
    a_spec.concretize()
    assert spack.version.Version("2") == a_spec[c][d].version
    assert spack.version.Version("2") == a_spec[e].version
    assert spack.version.Version("3") == a_spec[b][d].version
    assert spack.version.Version("3") == a_spec[d].version


@pytest.mark.usefixtures("config")
def test_specify_preinstalled_dep(tmpdir, monkeypatch):
    """Specify the use of a preinstalled package during concretization with a
    transitive dependency that is only supplied by the preinstalled package.
    """
    builder = spack.repo.MockRepositoryBuilder(tmpdir)
    builder.add_package("pkg-c")
    builder.add_package("pkg-b", dependencies=[("pkg-c", None, None)])
    builder.add_package("pkg-a", dependencies=[("pkg-b", None, None)])

    with spack.repo.use_repositories(builder.root):
        b_spec = Spec("pkg-b").concretized()
        monkeypatch.setattr(Spec, "installed", property(lambda x: x.name != "pkg-a"))

        a_spec = Spec("pkg-a")
        a_spec._add_dependency(b_spec, depflag=dt.BUILD | dt.LINK, virtuals=())
        a_spec.concretize()

        assert {x.name for x in a_spec.traverse()} == {"pkg-a", "pkg-b", "pkg-c"}


@pytest.mark.usefixtures("config")
@pytest.mark.parametrize(
    "spec_str,expr_str,expected",
    [("x ^y@2", "y@2", True), ("x@1", "y", False), ("x", "y@3", True)],
)
def test_conditional_dep_with_user_constraints(tmpdir, spec_str, expr_str, expected):
    """This sets up packages X->Y such that X depends on Y conditionally. It
    then constructs a Spec with X but with no constraints on X, so that the
    initial normalization pass cannot determine whether the constraints are
    met to add the dependency; this checks whether a user-specified constraint
    on Y is applied properly.
    """
    builder = spack.repo.MockRepositoryBuilder(tmpdir)
    builder.add_package("y")
    builder.add_package("x", dependencies=[("y", None, "x@2:")])

    with spack.repo.use_repositories(builder.root):
        spec = Spec(spec_str).concretized()
        result = expr_str in spec
        assert result is expected, "{0} in {1}".format(expr_str, spec)


@pytest.mark.usefixtures("mutable_mock_repo", "config")
class TestSpecDag:
    def test_conflicting_package_constraints(self, set_dependency):
        set_dependency("mpileaks", "mpich@1.0")
        set_dependency("callpath", "mpich@2.0")

        spec = Spec("mpileaks ^mpich ^callpath ^dyninst ^libelf ^libdwarf")

        with pytest.raises(spack.error.UnsatisfiableSpecError):
            spec.concretize()

    def test_preorder_node_traversal(self):
        dag = Spec("mpileaks ^zmpi").concretized()

        names = ["mpileaks", "callpath", "dyninst", "libdwarf", "libelf", "zmpi", "fake"]
        pairs = list(zip([0, 1, 2, 3, 4, 2, 3], names))

        traversal = dag.traverse()
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(depth=True)
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_preorder_edge_traversal(self):
        dag = Spec("mpileaks ^zmpi").concretized()

        names = [
            "mpileaks",
            "callpath",
            "dyninst",
            "libdwarf",
            "libelf",
            "libelf",
            "zmpi",
            "fake",
            "zmpi",
        ]
        pairs = list(zip([0, 1, 2, 3, 4, 3, 2, 3, 1], names))

        traversal = dag.traverse(cover="edges")
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover="edges", depth=True)
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_preorder_path_traversal(self):
        dag = Spec("mpileaks ^zmpi").concretized()

        names = [
            "mpileaks",
            "callpath",
            "dyninst",
            "libdwarf",
            "libelf",
            "libelf",
            "zmpi",
            "fake",
            "zmpi",
            "fake",
        ]
        pairs = list(zip([0, 1, 2, 3, 4, 3, 2, 3, 1, 2], names))

        traversal = dag.traverse(cover="paths")
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover="paths", depth=True)
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_postorder_node_traversal(self):
        dag = Spec("mpileaks ^zmpi").concretized()

        names = ["libelf", "libdwarf", "dyninst", "fake", "zmpi", "callpath", "mpileaks"]
        pairs = list(zip([4, 3, 2, 3, 2, 1, 0], names))

        traversal = dag.traverse(order="post")
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(depth=True, order="post")
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_postorder_edge_traversal(self):
        dag = Spec("mpileaks ^zmpi").concretized()

        names = [
            "libelf",
            "libdwarf",
            "libelf",
            "dyninst",
            "fake",
            "zmpi",
            "callpath",
            "zmpi",
            "mpileaks",
        ]
        pairs = list(zip([4, 3, 3, 2, 3, 2, 1, 1, 0], names))

        traversal = dag.traverse(cover="edges", order="post")
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover="edges", depth=True, order="post")
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_postorder_path_traversal(self):
        dag = Spec("mpileaks ^zmpi").concretized()

        names = [
            "libelf",
            "libdwarf",
            "libelf",
            "dyninst",
            "fake",
            "zmpi",
            "callpath",
            "fake",
            "zmpi",
            "mpileaks",
        ]
        pairs = list(zip([4, 3, 3, 2, 3, 2, 1, 2, 1, 0], names))

        traversal = dag.traverse(cover="paths", order="post")
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover="paths", depth=True, order="post")
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_dependents_and_dependencies_are_correct(self):
        spec = Spec.from_literal(
            {
                "mpileaks": {
                    "callpath": {
                        "dyninst": {"libdwarf": {"libelf": None}, "libelf": None},
                        "mpi": None,
                    },
                    "mpi": None,
                }
            }
        )
        check_links(spec)
        spec.concretize()
        check_links(spec)

    @pytest.mark.parametrize(
        "constraint_str,spec_str",
        [
            ("mpich@1.0", "mpileaks ^mpich@2.0"),
            ("mpich%gcc", "mpileaks ^mpich%intel"),
            ("mpich%gcc@4.6", "mpileaks ^mpich%gcc@4.5"),
            ("mpich platform=test target=be", "mpileaks ^mpich platform=test target=fe"),
        ],
    )
    def test_unsatisfiable_cases(self, set_dependency, constraint_str, spec_str):
        """Tests that synthetic cases of conflicting requirements raise an UnsatisfiableSpecError
        when concretizing.
        """
        set_dependency("mpileaks", constraint_str)
        with pytest.raises(spack.error.UnsatisfiableSpecError):
            Spec(spec_str).concretize()

    @pytest.mark.parametrize(
        "spec_str", ["libelf ^mpich", "libelf ^libdwarf", "mpich ^dyninst ^libelf"]
    )
    def test_invalid_dep(self, spec_str):
        spec = Spec(spec_str)
        with pytest.raises(spack.error.SpecError):
            spec.concretize()

    def test_equal(self):
        # Different spec structures to test for equality
        flat = Spec.from_literal({"mpileaks ^callpath ^libelf ^libdwarf": None})

        flat_init = Spec.from_literal(
            {"mpileaks": {"callpath": None, "libdwarf": None, "libelf": None}}
        )

        flip_flat = Spec.from_literal(
            {"mpileaks": {"libelf": None, "libdwarf": None, "callpath": None}}
        )

        dag = Spec.from_literal({"mpileaks": {"callpath": {"libdwarf": {"libelf": None}}}})

        flip_dag = Spec.from_literal({"mpileaks": {"callpath": {"libelf": {"libdwarf": None}}}})

        # All these are equal to each other with regular ==
        specs = (flat, flat_init, flip_flat, dag, flip_dag)
        for lhs, rhs in zip(specs, specs):
            assert lhs == rhs
            assert str(lhs) == str(rhs)

        # Same DAGs constructed different ways are equal
        assert flat.eq_dag(flat_init)

        # order at same level does not matter -- (dep on same parent)
        assert flat.eq_dag(flip_flat)

        # DAGs should be unequal if nesting is different
        assert not flat.eq_dag(dag)
        assert not flat.eq_dag(flip_dag)
        assert not flip_flat.eq_dag(dag)
        assert not flip_flat.eq_dag(flip_dag)
        assert not dag.eq_dag(flip_dag)

    def test_contains(self):
        spec = Spec("mpileaks ^mpi ^libelf@1.8.11 ^libdwarf")
        assert Spec("mpi") in spec
        assert Spec("libelf") in spec
        assert Spec("libelf@1.8.11") in spec
        assert Spec("libelf@1.8.12") not in spec
        assert Spec("libdwarf") in spec
        assert Spec("libgoblin") not in spec
        assert Spec("mpileaks") in spec

    def test_copy_simple(self):
        orig = Spec("mpileaks")
        copy = orig.copy()
        check_links(copy)

        assert orig == copy
        assert orig.eq_dag(copy)
        assert orig._normal == copy._normal
        assert orig._concrete == copy._concrete

        # ensure no shared nodes bt/w orig and copy.
        orig_ids = set(id(s) for s in orig.traverse())
        copy_ids = set(id(s) for s in copy.traverse())
        assert not orig_ids.intersection(copy_ids)

    def test_copy_concretized(self):
        orig = Spec("mpileaks")
        orig.concretize()
        copy = orig.copy()

        check_links(copy)

        assert orig == copy
        assert orig.eq_dag(copy)
        assert orig._normal == copy._normal
        assert orig._concrete == copy._concrete

        # ensure no shared nodes bt/w orig and copy.
        orig_ids = set(id(s) for s in orig.traverse())
        copy_ids = set(id(s) for s in copy.traverse())
        assert not orig_ids.intersection(copy_ids)

    def test_copy_through_spec_build_interface(self):
        """Check that copying dependencies using id(node) as a fast identifier of the
        node works when the spec is wrapped in a SpecBuildInterface object.
        """
        s = Spec("mpileaks").concretized()

        c0 = s.copy()
        assert c0 == s

        # Single indirection
        c1 = s["mpileaks"].copy()
        assert c0 == c1 == s

        # Double indirection
        c2 = s["mpileaks"]["mpileaks"].copy()
        assert c0 == c1 == c2 == s

    """
    Here is the graph with deptypes labeled (assume all packages have a 'dt'
    prefix). Arrows are marked with the deptypes ('b' for 'build', 'l' for
    'link', 'r' for 'run').

        use -bl-> top

        top -b->  build1
        top -bl-> link1
        top -r->  run1

        build1 -b->  build2
        build1 -bl-> link2
        build1 -r->  run2

        link1 -bl-> link3

        run1 -bl-> link5
        run1 -r->  run3

        link3 -b->  build2
        link3 -bl-> link4

        run3 -b-> build3
    """

    @pytest.mark.parametrize(
        "spec_str,deptypes,expected",
        [
            (
                "dtuse",
                ("build", "link"),
                [
                    "dtuse",
                    "dttop",
                    "dtbuild1",
                    "dtbuild2",
                    "dtlink2",
                    "dtlink1",
                    "dtlink3",
                    "dtlink4",
                ],
            ),
            (
                "dttop",
                ("build", "link"),
                ["dttop", "dtbuild1", "dtbuild2", "dtlink2", "dtlink1", "dtlink3", "dtlink4"],
            ),
            (
                "dttop",
                all,
                [
                    "dttop",
                    "dtbuild1",
                    "dtbuild2",
                    "dtlink2",
                    "dtrun2",
                    "dtlink1",
                    "dtlink3",
                    "dtlink4",
                    "dtrun1",
                    "dtlink5",
                    "dtrun3",
                    "dtbuild3",
                ],
            ),
            ("dttop", "run", ["dttop", "dtrun1", "dtrun3"]),
        ],
    )
    def test_deptype_traversal(self, spec_str, deptypes, expected):
        dag = Spec(spec_str).concretized()
        traversal = dag.traverse(deptype=deptypes)
        assert [x.name for x in traversal] == expected

    def test_hash_bits(self):
        """Ensure getting first n bits of a base32-encoded DAG hash works."""

        # RFC 4648 base32 decode table
        b32 = dict((j, i) for i, j in enumerate("abcdefghijklmnopqrstuvwxyz"))
        b32.update(dict((j, i) for i, j in enumerate("234567", 26)))

        # some package hashes
        tests = [
            "35orsd4cenv743hg4i5vxha2lzayycby",
            "6kfqtj7dap3773rxog6kkmoweix5gpwo",
            "e6h6ff3uvmjbq3azik2ckr6ckwm3depv",
            "snz2juf4ij7sv77cq3vs467q6acftmur",
            "4eg47oedi5bbkhpoxw26v3oe6vamkfd7",
            "vrwabwj6umeb5vjw6flx2rnft3j457rw",
        ]

        for test_hash in tests:
            # string containing raw bits of hash ('1' and '0')
            expected = "".join([format(b32[c], "#07b").replace("0b", "") for c in test_hash])

            for bits in (1, 2, 3, 4, 7, 8, 9, 16, 64, 117, 128, 160):
                actual_int = hashutil.base32_prefix_bits(test_hash, bits)
                fmt = "#0%sb" % (bits + 2)
                actual = format(actual_int, fmt).replace("0b", "")

                assert expected[:bits] == actual

            with pytest.raises(ValueError):
                hashutil.base32_prefix_bits(test_hash, 161)

            with pytest.raises(ValueError):
                hashutil.base32_prefix_bits(test_hash, 256)

    def test_traversal_directions(self):
        """Make sure child and parent traversals of specs work."""
        # Mock spec - d is used for a diamond dependency
        spec = Spec.from_literal(
            {"a": {"b": {"c": {"d": None}, "e": None}, "f": {"g": {"d": None}}}}
        )

        assert ["a", "b", "c", "d", "e", "f", "g"] == [
            s.name for s in spec.traverse(direction="children")
        ]

        assert ["g", "f", "a"] == [s.name for s in spec["g"].traverse(direction="parents")]

        assert ["d", "c", "b", "a", "g", "f"] == [
            s.name for s in spec["d"].traverse(direction="parents")
        ]

    def test_edge_traversals(self):
        """Make sure child and parent traversals of specs work."""
        # Mock spec - d is used for a diamond dependency
        spec = Spec.from_literal(
            {"a": {"b": {"c": {"d": None}, "e": None}, "f": {"g": {"d": None}}}}
        )

        assert ["a", "b", "c", "d", "e", "f", "g"] == [
            s.name for s in spec.traverse(direction="children")
        ]

        assert ["g", "f", "a"] == [s.name for s in spec["g"].traverse(direction="parents")]

        assert ["d", "c", "b", "a", "g", "f"] == [
            s.name for s in spec["d"].traverse(direction="parents")
        ]

    def test_copy_dependencies(self):
        s1 = Spec("mpileaks ^mpich2@1.1")
        s2 = s1.copy()

        assert "^mpich2@1.1" in s2
        assert "^mpich2" in s2

    def test_construct_spec_with_deptypes(self):
        """Ensure that it is possible to construct a spec with explicit
        dependency types."""
        s = Spec.from_literal(
            {"a": {"b": {"c:build": None}, "d": {"e:build,link": {"f:run": None}}}}
        )

        assert s["b"].edges_to_dependencies(name="c")[0].depflag == dt.BUILD
        assert s["d"].edges_to_dependencies(name="e")[0].depflag == dt.BUILD | dt.LINK
        assert s["e"].edges_to_dependencies(name="f")[0].depflag == dt.RUN

        assert s["c"].edges_from_dependents(name="b")[0].depflag == dt.BUILD
        assert s["e"].edges_from_dependents(name="d")[0].depflag == dt.BUILD | dt.LINK
        assert s["f"].edges_from_dependents(name="e")[0].depflag == dt.RUN

    def check_diamond_deptypes(self, spec):
        """Validate deptypes in dt-diamond spec.

        This ensures that concretization works properly when two packages
        depend on the same dependency in different ways.

        """
        assert (
            spec["dt-diamond"].edges_to_dependencies(name="dt-diamond-left")[0].depflag
            == dt.BUILD | dt.LINK
        )
        assert (
            spec["dt-diamond"].edges_to_dependencies(name="dt-diamond-right")[0].depflag
            == dt.BUILD | dt.LINK
        )
        assert (
            spec["dt-diamond-left"].edges_to_dependencies(name="dt-diamond-bottom")[0].depflag
            == dt.BUILD
        )
        assert (
            spec["dt-diamond-right"].edges_to_dependencies(name="dt-diamond-bottom")[0].depflag
            == dt.BUILD | dt.LINK | dt.RUN
        )

    def check_diamond_normalized_dag(self, spec):
        dag = Spec.from_literal(
            {
                "dt-diamond": {
                    "dt-diamond-left:build,link": {"dt-diamond-bottom:build": None},
                    "dt-diamond-right:build,link": {"dt-diamond-bottom:build,link,run": None},
                }
            }
        )

        assert spec.eq_dag(dag)

    def test_concretize_deptypes(self):
        """Ensure that dependency types are preserved after concretization."""
        s = Spec("dt-diamond")
        s.concretize()
        self.check_diamond_deptypes(s)

    def test_copy_deptypes(self):
        """Ensure that dependency types are preserved by spec copy."""
        s1 = Spec("dt-diamond").concretized()
        self.check_diamond_deptypes(s1)
        s2 = s1.copy()
        self.check_diamond_deptypes(s2)

    def test_getitem_query(self):
        s = Spec("mpileaks")
        s.concretize()

        # Check a query to a non-virtual package
        a = s["callpath"]

        query = a.last_query
        assert query.name == "callpath"
        assert len(query.extra_parameters) == 0
        assert not query.isvirtual

        # Check a query to a virtual package
        a = s["mpi"]

        query = a.last_query
        assert query.name == "mpi"
        assert len(query.extra_parameters) == 0
        assert query.isvirtual

        # Check a query to a virtual package with
        # extra parameters after query
        a = s["mpi:cxx,fortran"]

        query = a.last_query
        assert query.name == "mpi"
        assert len(query.extra_parameters) == 2
        assert "cxx" in query.extra_parameters
        assert "fortran" in query.extra_parameters
        assert query.isvirtual

    def test_getitem_exceptional_paths(self):
        s = Spec("mpileaks")
        s.concretize()
        # Needed to get a proxy object
        q = s["mpileaks"]

        # Test that the attribute is read-only
        with pytest.raises(AttributeError):
            q.libs = "foo"

        with pytest.raises(AttributeError):
            q.libs

    def test_canonical_deptype(self):
        # special values
        assert dt.canonicalize(all) == dt.ALL
        assert dt.canonicalize("all") == dt.ALL

        with pytest.raises(ValueError):
            dt.canonicalize(None)
        with pytest.raises(ValueError):
            dt.canonicalize([None])

        # everything in all_types is canonical
        for v in dt.ALL_TYPES:
            assert dt.canonicalize(v) == dt.flag_from_string(v)

        # tuples
        assert dt.canonicalize(("build",)) == dt.BUILD
        assert dt.canonicalize(("build", "link", "run")) == dt.BUILD | dt.LINK | dt.RUN
        assert dt.canonicalize(("build", "link")) == dt.BUILD | dt.LINK
        assert dt.canonicalize(("build", "run")) == dt.BUILD | dt.RUN

        # lists
        assert dt.canonicalize(["build", "link", "run"]) == dt.BUILD | dt.LINK | dt.RUN
        assert dt.canonicalize(["build", "link"]) == dt.BUILD | dt.LINK
        assert dt.canonicalize(["build", "run"]) == dt.BUILD | dt.RUN

        # sorting
        assert dt.canonicalize(("run", "build", "link")) == dt.BUILD | dt.LINK | dt.RUN
        assert dt.canonicalize(("run", "link", "build")) == dt.BUILD | dt.LINK | dt.RUN
        assert dt.canonicalize(("run", "link")) == dt.LINK | dt.RUN
        assert dt.canonicalize(("link", "build")) == dt.BUILD | dt.LINK

        # deduplication
        assert dt.canonicalize(("run", "run", "link")) == dt.RUN | dt.LINK
        assert dt.canonicalize(("run", "link", "link")) == dt.RUN | dt.LINK

        # can't put 'all' in tuple or list
        with pytest.raises(ValueError):
            dt.canonicalize(["all"])
        with pytest.raises(ValueError):
            dt.canonicalize(("all",))

        # invalid values
        with pytest.raises(ValueError):
            dt.canonicalize("foo")
        with pytest.raises(ValueError):
            dt.canonicalize(("foo", "bar"))
        with pytest.raises(ValueError):
            dt.canonicalize(("foo",))

    def test_invalid_literal_spec(self):
        # Can't give type 'build' to a top-level spec
        with pytest.raises(spack.error.SpecSyntaxError):
            Spec.from_literal({"foo:build": None})

        # Can't use more than one ':' separator
        with pytest.raises(KeyError):
            Spec.from_literal({"foo": {"bar:build:link": None}})

    def test_spec_tree_respect_deptypes(self):
        # Version-test-root uses version-test-pkg as a build dependency
        s = Spec("version-test-root").concretized()
        out = s.tree(deptypes="all")
        assert "version-test-pkg" in out
        out = s.tree(deptypes=("link", "run"))
        assert "version-test-pkg" not in out


def test_tree_cover_nodes_reduce_deptype():
    """Test that tree output with deptypes sticks to the sub-dag of interest, instead of looking
    at in-edges from nodes not reachable from the root."""
    a, b, c, d = Spec("a"), Spec("b"), Spec("c"), Spec("d")
    a.add_dependency_edge(d, depflag=dt.BUILD, virtuals=())
    a.add_dependency_edge(b, depflag=dt.LINK, virtuals=())
    b.add_dependency_edge(d, depflag=dt.LINK, virtuals=())
    c.add_dependency_edge(d, depflag=dt.RUN | dt.TEST, virtuals=())
    assert (
        a.tree(cover="nodes", show_types=True)
        == """\
[    ]  a
[ l  ]      ^b
[bl  ]      ^d
"""
    )
    assert (
        c.tree(cover="nodes", show_types=True)
        == """\
[    ]  c
[  rt]      ^d
"""
    )


def test_synthetic_construction_of_split_dependencies_from_same_package(mock_packages, config):
    # Construct in a synthetic way (i.e. without using the solver)
    # the following spec:
    #
    #        pkg-b
    #  build /   \ link,run
    #  pkg-c@2.0   pkg-c@1.0
    #
    # To demonstrate that a spec can now hold two direct
    # dependencies from the same package
    root = Spec("pkg-b").concretized()
    link_run_spec = Spec("pkg-c@=1.0").concretized()
    build_spec = Spec("pkg-c@=2.0").concretized()

    root.add_dependency_edge(link_run_spec, depflag=dt.LINK, virtuals=())
    root.add_dependency_edge(link_run_spec, depflag=dt.RUN, virtuals=())
    root.add_dependency_edge(build_spec, depflag=dt.BUILD, virtuals=())

    # Check dependencies from the perspective of root
    assert len(root.dependencies()) == 2
    assert all(x.name == "pkg-c" for x in root.dependencies())

    assert "@2.0" in root.dependencies(name="pkg-c", deptype=dt.BUILD)[0]
    assert "@1.0" in root.dependencies(name="pkg-c", deptype=dt.LINK | dt.RUN)[0]

    # Check parent from the perspective of the dependencies
    assert len(build_spec.dependents()) == 1
    assert len(link_run_spec.dependents()) == 1
    assert build_spec.dependents() == link_run_spec.dependents()
    assert build_spec != link_run_spec


def test_synthetic_construction_bootstrapping(mock_packages, config):
    # Construct the following spec:
    #
    #  pkg-b@2.0
    #    | build
    #  pkg-b@1.0
    #
    root = Spec("pkg-b@=2.0").concretized()
    bootstrap = Spec("pkg-b@=1.0").concretized()

    root.add_dependency_edge(bootstrap, depflag=dt.BUILD, virtuals=())

    assert len(root.dependencies()) == 1
    assert root.dependencies()[0].name == "pkg-b"
    assert root.name == "pkg-b"


def test_addition_of_different_deptypes_in_multiple_calls(mock_packages, config):
    # Construct the following spec:
    #
    #  pkg-b@2.0
    #    | build,link,run
    #  pkg-b@1.0
    #
    # with three calls and check we always have a single edge
    root = Spec("pkg-b@=2.0").concretized()
    bootstrap = Spec("pkg-b@=1.0").concretized()

    for current_depflag in (dt.BUILD, dt.LINK, dt.RUN):
        root.add_dependency_edge(bootstrap, depflag=current_depflag, virtuals=())

        # Check edges in dependencies
        assert len(root.edges_to_dependencies()) == 1
        forward_edge = root.edges_to_dependencies(depflag=current_depflag)[0]
        assert current_depflag & forward_edge.depflag
        assert id(forward_edge.parent) == id(root)
        assert id(forward_edge.spec) == id(bootstrap)

        # Check edges from dependents
        assert len(bootstrap.edges_from_dependents()) == 1
        backward_edge = bootstrap.edges_from_dependents(depflag=current_depflag)[0]
        assert current_depflag & backward_edge.depflag
        assert id(backward_edge.parent) == id(root)
        assert id(backward_edge.spec) == id(bootstrap)


@pytest.mark.parametrize(
    "c1_depflag,c2_depflag",
    [(dt.LINK, dt.BUILD | dt.LINK), (dt.LINK | dt.RUN, dt.BUILD | dt.LINK)],
)
def test_adding_same_deptype_with_the_same_name_raises(
    mock_packages, config, c1_depflag, c2_depflag
):
    p = Spec("pkg-b@=2.0").concretized()
    c1 = Spec("pkg-b@=1.0").concretized()
    c2 = Spec("pkg-b@=2.0").concretized()

    p.add_dependency_edge(c1, depflag=c1_depflag, virtuals=())
    with pytest.raises(spack.error.SpackError):
        p.add_dependency_edge(c2, depflag=c2_depflag, virtuals=())


@pytest.mark.regression("33499")
def test_indexing_prefers_direct_or_transitive_link_deps():
    # Test whether spec indexing prefers direct/transitive link type deps over deps of
    # build/run/test deps, and whether it does fall back to a full dag search.
    root = Spec("root")

    # Use a and z to since we typically traverse by edges sorted alphabetically.
    a1 = Spec("a1")
    a2 = Spec("a2")
    z1 = Spec("z1")
    z2 = Spec("z2")

    # Same package, different spec.
    z3_flavor_1 = Spec("z3 +through_a1")
    z3_flavor_2 = Spec("z3 +through_z1")

    root.add_dependency_edge(a1, depflag=dt.BUILD | dt.RUN | dt.TEST, virtuals=())

    # unique package as a dep of a build/run/test type dep.
    a1.add_dependency_edge(a2, depflag=dt.ALL, virtuals=())
    a1.add_dependency_edge(z3_flavor_1, depflag=dt.ALL, virtuals=())

    # chain of link type deps root -> z1 -> z2 -> z3
    root.add_dependency_edge(z1, depflag=dt.LINK, virtuals=())
    z1.add_dependency_edge(z2, depflag=dt.LINK, virtuals=())
    z2.add_dependency_edge(z3_flavor_2, depflag=dt.LINK, virtuals=())

    # Indexing should prefer the link-type dep.
    assert "through_z1" in root["z3"].variants
    assert "through_a1" in a1["z3"].variants

    # Ensure that the full DAG is still searched
    assert root["a2"]


def test_getitem_sticks_to_subdag():
    """Test that indexing on Spec by virtual does not traverse outside the dag, which happens in
    the unlikely case someone would rewrite __getitem__ in terms of edges_from_dependents instead
    of edges_to_dependencies."""
    x, y, z = Spec("x"), Spec("y"), Spec("z")
    x.add_dependency_edge(z, depflag=dt.LINK, virtuals=("virtual",))
    y.add_dependency_edge(z, depflag=dt.LINK, virtuals=())
    assert x["virtual"].name == "z"
    with pytest.raises(KeyError):
        y["virtual"]


def test_getitem_finds_transitive_virtual():
    x, y, z = Spec("x"), Spec("y"), Spec("z")
    x.add_dependency_edge(z, depflag=dt.LINK, virtuals=())
    x.add_dependency_edge(y, depflag=dt.LINK, virtuals=())
    y.add_dependency_edge(z, depflag=dt.LINK, virtuals=("virtual",))
    assert x["virtual"].name == "z"
