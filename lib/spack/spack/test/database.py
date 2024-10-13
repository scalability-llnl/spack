# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Check the database is functioning properly, both in memory and in its file."""
import datetime
import functools
import json
import os
import re
import shutil
import sys

import pytest

import spack.subprocess_context

try:
    import uuid

    _use_uuid = True
except ImportError:
    _use_uuid = False

import jsonschema

import llnl.util.lock as lk
from llnl.util.tty.colify import colify

import spack.database
import spack.deptypes as dt
import spack.package_base
import spack.repo
import spack.spec
import spack.store
import spack.version as vn
from spack.installer import PackageInstaller
from spack.schema.database_index import schema
from spack.util.executable import Executable

pytestmark = pytest.mark.db


@pytest.fixture()
def upstream_and_downstream_db(tmpdir, gen_mock_layout):
    mock_db_root = str(tmpdir.mkdir("mock_db_root"))
    upstream_layout = gen_mock_layout("/a/")
    upstream_write_db = spack.database.Database(mock_db_root, layout=upstream_layout)
    upstream_db = spack.database.Database(mock_db_root, is_upstream=True, layout=upstream_layout)
    # Generate initial DB file to avoid reindex
    with open(upstream_write_db._index_path, "w") as db_file:
        upstream_write_db._write_to_file(db_file)

    downstream_db_root = str(tmpdir.mkdir("mock_downstream_db_root"))
    downstream_db = spack.database.Database(
        downstream_db_root, upstream_dbs=[upstream_db], layout=gen_mock_layout("/b/")
    )
    with open(downstream_db._index_path, "w") as db_file:
        downstream_db._write_to_file(db_file)

    yield upstream_write_db, upstream_db, downstream_db


@pytest.mark.parametrize(
    "install_tree,result",
    [
        ("all", ["pkg-b", "pkg-c"]),
        ("upstream", ["pkg-c"]),
        ("local", ["pkg-b"]),
        ("{u}", ["pkg-c"]),
        ("{d}", ["pkg-b"]),
    ],
)
def test_query_by_install_tree(
    install_tree, result, upstream_and_downstream_db, mock_packages, monkeypatch, config
):
    up_write_db, up_db, down_db = upstream_and_downstream_db

    # Set the upstream DB to contain "pkg-c" and downstream to contain "pkg-b")
    b = spack.spec.Spec("pkg-b").concretized()
    c = spack.spec.Spec("pkg-c").concretized()
    up_write_db.add(c)
    up_db._read()
    down_db.add(b)

    specs = down_db.query(install_tree=install_tree.format(u=up_db.root, d=down_db.root))
    assert [s.name for s in specs] == result


def test_spec_installed_upstream(
    upstream_and_downstream_db, mock_custom_repository, config, monkeypatch
):
    """Test whether Spec.installed_upstream() works."""
    upstream_write_db, upstream_db, downstream_db = upstream_and_downstream_db

    # a known installed spec should say that it's installed
    with spack.repo.use_repositories(mock_custom_repository):
        spec = spack.spec.Spec("pkg-c").concretized()
        assert not spec.installed
        assert not spec.installed_upstream

        upstream_write_db.add(spec)
        upstream_db._read()

        monkeypatch.setattr(spack.store.STORE, "db", downstream_db)
        assert spec.installed
        assert spec.installed_upstream
        assert spec.copy().installed

    # an abstract spec should say it's not installed
    spec = spack.spec.Spec("not-a-real-package")
    assert not spec.installed
    assert not spec.installed_upstream


@pytest.mark.usefixtures("config")
def test_installed_upstream(upstream_and_downstream_db, tmpdir):
    upstream_write_db, upstream_db, downstream_db = upstream_and_downstream_db

    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("mock.repo"))
    builder.add_package("x")
    builder.add_package("z")
    builder.add_package("y", dependencies=[("z", None, None)])
    builder.add_package("w", dependencies=[("x", None, None), ("y", None, None)])

    with spack.repo.use_repositories(builder.root):
        spec = spack.spec.Spec("w").concretized()
        for dep in spec.traverse(root=False):
            upstream_write_db.add(dep)
        upstream_db._read()

        for dep in spec.traverse(root=False):
            record = downstream_db.get_by_hash(dep.dag_hash())
            assert record is not None
            with pytest.raises(spack.database.ForbiddenLockError):
                upstream_db.get_by_hash(dep.dag_hash())

        new_spec = spack.spec.Spec("w").concretized()
        downstream_db.add(new_spec)
        for dep in new_spec.traverse(root=False):
            upstream, record = downstream_db.query_by_spec_hash(dep.dag_hash())
            assert upstream
            assert record.path == upstream_db.layout.path_for_spec(dep)
        upstream, record = downstream_db.query_by_spec_hash(new_spec.dag_hash())
        assert not upstream
        assert record.installed

        upstream_db._check_ref_counts()
        downstream_db._check_ref_counts()


def test_removed_upstream_dep(upstream_and_downstream_db, tmpdir, capsys, config):
    upstream_write_db, upstream_db, downstream_db = upstream_and_downstream_db

    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("mock.repo"))
    builder.add_package("z")
    builder.add_package("y", dependencies=[("z", None, None)])

    with spack.repo.use_repositories(builder):
        y = spack.spec.Spec("y").concretized()
        z = y["z"]

        # add dependency to upstream, dependents to downstream
        upstream_write_db.add(z)
        upstream_db._read()
        downstream_db.add(y)

        # remove the dependency from the upstream DB
        upstream_write_db.remove(z)
        upstream_db._read()

        # then rereading the downstream DB should warn about the missing dep
        downstream_db._read_from_file(downstream_db._index_path)
        assert (
            f"Missing dependency not in database: y/{y.dag_hash(7)} needs z"
            in capsys.readouterr().err
        )


@pytest.mark.usefixtures("config")
def test_add_to_upstream_after_downstream(upstream_and_downstream_db, tmpdir):
    """An upstream DB can add a package after it is installed in the downstream
    DB. When a package is recorded as installed in both, the results should
    refer to the downstream DB.
    """
    upstream_write_db, upstream_db, downstream_db = upstream_and_downstream_db

    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("mock.repo"))
    builder.add_package("x")

    with spack.repo.use_repositories(builder.root):
        spec = spack.spec.Spec("x").concretized()

        downstream_db.add(spec)
        upstream_write_db.add(spec)
        upstream_db._read()

        upstream, record = downstream_db.query_by_spec_hash(spec.dag_hash())
        # Even though the package is recorded as installed in the upstream DB,
        # we prefer the locally-installed instance
        assert not upstream

        qresults = downstream_db.query("x")
        assert len(qresults) == 1
        (queried_spec,) = qresults
        try:
            orig_db = spack.store.STORE.db
            spack.store.STORE.db = downstream_db
            assert queried_spec.prefix == downstream_db.layout.path_for_spec(spec)
        finally:
            spack.store.STORE.db = orig_db


def test_cannot_write_upstream(tmp_path, mock_packages, config):
    # Instantiate the database that will be used as the upstream DB and make
    # sure it has an index file
    with spack.database.Database(str(tmp_path)).write_transaction():
        pass

    # Create it as an upstream
    db = spack.database.Database(str(tmp_path), is_upstream=True)

    with pytest.raises(spack.database.ForbiddenLockError):
        db.add(spack.spec.Spec("pkg-a").concretized())


@pytest.mark.usefixtures("config", "temporary_store")
def test_recursive_upstream_dbs(tmpdir, gen_mock_layout):
    roots = [str(tmpdir.mkdir(x)) for x in ["a", "b", "c"]]
    layouts = [gen_mock_layout(x) for x in ["/ra/", "/rb/", "/rc/"]]

    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("mock.repo"))
    builder.add_package("z")
    builder.add_package("y", dependencies=[("z", None, None)])
    builder.add_package("x", dependencies=[("y", None, None)])

    with spack.repo.use_repositories(builder.root):
        spec = spack.spec.Spec("x").concretized()
        db_c = spack.database.Database(roots[2], layout=layouts[2])
        db_c.add(spec["z"])

        db_b = spack.database.Database(roots[1], upstream_dbs=[db_c], layout=layouts[1])
        db_b.add(spec["y"])

        db_a = spack.database.Database(roots[0], upstream_dbs=[db_b, db_c], layout=layouts[0])
        db_a.add(spec["x"])

        upstream_dbs_from_scratch = spack.store._construct_upstream_dbs_from_install_roots(
            [roots[1], roots[2]]
        )
        db_a_from_scratch = spack.database.Database(
            roots[0], upstream_dbs=upstream_dbs_from_scratch
        )

        assert db_a_from_scratch.db_for_spec_hash(spec.dag_hash()) == (db_a_from_scratch)
        assert db_a_from_scratch.db_for_spec_hash(spec["y"].dag_hash()) == (
            upstream_dbs_from_scratch[0]
        )
        assert db_a_from_scratch.db_for_spec_hash(spec["z"].dag_hash()) == (
            upstream_dbs_from_scratch[1]
        )

        db_a_from_scratch._check_ref_counts()
        upstream_dbs_from_scratch[0]._check_ref_counts()
        upstream_dbs_from_scratch[1]._check_ref_counts()

        assert db_a_from_scratch.installed_relatives(spec) == set(spec.traverse(root=False))
        assert db_a_from_scratch.installed_relatives(spec["z"], direction="parents") == set(
            [spec, spec["y"]]
        )


@pytest.fixture()
def usr_folder_exists(monkeypatch):
    """The ``/usr`` folder is assumed to be existing in some tests. This
    fixture makes it such that its existence is mocked, so we have no
    requirements on the system running tests.
    """
    isdir = os.path.isdir

    @functools.wraps(os.path.isdir)
    def mock_isdir(path):
        if path == "/usr":
            return True
        return isdir(path)

    monkeypatch.setattr(os.path, "isdir", mock_isdir)


def _print_ref_counts():
    """Print out all ref counts for the graph used here, for debugging"""
    recs = []

    def add_rec(spec):
        cspecs = spack.store.STORE.db.query(spec, installed=any)

        if not cspecs:
            recs.append("[ %-7s ] %-20s-" % ("", spec))
        else:
            key = cspecs[0].dag_hash()
            rec = spack.store.STORE.db.get_record(cspecs[0])
            recs.append("[ %-7s ] %-20s%d" % (key[:7], spec, rec.ref_count))

    with spack.store.STORE.db.read_transaction():
        add_rec("mpileaks ^mpich")
        add_rec("callpath ^mpich")
        add_rec("mpich")

        add_rec("mpileaks ^mpich2")
        add_rec("callpath ^mpich2")
        add_rec("mpich2")

        add_rec("mpileaks ^zmpi")
        add_rec("callpath ^zmpi")
        add_rec("zmpi")
        add_rec("fake")

        add_rec("dyninst")
        add_rec("libdwarf")
        add_rec("libelf")

    colify(recs, cols=3)


def _check_merkleiness():
    """Ensure the spack database is a valid merkle graph."""
    all_specs = spack.store.STORE.db.query(installed=any)

    seen = {}
    for spec in all_specs:
        for dep in spec.dependencies():
            hash_key = dep.dag_hash()
            if hash_key not in seen:
                seen[hash_key] = id(dep)
            else:
                assert seen[hash_key] == id(dep)


def _check_db_sanity(database):
    """Utility function to check db against install layout."""
    pkg_in_layout = sorted(spack.store.STORE.layout.all_specs())
    actual = sorted(database.query())

    externals = sorted([x for x in actual if x.external])
    nexpected = len(pkg_in_layout) + len(externals)

    assert nexpected == len(actual)

    non_external_in_db = sorted([x for x in actual if not x.external])

    for e, a in zip(pkg_in_layout, non_external_in_db):
        assert e == a

    _check_merkleiness()


def _check_remove_and_add_package(database: spack.database.Database, spec):
    """Remove a spec from the DB, then add it and make sure everything's
    still ok once it is added.  This checks that it was
    removed, that it's back when added again, and that ref
    counts are consistent.
    """
    original = database.query()
    database._check_ref_counts()

    # Remove spec
    concrete_spec = database.remove(spec)
    database._check_ref_counts()
    remaining = database.query()

    # ensure spec we removed is gone
    assert len(original) - 1 == len(remaining)
    assert all(s in original for s in remaining)
    assert concrete_spec not in remaining

    # add it back and make sure everything is ok.
    database.add(concrete_spec)
    installed = database.query()
    assert concrete_spec in installed
    assert installed == original

    # sanity check against direcory layout and check ref counts.
    _check_db_sanity(database)
    database._check_ref_counts()


def _mock_install(spec: str):
    s = spack.spec.Spec(spec).concretized()
    PackageInstaller([s.package], fake=True, explicit=True).install()


def _mock_remove(spec):
    specs = spack.store.STORE.db.query(spec)
    assert len(specs) == 1
    spec = specs[0]
    spec.package.do_uninstall(spec)


def test_default_queries(database):
    # Testing a package whose name *doesn't* start with 'lib'
    # to ensure the library has 'lib' prepended to the name
    rec = database.get_record("zmpi")

    spec = rec.spec

    libraries = spec["zmpi"].libs
    assert len(libraries) == 1
    assert libraries.names[0] == "zmpi"

    headers = spec["zmpi"].headers
    assert len(headers) == 1
    assert headers.names[0] == "zmpi"

    command = spec["zmpi"].command
    assert isinstance(command, Executable)
    assert command.name == "zmpi"
    assert os.path.exists(command.path)

    # Testing a package whose name *does* start with 'lib'
    # to ensure the library doesn't have a double 'lib' prefix
    rec = database.get_record("libelf")

    spec = rec.spec

    libraries = spec["libelf"].libs
    assert len(libraries) == 1
    assert libraries.names[0] == "elf"

    headers = spec["libelf"].headers
    assert len(headers) == 1
    assert headers.names[0] == "libelf"

    command = spec["libelf"].command
    assert isinstance(command, Executable)
    assert command.name == "libelf"
    assert os.path.exists(command.path)


def test_005_db_exists(database):
    """Make sure db cache file exists after creating."""
    index_file = os.path.join(database.root, ".spack-db", "index.json")
    lock_file = os.path.join(database.root, ".spack-db", "lock")
    assert os.path.exists(str(index_file))
    # Lockfiles not currently supported on Windows
    if sys.platform != "win32":
        assert os.path.exists(str(lock_file))

    with open(index_file) as fd:
        index_object = json.load(fd)
        jsonschema.validate(index_object, schema)


def test_010_all_install_sanity(database):
    """Ensure that the install layout reflects what we think it does."""
    all_specs = spack.store.STORE.layout.all_specs()
    assert len(all_specs) == 15

    # Query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies("mpileaks")]
    callpath_specs = [s for s in all_specs if s.satisfies("callpath")]
    mpi_specs = [s for s in all_specs if s.satisfies("mpi")]

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # Query specs with single configurations
    dyninst_specs = [s for s in all_specs if s.satisfies("dyninst")]
    libdwarf_specs = [s for s in all_specs if s.satisfies("libdwarf")]
    libelf_specs = [s for s in all_specs if s.satisfies("libelf")]

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len([s for s in all_specs if s.satisfies("mpileaks ^mpich")]) == 1
    assert len([s for s in all_specs if s.satisfies("mpileaks ^mpich2")]) == 1
    assert len([s for s in all_specs if s.satisfies("mpileaks ^zmpi")]) == 1


def test_015_write_and_read(mutable_database):
    # write and read DB
    with spack.store.STORE.db.write_transaction():
        specs = spack.store.STORE.db.query()
        recs = [spack.store.STORE.db.get_record(s) for s in specs]

    for spec, rec in zip(specs, recs):
        new_rec = spack.store.STORE.db.get_record(spec)
        assert new_rec.ref_count == rec.ref_count
        assert new_rec.spec == rec.spec
        assert new_rec.path == rec.path
        assert new_rec.installed == rec.installed


def test_017_write_and_read_without_uuid(mutable_database, monkeypatch):
    monkeypatch.setattr(spack.database, "_use_uuid", False)
    # write and read DB
    with spack.store.STORE.db.write_transaction():
        specs = spack.store.STORE.db.query()
        recs = [spack.store.STORE.db.get_record(s) for s in specs]

    for spec, rec in zip(specs, recs):
        new_rec = spack.store.STORE.db.get_record(spec)
        assert new_rec.ref_count == rec.ref_count
        assert new_rec.spec == rec.spec
        assert new_rec.path == rec.path
        assert new_rec.installed == rec.installed


def test_020_db_sanity(database):
    """Make sure query() returns what's actually in the db."""
    _check_db_sanity(database)


def test_025_reindex(mutable_database):
    """Make sure reindex works and ref counts are valid."""
    spack.store.STORE.reindex()
    _check_db_sanity(mutable_database)


def test_026_reindex_after_deprecate(mutable_database):
    """Make sure reindex works and ref counts are valid after deprecation."""
    mpich = mutable_database.query_one("mpich")
    zmpi = mutable_database.query_one("zmpi")
    mutable_database.deprecate(mpich, zmpi)

    spack.store.STORE.reindex()
    _check_db_sanity(mutable_database)


class ReadModify:
    """Provide a function which can execute in a separate process that removes
    a spec from the database.
    """

    def __call__(self):
        # check that other process can read DB
        _check_db_sanity(spack.store.STORE.db)
        with spack.store.STORE.db.write_transaction():
            _mock_remove("mpileaks ^zmpi")


def test_030_db_sanity_from_another_process(mutable_database):
    spack_process = spack.subprocess_context.SpackTestProcess(ReadModify())
    p = spack_process.create()
    p.start()
    p.join()

    # ensure child process change is visible in parent process
    with mutable_database.read_transaction():
        assert len(mutable_database.query("mpileaks ^zmpi")) == 0


def test_040_ref_counts(database):
    """Ensure that we got ref counts right when we read the DB."""
    database._check_ref_counts()


def test_041_ref_counts_deprecate(mutable_database):
    """Ensure that we have appropriate ref counts after deprecating"""
    mpich = mutable_database.query_one("mpich")
    zmpi = mutable_database.query_one("zmpi")

    mutable_database.deprecate(mpich, zmpi)
    mutable_database._check_ref_counts()


def test_050_basic_query(database):
    """Ensure querying database is consistent with what is installed."""
    # query everything
    total_specs = len(spack.store.STORE.db.query())
    assert total_specs == 17

    # query specs with multiple configurations
    mpileaks_specs = database.query("mpileaks")
    callpath_specs = database.query("callpath")
    mpi_specs = database.query("mpi")

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # query specs with single configurations
    dyninst_specs = database.query("dyninst")
    libdwarf_specs = database.query("libdwarf")
    libelf_specs = database.query("libelf")

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len(database.query("mpileaks ^mpich")) == 1
    assert len(database.query("mpileaks ^mpich2")) == 1
    assert len(database.query("mpileaks ^zmpi")) == 1

    # Query by date
    assert len(database.query(start_date=datetime.datetime.min)) == total_specs
    assert len(database.query(start_date=datetime.datetime.max)) == 0
    assert len(database.query(end_date=datetime.datetime.min)) == 0
    assert len(database.query(end_date=datetime.datetime.max)) == total_specs


def test_060_remove_and_add_root_package(mutable_database):
    _check_remove_and_add_package(mutable_database, "mpileaks ^mpich")


def test_070_remove_and_add_dependency_package(mutable_database):
    _check_remove_and_add_package(mutable_database, "dyninst")


def test_080_root_ref_counts(mutable_database):
    rec = mutable_database.get_record("mpileaks ^mpich")

    # Remove a top-level spec from the DB
    mutable_database.remove("mpileaks ^mpich")

    # record no longer in DB
    assert mutable_database.query("mpileaks ^mpich", installed=any) == []

    # record's deps have updated ref_counts
    assert mutable_database.get_record("callpath ^mpich").ref_count == 0
    assert mutable_database.get_record("mpich").ref_count == 1

    # Put the spec back
    mutable_database.add(rec.spec)

    # record is present again
    assert len(mutable_database.query("mpileaks ^mpich", installed=any)) == 1

    # dependencies have ref counts updated
    assert mutable_database.get_record("callpath ^mpich").ref_count == 1
    assert mutable_database.get_record("mpich").ref_count == 2


def test_090_non_root_ref_counts(mutable_database):
    mutable_database.get_record("mpileaks ^mpich")
    mutable_database.get_record("callpath ^mpich")

    # "force remove" a non-root spec from the DB
    mutable_database.remove("callpath ^mpich")

    # record still in DB but marked uninstalled
    assert mutable_database.query("callpath ^mpich", installed=True) == []
    assert len(mutable_database.query("callpath ^mpich", installed=any)) == 1

    # record and its deps have same ref_counts
    assert mutable_database.get_record("callpath ^mpich", installed=any).ref_count == 1
    assert mutable_database.get_record("mpich").ref_count == 2

    # remove only dependent of uninstalled callpath record
    mutable_database.remove("mpileaks ^mpich")

    # record and parent are completely gone.
    assert mutable_database.query("mpileaks ^mpich", installed=any) == []
    assert mutable_database.query("callpath ^mpich", installed=any) == []

    # mpich ref count updated properly.
    mpich_rec = mutable_database.get_record("mpich")
    assert mpich_rec.ref_count == 0


def test_100_no_write_with_exception_on_remove(database):
    def fail_while_writing():
        with database.write_transaction():
            _mock_remove("mpileaks ^zmpi")
            raise Exception()

    with database.read_transaction():
        assert len(database.query("mpileaks ^zmpi", installed=any)) == 1

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure zmpi is still there.
    with database.read_transaction():
        assert len(database.query("mpileaks ^zmpi", installed=any)) == 1


def test_110_no_write_with_exception_on_install(database):
    def fail_while_writing():
        with database.write_transaction():
            _mock_install("cmake")
            raise Exception()

    with database.read_transaction():
        assert database.query("cmake", installed=any) == []

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure cmake was not written.
    with database.read_transaction():
        assert database.query("cmake", installed=any) == []


def test_115_reindex_with_packages_not_in_repo(mutable_database, tmpdir):
    # Dont add any package definitions to this repository, the idea is that
    # packages should not have to be defined in the repository once they
    # are installed
    with spack.repo.use_repositories(spack.repo.MockRepositoryBuilder(tmpdir).root):
        spack.store.STORE.reindex()
        _check_db_sanity(mutable_database)


def test_external_entries_in_db(mutable_database):
    rec = mutable_database.get_record("mpileaks ^zmpi")
    assert rec.spec.external_path is None
    assert not rec.spec.external_modules

    rec = mutable_database.get_record("externaltool")
    assert rec.spec.external_path == os.path.sep + os.path.join("path", "to", "external_tool")
    assert not rec.spec.external_modules
    assert rec.explicit is False

    PackageInstaller([rec.spec.package], fake=True, explicit=True).install()
    rec = mutable_database.get_record("externaltool")
    assert rec.spec.external_path == os.path.sep + os.path.join("path", "to", "external_tool")
    assert not rec.spec.external_modules
    assert rec.explicit is True


@pytest.mark.regression("8036")
def test_regression_issue_8036(mutable_database, usr_folder_exists):
    # The test ensures that the external package prefix is treated as
    # existing. Even when the package prefix exists, the package should
    # not be considered installed until it is added to the database by
    # the installer with install().
    s = spack.spec.Spec("externaltool@0.9")
    s.concretize()
    assert not s.installed

    # Now install the external package and check again the `installed` property
    PackageInstaller([s.package], fake=True, explicit=True).install()
    assert s.installed


@pytest.mark.regression("11118")
def test_old_external_entries_prefix(mutable_database):
    with open(spack.store.STORE.db._index_path, "r") as f:
        db_obj = json.loads(f.read())

    jsonschema.validate(db_obj, schema)

    s = spack.spec.Spec("externaltool")
    s.concretize()

    db_obj["database"]["installs"][s.dag_hash()]["path"] = "None"

    with open(spack.store.STORE.db._index_path, "w") as f:
        f.write(json.dumps(db_obj))
    if _use_uuid:
        with open(spack.store.STORE.db._verifier_path, "w") as f:
            f.write(str(uuid.uuid4()))

    record = spack.store.STORE.db.get_record(s)

    assert record.path is None
    assert record.spec._prefix is None
    assert record.spec.prefix == record.spec.external_path


def test_uninstall_by_spec(mutable_database):
    with mutable_database.write_transaction():
        for spec in mutable_database.query():
            if spec.installed:
                spack.package_base.PackageBase.uninstall_by_spec(spec, force=True)
            else:
                mutable_database.remove(spec)
    assert len(mutable_database.query()) == 0


def test_query_unused_specs(mutable_database):
    # This spec installs a fake cmake as a build only dependency
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    PackageInstaller([s.package], fake=True, explicit=True).install()

    si = s.dag_hash()
    ml_mpich = spack.store.STORE.db.query_one("mpileaks ^mpich").dag_hash()
    ml_mpich2 = spack.store.STORE.db.query_one("mpileaks ^mpich2").dag_hash()
    ml_zmpi = spack.store.STORE.db.query_one("mpileaks ^zmpi").dag_hash()
    externaltest = spack.store.STORE.db.query_one("externaltest").dag_hash()
    trivial_smoke_test = spack.store.STORE.db.query_one("trivial-smoke-test").dag_hash()

    def check_unused(roots, deptype, expected):
        unused = spack.store.STORE.db.unused_specs(root_hashes=roots, deptype=deptype)
        assert set(u.name for u in unused) == set(expected)

    default_dt = dt.LINK | dt.RUN
    check_unused(None, default_dt, ["cmake"])
    check_unused(
        [si, ml_mpich, ml_mpich2, ml_zmpi, externaltest],
        default_dt,
        ["trivial-smoke-test", "cmake"],
    )
    check_unused(
        [si, ml_mpich, ml_mpich2, ml_zmpi, externaltest],
        dt.LINK | dt.RUN | dt.BUILD,
        ["trivial-smoke-test"],
    )
    check_unused(
        [si, ml_mpich, ml_mpich2, externaltest, trivial_smoke_test],
        dt.LINK | dt.RUN | dt.BUILD,
        ["mpileaks", "callpath", "zmpi", "fake"],
    )
    check_unused(
        [si, ml_mpich, ml_mpich2, ml_zmpi],
        default_dt,
        ["trivial-smoke-test", "cmake", "externaltest", "externaltool", "externalvirtual"],
    )


@pytest.mark.regression("10019")
def test_query_spec_with_conditional_dependency(mutable_database):
    # The issue is triggered by having dependencies that are
    # conditional on a Boolean variant
    s = spack.spec.Spec("hdf5~mpi")
    s.concretize()
    PackageInstaller([s.package], fake=True, explicit=True).install()

    results = spack.store.STORE.db.query_local("hdf5 ^mpich")
    assert not results


@pytest.mark.regression("10019")
def test_query_spec_with_non_conditional_virtual_dependency(database):
    # Ensure the same issue doesn't come up for virtual
    # dependency that are not conditional on variants
    results = spack.store.STORE.db.query_local("mpileaks ^mpich")
    assert len(results) == 1


def test_query_virtual_spec(database):
    """Make sure we can query for virtuals in the DB"""
    results = spack.store.STORE.db.query_local("mpi")
    assert len(results) == 3
    names = [s.name for s in results]
    assert all(name in names for name in ["mpich", "mpich2", "zmpi"])


def test_failed_spec_path_error(database):
    """Ensure spec not concrete check is covered."""
    s = spack.spec.Spec("pkg-a")
    with pytest.raises(AssertionError, match="concrete spec required"):
        spack.store.STORE.failure_tracker.mark(s)


@pytest.mark.db
def test_clear_failure_keep(mutable_database, monkeypatch, capfd):
    """Add test coverage for clear_failure operation when to be retained."""

    def _is(self, spec):
        return True

    # Pretend the spec has been failure locked
    monkeypatch.setattr(spack.database.FailureTracker, "lock_taken", _is)

    s = spack.spec.Spec("pkg-a").concretized()
    spack.store.STORE.failure_tracker.clear(s)
    out = capfd.readouterr()[0]
    assert "Retaining failure marking" in out


@pytest.mark.db
def test_clear_failure_forced(mutable_database, monkeypatch, capfd):
    """Add test coverage for clear_failure operation when force."""

    def _is(self, spec):
        return True

    # Pretend the spec has been failure locked
    monkeypatch.setattr(spack.database.FailureTracker, "lock_taken", _is)
    # Ensure raise OSError when try to remove the non-existent marking
    monkeypatch.setattr(spack.database.FailureTracker, "persistent_mark", _is)

    s = spack.spec.Spec("pkg-a").concretized()
    spack.store.STORE.failure_tracker.clear(s, force=True)
    out = capfd.readouterr()[1]
    assert "Removing failure marking despite lock" in out
    assert "Unable to remove failure marking" in out


@pytest.mark.db
def test_mark_failed(mutable_database, monkeypatch, tmpdir, capsys):
    """Add coverage to mark_failed."""

    def _raise_exc(lock):
        raise lk.LockTimeoutError("write", "/mock-lock", 1.234, 10)

    with tmpdir.as_cwd():
        s = spack.spec.Spec("pkg-a").concretized()

        # Ensure attempt to acquire write lock on the mark raises the exception
        monkeypatch.setattr(lk.Lock, "acquire_write", _raise_exc)

        spack.store.STORE.failure_tracker.mark(s)
        out = str(capsys.readouterr()[1])
        assert "Unable to mark pkg-a as failed" in out

    spack.store.STORE.failure_tracker.clear_all()


@pytest.mark.db
def test_prefix_failed(mutable_database, monkeypatch):
    """Add coverage to failed operation."""

    s = spack.spec.Spec("pkg-a").concretized()

    # Confirm the spec is not already marked as failed
    assert not spack.store.STORE.failure_tracker.has_failed(s)

    # Check that a failure entry is sufficient
    spack.store.STORE.failure_tracker.mark(s)
    assert spack.store.STORE.failure_tracker.has_failed(s)

    # Remove the entry and check again
    spack.store.STORE.failure_tracker.clear(s)
    assert not spack.store.STORE.failure_tracker.has_failed(s)

    # Now pretend that the prefix failure is locked
    monkeypatch.setattr(spack.database.FailureTracker, "lock_taken", lambda self, spec: True)
    assert spack.store.STORE.failure_tracker.has_failed(s)


def test_prefix_write_lock_error(mutable_database, monkeypatch):
    """Cover the prefix write lock exception."""

    def _raise(db, spec):
        raise lk.LockError("Mock lock error")

    s = spack.spec.Spec("pkg-a").concretized()

    # Ensure subsequent lock operations fail
    monkeypatch.setattr(lk.Lock, "acquire_write", _raise)

    with pytest.raises(Exception):
        with spack.store.STORE.prefix_locker.write_lock(s):
            assert False


@pytest.mark.regression("26600")
def test_database_works_with_empty_dir(tmpdir):
    # Create the lockfile and failures directory otherwise
    # we'll get a permission error on Database creation
    db_dir = tmpdir.ensure_dir(".spack-db")
    db_dir.ensure("lock")
    db_dir.ensure_dir("failures")
    tmpdir.chmod(mode=0o555, rec=1)
    db = spack.database.Database(str(tmpdir))
    with db.read_transaction():
        db.query()
    # Check that reading an empty directory didn't create a new index.json
    assert not os.path.exists(db._index_path)


@pytest.mark.parametrize(
    "query_arg,exc_type,msg_str",
    [
        (["callpath"], spack.store.MatchError, "matches multiple packages"),
        (["tensorflow"], spack.store.MatchError, "does not match any"),
    ],
)
def test_store_find_failures(database, query_arg, exc_type, msg_str):
    with pytest.raises(exc_type) as exc_info:
        spack.store.find(query_arg, multiple=False)
    assert msg_str in str(exc_info.value)


def test_store_find_accept_string(database):
    result = spack.store.find("callpath", multiple=True)
    assert len(result) == 3


def test_reindex_removed_prefix_is_not_installed(mutable_database, mock_store, capfd):
    """When a prefix of a dependency is removed and the database is reindexed,
    the spec should still be added through the dependent, but should be listed as
    not installed."""

    # Remove libelf from the filesystem
    prefix = mutable_database.query_one("libelf").prefix
    assert prefix.startswith(str(mock_store))
    shutil.rmtree(prefix)

    # Reindex should pick up libelf as a dependency of libdwarf
    spack.store.STORE.reindex()

    # Reindexing should warn about libelf not found on the filesystem
    assert re.search(
        "libelf@0.8.13.+ was marked installed in the database "
        "but was not found on the file system",
        capfd.readouterr().err,
    )

    # And we should still have libelf in the database, but not installed.
    assert not mutable_database.query_one("libelf", installed=True)
    assert mutable_database.query_one("libelf", installed=False)


def test_reindex_when_all_prefixes_are_removed(mutable_database, mock_store):
    # Remove all non-external installations from the filesystem
    for spec in spack.store.STORE.db.query_local():
        if not spec.external:
            assert spec.prefix.startswith(str(mock_store))
            shutil.rmtree(spec.prefix)

    # Make sure we have some explicitly installed specs
    num = len(mutable_database.query_local(installed=True, explicit=True))
    assert num > 0

    # Reindex uses the current index to repopulate itself
    spack.store.STORE.reindex()

    # Make sure all explicit specs are still there, but are now uninstalled.
    specs = mutable_database.query_local(installed=False, explicit=True)
    assert len(specs) == num

    # And make sure they can be removed from the database (covers the case where
    # `ref_count == 0 and not installed`, which hits some obscure branches.
    for s in specs:
        mutable_database.remove(s)

    assert len(mutable_database.query_local(installed=False, explicit=True)) == 0


@pytest.mark.parametrize(
    "spec_str,parent_name,expected_nparents",
    [("dyninst", "callpath", 3), ("libelf", "dyninst", 1), ("libelf", "libdwarf", 1)],
)
@pytest.mark.regression("11983")
def test_check_parents(spec_str, parent_name, expected_nparents, database):
    """Check that a spec returns the correct number of parents."""
    s = database.query_one(spec_str)

    parents = s.dependents(name=parent_name)
    assert len(parents) == expected_nparents

    edges = s.edges_from_dependents(name=parent_name)
    assert len(edges) == expected_nparents


def test_db_all_hashes(database):
    # ensure we get the right number of hashes without a read transaction
    hashes = database.all_hashes()
    assert len(hashes) == 17

    # and make sure the hashes match
    with database.read_transaction():
        assert set(s.dag_hash() for s in database.query()) == set(hashes)


def test_consistency_of_dependents_upon_remove(mutable_database):
    # Check the initial state
    s = mutable_database.query_one("dyninst")
    parents = s.dependents(name="callpath")
    assert len(parents) == 3

    # Remove a dependent (and all its dependents)
    mutable_database.remove("mpileaks ^callpath ^mpich2")
    mutable_database.remove("callpath ^mpich2")

    # Check the final state
    s = mutable_database.query_one("dyninst")
    parents = s.dependents(name="callpath")
    assert len(parents) == 2


@pytest.mark.regression("30187")
def test_query_installed_when_package_unknown(database, tmpdir):
    """Test that we can query the installation status of a spec
    when we don't know its package.py
    """
    with spack.repo.use_repositories(spack.repo.MockRepositoryBuilder(tmpdir).root):
        specs = database.query("mpileaks")
        for s in specs:
            # Assert that we can query the installation methods even though we
            # don't have the package.py available
            assert s.installed
            assert not s.installed_upstream
            with pytest.raises(spack.repo.UnknownNamespaceError):
                s.package


def test_error_message_when_using_too_new_db(database, monkeypatch):
    """Sometimes the database format needs to be bumped. When that happens, we have forward
    incompatibilities that need to be reported in a clear way to the user, in case we moved
    back to an older version of Spack. This test ensures that the error message for a too
    new database version stays comprehensible across refactoring of the database code.
    """
    monkeypatch.setattr(spack.database, "_DB_VERSION", vn.Version("0"))
    with pytest.raises(
        spack.database.InvalidDatabaseVersionError, match="you need a newer Spack version"
    ):
        spack.database.Database(database.root)._read()


@pytest.mark.parametrize(
    "lock_cfg",
    [spack.database.NO_LOCK, spack.database.NO_TIMEOUT, spack.database.DEFAULT_LOCK_CFG, None],
)
def test_database_construction_doesnt_use_globals(tmpdir, config, nullify_globals, lock_cfg):
    lock_cfg = lock_cfg or spack.database.lock_configuration(config)
    db = spack.database.Database(str(tmpdir), lock_cfg=lock_cfg)
    assert os.path.exists(db.database_directory)


def test_database_read_works_with_trailing_data(tmp_path, default_mock_concretization):
    # Populate a database
    root = str(tmp_path)
    db = spack.database.Database(root, layout=None)
    spec = default_mock_concretization("pkg-a")
    db.add(spec)
    specs_in_db = db.query_local()
    assert spec in specs_in_db

    # Append anything to the end of the database file
    with open(db._index_path, "a") as f:
        f.write(json.dumps({"hello": "world"}))

    # Read the database and check that it ignores the trailing data
    assert spack.database.Database(root).query_local() == specs_in_db


def test_database_errors_with_just_a_version_key(tmp_path):
    root = str(tmp_path)
    db = spack.database.Database(root)
    next_version = f"{spack.database._DB_VERSION}.next"
    with open(db._index_path, "w") as f:
        f.write(json.dumps({"database": {"version": next_version}}))

    with pytest.raises(spack.database.InvalidDatabaseVersionError):
        spack.database.Database(root).query_local()


def test_reindex_with_upstreams(tmp_path, monkeypatch, mock_packages, config):
    # Reindexing should not put install records of upstream entries into the local database. Here
    # we install `mpileaks` locally with dependencies in the upstream. And we even install
    # `mpileaks` with the same hash in the upstream. After reindexing, `mpileaks` should still be
    # in the local db, and `callpath` should not.
    mpileaks = spack.spec.Spec("mpileaks").concretized()
    callpath = mpileaks.dependencies("callpath")[0]

    upstream_store = spack.store.create(
        {"config": {"install_tree": {"root": str(tmp_path / "upstream")}}}
    )
    monkeypatch.setattr(spack.store, "STORE", upstream_store)
    PackageInstaller([callpath.package], fake=True, explicit=True).install()

    local_store = spack.store.create(
        {
            "config": {"install_tree": {"root": str(tmp_path / "local")}},
            "upstreams": {"my-upstream": {"install_tree": str(tmp_path / "upstream")}},
        }
    )
    monkeypatch.setattr(spack.store, "STORE", local_store)
    PackageInstaller([mpileaks.package], fake=True, explicit=True).install()

    # Sanity check that callpath is from upstream.
    assert not local_store.db.query_local("callpath")
    assert local_store.db.query("callpath")

    # Install mpileaks also upstream with the same hash to ensure that determining upstreamness
    # checks local installs before upstream databases, even when the local database is being
    # reindexed.
    monkeypatch.setattr(spack.store, "STORE", upstream_store)
    PackageInstaller([mpileaks.package], fake=True, explicit=True).install()

    # Delete the local database
    shutil.rmtree(local_store.db.database_directory)

    # Create a new instance s.t. we don't have cached specs in memory
    reindexed_local_store = spack.store.create(
        {
            "config": {"install_tree": {"root": str(tmp_path / "local")}},
            "upstreams": {"my-upstream": {"install_tree": str(tmp_path / "upstream")}},
        }
    )
    reindexed_local_store.db.reindex()

    assert not reindexed_local_store.db.query_local("callpath")
    assert reindexed_local_store.db.query("callpath") == [callpath]
    assert reindexed_local_store.db.query_local("mpileaks") == [mpileaks]
