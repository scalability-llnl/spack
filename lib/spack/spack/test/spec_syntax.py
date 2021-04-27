# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import pytest
import shlex

import llnl.util.filesystem as fs

import spack.hash_types as ht
import spack.repo
import spack.store
import spack.spec as sp
from spack.parse import Token
from spack.spec import Spec
from spack.spec import SpecParseError, RedundantSpecError
from spack.spec import AmbiguousHashError, InvalidHashError, NoSuchHashError
from spack.spec import DuplicateArchitectureError
from spack.spec import DuplicateDependencyError, DuplicateCompilerSpecError
from spack.spec import SpecFilenameError, NoSuchSpecFileError
from spack.spec import MultipleVersionError
from spack.variant import DuplicateVariantError


# Sample output for a complex lexing.
complex_lex = [Token(sp.ID, 'mvapich_foo'),
               Token(sp.DEP),
               Token(sp.ID, '_openmpi'),
               Token(sp.AT),
               Token(sp.ID, '1.2'),
               Token(sp.COLON),
               Token(sp.ID, '1.4'),
               Token(sp.COMMA),
               Token(sp.ID, '1.6'),
               Token(sp.PCT),
               Token(sp.ID, 'intel'),
               Token(sp.AT),
               Token(sp.ID, '12.1'),
               Token(sp.COLON),
               Token(sp.ID, '12.6'),
               Token(sp.ON),
               Token(sp.ID, 'debug'),
               Token(sp.OFF),
               Token(sp.ID, 'qt_4'),
               Token(sp.DEP),
               Token(sp.ID, 'stackwalker'),
               Token(sp.AT),
               Token(sp.ID, '8.1_1e')]

# Another sample lexer output with a kv pair.
kv_lex = [Token(sp.ID, 'mvapich_foo'),
          Token(sp.ID, 'debug'),
          Token(sp.EQ),
          Token(sp.VAL, '4'),
          Token(sp.DEP),
          Token(sp.ID, '_openmpi'),
          Token(sp.AT),
          Token(sp.ID, '1.2'),
          Token(sp.COLON),
          Token(sp.ID, '1.4'),
          Token(sp.COMMA),
          Token(sp.ID, '1.6'),
          Token(sp.PCT),
          Token(sp.ID, 'intel'),
          Token(sp.AT),
          Token(sp.ID, '12.1'),
          Token(sp.COLON),
          Token(sp.ID, '12.6'),
          Token(sp.ON),
          Token(sp.ID, 'debug'),
          Token(sp.OFF),
          Token(sp.ID, 'qt_4'),
          Token(sp.DEP),
          Token(sp.ID, 'stackwalker'),
          Token(sp.AT),
          Token(sp.ID, '8.1_1e')]


class TestSpecSyntax(object):
    # ========================================================================
    # Parse checks
    # ========================================================================

    def check_parse(self, expected, spec=None):
        """Assert that the provided spec is able to be parsed.

           If this is called with one argument, it assumes that the
           string is canonical (i.e., no spaces and ~ instead of - for
           variants) and that it will convert back to the string it came
           from.

           If this is called with two arguments, the first argument is
           the expected canonical form and the second is a non-canonical
           input to be parsed.

        """
        if spec is None:
            spec = expected
        output = sp.parse(spec)

        parsed = (" ".join(str(spec) for spec in output))
        assert expected == parsed

    def check_lex(self, tokens, spec):
        """Check that the provided spec parses to the provided token list."""
        spec = shlex.split(str(spec))
        lex_output = sp.SpecLexer().lex(spec)
        assert len(tokens) == len(lex_output), "unexpected number of tokens"
        for tok, spec_tok in zip(tokens, lex_output):
            if tok.type == sp.ID or tok.type == sp.VAL:
                assert tok == spec_tok
            else:
                # Only check the type for non-identifiers.
                assert tok.type == spec_tok.type

    def _check_raises(self, exc_type, items):
        for item in items:
            with pytest.raises(exc_type):
                print("CHECKING: ", item, "=======================")
                Spec(item)

    # ========================================================================
    # Parse checks
    # ========================================================================
    def test_package_names(self):
        self.check_parse("mvapich")
        self.check_parse("mvapich_foo")
        self.check_parse("_mvapich_foo")

    def test_anonymous_specs(self):
        self.check_parse("%intel")
        self.check_parse("@2.7")
        self.check_parse("^zlib")
        self.check_parse("+foo")
        self.check_parse("arch=test-None-None", "platform=test")
        self.check_parse('@2.7:')

    def test_anonymous_specs_with_multiple_parts(self):
        # Parse anonymous spec with multiple tokens
        self.check_parse('@4.2: languages=go', 'languages=go @4.2:')
        self.check_parse('@4.2: languages=go')

    def test_simple_dependence(self):
        self.check_parse("openmpi ^hwloc")
        self.check_parse("openmpi ^hwloc", "openmpi^hwloc")

        self.check_parse("openmpi ^hwloc ^libunwind")
        self.check_parse("openmpi ^hwloc ^libunwind",
                         "openmpi^hwloc^libunwind")

    def test_version_after_compiler(self):
        self.check_parse('foo@2.0%bar@1.0', 'foo %bar@1.0 @2.0')

    def test_dependencies_with_versions(self):
        self.check_parse("openmpi ^hwloc@1.2e6")
        self.check_parse("openmpi ^hwloc@1.2e6:")
        self.check_parse("openmpi ^hwloc@:1.4b7-rc3")
        self.check_parse("openmpi ^hwloc@1.2e6:1.4b7-rc3")

    def test_multiple_specs(self):
        self.check_parse("mvapich emacs")

    def test_multiple_specs_after_kv(self):
        self.check_parse('mvapich cppflags="-O3 -fPIC" emacs')
        self.check_parse('mvapich cflags="-O3" emacs',
                         'mvapich cflags=-O3 emacs')

    def test_multiple_specs_long_second(self):
        self.check_parse('mvapich emacs@1.1.1%intel cflags="-O3"',
                         'mvapich emacs @1.1.1 %intel cflags=-O3')
        self.check_parse('mvapich cflags="-O3 -fPIC" emacs ^ncurses%intel')
        self.check_parse('mvapich cflags="-O3 -fPIC" emacs ^ncurses%intel',
                         'mvapich cflags="-O3 -fPIC" emacs^ncurses%intel')

    def test_full_specs(self):
        self.check_parse(
            "mvapich_foo"
            " ^_openmpi@1.2:1.4,1.6%intel@12.1+debug~qt_4"
            " ^stackwalker@8.1_1e")
        self.check_parse(
            "mvapich_foo"
            " ^_openmpi@1.2:1.4,1.6%intel@12.1~qt_4 debug=2"
            " ^stackwalker@8.1_1e")
        self.check_parse(
            'mvapich_foo'
            ' ^_openmpi@1.2:1.4,1.6%intel@12.1 cppflags="-O3" +debug~qt_4'
            ' ^stackwalker@8.1_1e')
        self.check_parse(
            "mvapich_foo"
            " ^_openmpi@1.2:1.4,1.6%intel@12.1~qt_4 debug=2"
            " ^stackwalker@8.1_1e arch=test-redhat6-x86")

    def test_yaml_specs(self):
        self.check_parse(
            "yaml-cpp@0.1.8%intel@12.1"
            " ^boost@3.1.4")
        tempspec = r"builtin.yaml-cpp%gcc"
        self.check_parse(
            tempspec.strip("builtin."),
            spec=tempspec)
        tempspec = r"testrepo.yaml-cpp%gcc"
        self.check_parse(
            tempspec.strip("testrepo."),
            spec=tempspec)
        tempspec = r"builtin.yaml-cpp@0.1.8%gcc"
        self.check_parse(
            tempspec.strip("builtin."),
            spec=tempspec)
        tempspec = r"builtin.yaml-cpp@0.1.8%gcc@7.2.0"
        self.check_parse(
            tempspec.strip("builtin."),
            spec=tempspec)
        tempspec = r"builtin.yaml-cpp@0.1.8%gcc@7.2.0" \
            r" ^boost@3.1.4"
        self.check_parse(
            tempspec.strip("builtin."),
            spec=tempspec)

    def test_canonicalize(self):
        self.check_parse(
            "mvapich_foo"
            " ^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4"
            " ^stackwalker@8.1_1e",

            "mvapich_foo "
            "^_openmpi@1.6,1.2:1.4%intel@12.1:12.6+debug~qt_4 "
            "^stackwalker@8.1_1e")

        self.check_parse(
            "mvapich_foo"
            " ^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4"
            " ^stackwalker@8.1_1e",

            "mvapich_foo "
            "^stackwalker@8.1_1e "
            "^_openmpi@1.6,1.2:1.4%intel@12.1:12.6~qt_4+debug")

        self.check_parse(
            "x ^y@1,2:3,4%intel@1,2,3,4+a~b+c~d+e~f",
            "x ^y~f+e~d+c~b+a@4,2:3,1%intel@4,3,2,1")

        self.check_parse(
            "x arch=test-redhat6-None"
            " ^y arch=test-None-core2"
            " ^z arch=linux-None-None",

            "x os=fe "
            "^y target=be "
            "^z platform=linux")

        self.check_parse(
            "x arch=test-debian6-core2"
            " ^y arch=test-debian6-core2",

            "x os=default_os target=default_target"
            " ^y os=default_os target=default_target")

        self.check_parse("x ^y", "x@: ^y@:")

    def test_parse_errors(self):
        errors = ['x@@1.2', 'x ^y@@1.2', 'x@1.2::', 'x::']
        self._check_raises(SpecParseError, errors)

    def _check_hash_parse(self, spec):
        """Check several ways to specify a spec by hash."""
        # full hash
        self.check_parse(str(spec), '/' + spec.dag_hash())

        # partial hash
        self.check_parse(str(spec), '/ ' + spec.dag_hash()[:5])

        # name + hash
        self.check_parse(str(spec), spec.name + '/' + spec.dag_hash())

        # name + version + space + partial hash
        self.check_parse(
            str(spec), spec.name + '@' + str(spec.version) +
            ' /' + spec.dag_hash()[:6])

    @pytest.mark.db
    def test_spec_by_hash(self, database):
        specs = database.query()
        assert len(specs)  # make sure something's in the DB

        for spec in specs:
            self._check_hash_parse(spec)

    @pytest.mark.db
    def test_dep_spec_by_hash(self, database):
        mpileaks_zmpi = database.query_one('mpileaks ^zmpi')
        zmpi = database.query_one('zmpi')
        fake = database.query_one('fake')

        assert 'fake' in mpileaks_zmpi
        assert 'zmpi' in mpileaks_zmpi

        mpileaks_hash_fake = sp.Spec('mpileaks ^/' + fake.dag_hash())
        assert 'fake' in mpileaks_hash_fake
        assert mpileaks_hash_fake['fake'] == fake

        mpileaks_hash_zmpi = sp.Spec(
            'mpileaks %' + str(mpileaks_zmpi.compiler) +
            ' ^ / ' + zmpi.dag_hash())
        assert 'zmpi' in mpileaks_hash_zmpi
        assert mpileaks_hash_zmpi['zmpi'] == zmpi
        assert mpileaks_hash_zmpi.compiler == mpileaks_zmpi.compiler

        mpileaks_hash_fake_and_zmpi = sp.Spec(
            'mpileaks ^/' + fake.dag_hash()[:4] + '^ / ' + zmpi.dag_hash()[:5])
        assert 'zmpi' in mpileaks_hash_fake_and_zmpi
        assert mpileaks_hash_fake_and_zmpi['zmpi'] == zmpi

        assert 'fake' in mpileaks_hash_fake_and_zmpi
        assert mpileaks_hash_fake_and_zmpi['fake'] == fake

    @pytest.mark.db
    def test_multiple_specs_with_hash(self, database):
        mpileaks_zmpi = database.query_one('mpileaks ^zmpi')
        callpath_mpich2 = database.query_one('callpath ^mpich2')

        # name + hash + separate hash
        specs = sp.parse('mpileaks /' + mpileaks_zmpi.dag_hash() +
                         '/' + callpath_mpich2.dag_hash())
        assert len(specs) == 2

        # 2 separate hashes
        specs = sp.parse('/' + mpileaks_zmpi.dag_hash() +
                         '/' + callpath_mpich2.dag_hash())
        assert len(specs) == 2

        # 2 separate hashes + name
        specs = sp.parse('/' + mpileaks_zmpi.dag_hash() +
                         '/' + callpath_mpich2.dag_hash() +
                         ' callpath')
        assert len(specs) == 3

        # hash + 2 names
        specs = sp.parse('/' + mpileaks_zmpi.dag_hash() +
                         ' callpath' +
                         ' callpath')
        assert len(specs) == 3

        # hash + name + hash
        specs = sp.parse('/' + mpileaks_zmpi.dag_hash() +
                         ' callpath' +
                         ' / ' + callpath_mpich2.dag_hash())
        assert len(specs) == 2

    @pytest.mark.db
    def test_ambiguous_hash(self, mutable_database):
        x1 = Spec('a')
        x1.concretize()
        x1._hash = 'xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
        x2 = Spec('a')
        x2.concretize()
        x2._hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        mutable_database.add(x1, spack.store.layout)
        mutable_database.add(x2, spack.store.layout)

        # ambiguity in first hash character
        self._check_raises(AmbiguousHashError, ['/x'])

        # ambiguity in first hash character AND spec name
        self._check_raises(AmbiguousHashError, ['a/x'])

    @pytest.mark.db
    def test_invalid_hash(self, database):
        mpileaks_zmpi = database.query_one('mpileaks ^zmpi')
        zmpi = database.query_one('zmpi')

        mpileaks_mpich = database.query_one('mpileaks ^mpich')
        mpich = database.query_one('mpich')

        # name + incompatible hash
        self._check_raises(InvalidHashError, [
            'zmpi /' + mpich.dag_hash(),
            'mpich /' + zmpi.dag_hash()])

        # name + dep + incompatible hash
        self._check_raises(InvalidHashError, [
            'mpileaks ^mpich /' + mpileaks_zmpi.dag_hash(),
            'mpileaks ^zmpi /' + mpileaks_mpich.dag_hash()])

    @pytest.mark.db
    def test_nonexistent_hash(self, database):
        """Ensure we get errors for nonexistant hashes."""
        specs = database.query()

        # This hash shouldn't be in the test DB.  What are the odds :)
        no_such_hash = 'aaaaaaaaaaaaaaa'
        hashes = [s._hash for s in specs]
        assert no_such_hash not in [h[:len(no_such_hash)] for h in hashes]

        self._check_raises(NoSuchHashError, [
            '/' + no_such_hash,
            'mpileaks /' + no_such_hash])

    @pytest.mark.db
    def test_redundant_spec(self, database):
        """Check that redundant spec constraints raise errors.

        TODO (TG): does this need to be an error? Or should concrete
        specs only raise errors if constraints cause a contradiction?

        """
        mpileaks_zmpi = database.query_one('mpileaks ^zmpi')
        callpath_zmpi = database.query_one('callpath ^zmpi')
        dyninst = database.query_one('dyninst')

        mpileaks_mpich2 = database.query_one('mpileaks ^mpich2')

        redundant_specs = [
            # redudant compiler
            '/' + mpileaks_zmpi.dag_hash() + '%' + str(mpileaks_zmpi.compiler),

            # redudant version
            'mpileaks/' + mpileaks_mpich2.dag_hash() +
            '@' + str(mpileaks_mpich2.version),

            # redundant dependency
            'callpath /' + callpath_zmpi.dag_hash() + '^ libelf',

            # redundant flags
            '/' + dyninst.dag_hash() + ' cflags="-O3 -fPIC"']

        self._check_raises(RedundantSpecError, redundant_specs)

    def test_duplicate_variant(self):
        duplicates = [
            'x@1.2+debug+debug',
            'x ^y@1.2+debug debug=true',
            'x ^y@1.2 debug=false debug=true',
            'x ^y@1.2 debug=false ~debug'
        ]
        self._check_raises(DuplicateVariantError, duplicates)

    def test_multiple_versions(self):
        multiples = [
            'x@1.2@2.3',
            'x@1.2:2.3@1.4',
            'x@1.2@2.3:2.4',
            'x@1.2@2.3,2.4',
            'x@1.2 +foo~bar @2.3',
            'x@1.2%y@1.2@2.3:2.4',
        ]
        self._check_raises(MultipleVersionError, multiples)

    def test_duplicate_dependency(self):
        self._check_raises(DuplicateDependencyError, ["x ^y ^y"])

    def test_duplicate_compiler(self):
        duplicates = [
            "x%intel%intel",
            "x%intel%gcc",
            "x%gcc%intel",
            "x ^y%intel%intel",
            "x ^y%intel%gcc",
            "x ^y%gcc%intel"
        ]
        self._check_raises(DuplicateCompilerSpecError, duplicates)

    def test_duplicate_architecture(self):
        duplicates = [
            "x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64",
            "x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le",
            "x arch=linux-rhel7-ppc64le arch=linux-rhel7-x86_64",
            "y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64",
            "y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le"
        ]
        self._check_raises(DuplicateArchitectureError, duplicates)

    def test_duplicate_architecture_component(self):
        duplicates = [
            "x os=fe os=fe",
            "x os=fe os=be",
            "x target=fe target=fe",
            "x target=fe target=be",
            "x platform=test platform=test",
            "x os=fe platform=test target=fe os=fe",
            "x target=be platform=test os=be os=fe"
        ]
        self._check_raises(DuplicateArchitectureError, duplicates)

    @pytest.mark.usefixtures('config')
    def test_parse_yaml_simple(self, mock_packages, tmpdir):
        s = Spec('libdwarf')
        s.concretize()

        specfile = tmpdir.join('libdwarf.yaml')

        with specfile.open('w') as f:
            f.write(s.to_yaml(hash=ht.build_hash))

        # Check an absolute path to spec.yaml by itself:
        #     "spack spec /path/to/libdwarf.yaml"
        specs = sp.parse(specfile.strpath)
        assert len(specs) == 1

        # Check absolute path to spec.yaml mixed with a clispec, e.g.:
        #     "spack spec mvapich_foo /path/to/libdwarf.yaml"
        specs = sp.parse('mvapich_foo {0}'.format(specfile.strpath))
        assert len(specs) == 2

    @pytest.mark.usefixtures('config')
    def test_parse_filename_missing_slash_as_spec(self, mock_packages, tmpdir):
        """Ensure that libelf.yaml parses as a spec, NOT a file."""
        s = Spec('libelf')
        s.concretize()

        specfile = tmpdir.join('libelf.yaml')

        # write the file to the current directory to make sure it exists,
        # and that we still do not parse the spec as a file.
        with specfile.open('w') as f:
            f.write(s.to_yaml(hash=ht.build_hash))

        # Check the spec `libelf.yaml` in the working directory, which
        # should evaluate to a spec called `yaml` in the `libelf`
        # namespace, NOT a spec for `libelf`.
        with tmpdir.as_cwd():
            specs = sp.parse("libelf.yaml")
        assert len(specs) == 1

        spec = specs[0]
        assert spec.name == "yaml"
        assert spec.namespace == "libelf"
        assert spec.fullname == "libelf.yaml"

        # check that if we concretize this spec, we get a good error
        # message that mentions we might've meant a file.
        with pytest.raises(spack.repo.UnknownPackageError) as exc_info:
            spec.concretize()
        assert exc_info.value.long_message
        assert ("Did you mean to specify a filename with './libelf.yaml'?"
                in exc_info.value.long_message)

        # make sure that only happens when the spec ends in yaml
        with pytest.raises(spack.repo.UnknownPackageError) as exc_info:
            Spec('builtin.mock.doesnotexist').concretize()
        assert (
            not exc_info.value.long_message or (
                "Did you mean to specify a filename with" not in
                exc_info.value.long_message
            )
        )

    @pytest.mark.usefixtures('config')
    def test_parse_yaml_dependency(self, mock_packages, tmpdir):
        s = Spec('libdwarf')
        s.concretize()

        specfile = tmpdir.join('libelf.yaml')

        with specfile.open('w') as f:
            f.write(s['libelf'].to_yaml(hash=ht.build_hash))

        # Make sure we can use yaml path as dependency, e.g.:
        #     "spack spec libdwarf ^ /path/to/libelf.yaml"
        specs = sp.parse('libdwarf ^ {0}'.format(specfile.strpath))
        assert len(specs) == 1

    @pytest.mark.usefixtures('config')
    def test_parse_yaml_relative_paths(self, mock_packages, tmpdir):
        s = Spec('libdwarf')
        s.concretize()

        specfile = tmpdir.join('libdwarf.yaml')

        with specfile.open('w') as f:
            f.write(s.to_yaml(hash=ht.build_hash))

        file_name = specfile.basename
        parent_dir = os.path.basename(specfile.dirname)

        # Relative path to specfile
        with fs.working_dir(specfile.dirname):
            # Test for command like: "spack spec libelf.yaml"
            # This should parse a single spec, but should not concretize.
            # See test_parse_filename_missing_slash_as_spec()
            specs = sp.parse('{0}'.format(file_name))
            assert len(specs) == 1

            # Make sure this also works: "spack spec ./libelf.yaml"
            specs = sp.parse('./{0}'.format(file_name))
            assert len(specs) == 1

            # Should also be accepted: "spack spec ../<cur-dir>/libelf.yaml"
            specs = sp.parse('../{0}/{1}'.format(parent_dir, file_name))
            assert len(specs) == 1

            # Should also handle mixed clispecs and relative paths, e.g.:
            #     "spack spec mvapich_foo ../<cur-dir>/libelf.yaml"
            specs = sp.parse('mvapich_foo ../{0}/{1}'.format(
                parent_dir, file_name))
            assert len(specs) == 2

    @pytest.mark.usefixtures('config')
    def test_parse_yaml_relative_subdir_path(self, mock_packages, tmpdir):
        s = Spec('libdwarf')
        s.concretize()

        specfile = tmpdir.mkdir('subdir').join('libdwarf.yaml')

        with specfile.open('w') as f:
            f.write(s.to_yaml(hash=ht.build_hash))

        file_name = specfile.basename

        # Relative path to specfile
        with tmpdir.as_cwd():
            assert os.path.exists('subdir/{0}'.format(file_name))

            # Test for command like: "spack spec libelf.yaml"
            specs = sp.parse('subdir/{0}'.format(file_name))
            assert len(specs) == 1

    @pytest.mark.usefixtures('config')
    def test_parse_yaml_dependency_relative_paths(self, mock_packages, tmpdir):
        s = Spec('libdwarf')
        s.concretize()

        specfile = tmpdir.join('libelf.yaml')

        with specfile.open('w') as f:
            f.write(s['libelf'].to_yaml(hash=ht.build_hash))

        file_name = specfile.basename
        parent_dir = os.path.basename(specfile.dirname)

        # Relative path to specfile
        with fs.working_dir(specfile.dirname):
            # Test for command like: "spack spec libelf.yaml"
            specs = sp.parse('libdwarf^{0}'.format(file_name))
            assert len(specs) == 1

            # Make sure this also works: "spack spec ./libelf.yaml"
            specs = sp.parse('libdwarf^./{0}'.format(file_name))
            assert len(specs) == 1

            # Should also be accepted: "spack spec ../<cur-dir>/libelf.yaml"
            specs = sp.parse('libdwarf^../{0}/{1}'.format(
                parent_dir, file_name))
            assert len(specs) == 1

    def test_parse_yaml_error_handling(self):
        self._check_raises(NoSuchSpecFileError, [
            # Single spec that looks like a yaml path
            '/bogus/path/libdwarf.yaml',
            '../../libdwarf.yaml',
            './libdwarf.yaml',
            # Dependency spec that looks like a yaml path
            'libdwarf^/bogus/path/libelf.yaml',
            'libdwarf ^../../libelf.yaml',
            'libdwarf^ ./libelf.yaml',
            # Multiple specs, one looks like a yaml path
            'mvapich_foo /bogus/path/libelf.yaml',
            'mvapich_foo ../../libelf.yaml',
            'mvapich_foo ./libelf.yaml',
        ])

    def test_nice_error_for_no_space_after_spec_filename(self):
        """Ensure that omitted spaces don't give weird errors about hashes."""
        self._check_raises(SpecFilenameError, [
            '/bogus/path/libdwarf.yamlfoobar',
            'libdwarf^/bogus/path/libelf.yamlfoobar ^/path/to/bogus.yaml',
        ])

    @pytest.mark.usefixtures('config')
    def test_yaml_spec_not_filename(self, mock_packages, tmpdir):
        with pytest.raises(spack.repo.UnknownPackageError):
            Spec('builtin.mock.yaml').concretize()

        with pytest.raises(spack.repo.UnknownPackageError):
            Spec('builtin.mock.yamlfoobar').concretize()

    @pytest.mark.usefixtures('config')
    def test_parse_yaml_variant_error(self, mock_packages, tmpdir):
        s = Spec('a')
        s.concretize()

        specfile = tmpdir.join('a.yaml')

        with specfile.open('w') as f:
            f.write(s.to_yaml(hash=ht.build_hash))

        with pytest.raises(RedundantSpecError):
            # Trying to change a variant on a concrete spec is an error
            sp.parse('{0} ~bvv'.format(specfile.strpath))

    # ========================================================================
    # Lex checks
    # ========================================================================
    def test_ambiguous(self):
        # This first one is ambiguous because - can be in an identifier AND
        # indicate disabling an option.
        with pytest.raises(AssertionError):
            self.check_lex(
                complex_lex,
                "mvapich_foo"
                "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug-qt_4"
                "^stackwalker@8.1_1e"
            )

    # The following lexes are non-ambiguous (add a space before -qt_4)
    # and should all result in the tokens in complex_lex
    def test_minimal_spaces(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug -qt_4"
            "^stackwalker@8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo"
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4"
            "^stackwalker@8.1_1e")

    def test_spaces_between_dependences(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug -qt_4 "
            "^stackwalker @ 8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^_openmpi@1.2:1.4,1.6%intel@12.1:12.6+debug~qt_4 "
            "^stackwalker @ 8.1_1e")

    def test_spaces_between_options(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^_openmpi @1.2:1.4,1.6 %intel @12.1:12.6 +debug -qt_4 "
            "^stackwalker @8.1_1e")

    def test_way_too_many_spaces(self):
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            complex_lex,
            "mvapich_foo "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug ~ qt_4 "
            "^ stackwalker @ 8.1_1e")

    def test_kv_with_quotes(self):
        self.check_lex(
            kv_lex,
            "mvapich_foo debug='4' "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            'mvapich_foo debug="4" '
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            "mvapich_foo 'debug = 4' "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")

    def test_kv_without_quotes(self):
        self.check_lex(
            kv_lex,
            "mvapich_foo debug=4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")

    def test_kv_with_spaces(self):
        self.check_lex(
            kv_lex,
            "mvapich_foo debug = 4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            "mvapich_foo debug =4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")
        self.check_lex(
            kv_lex,
            "mvapich_foo debug= 4 "
            "^ _openmpi @1.2 : 1.4 , 1.6 % intel @ 12.1 : 12.6 + debug - qt_4 "
            "^ stackwalker @ 8.1_1e")

    @pytest.mark.parametrize('expected_tokens,spec_string', [
        ([Token(sp.ID, 'target'),
          Token(sp.EQ, '='),
          Token(sp.VAL, 'broadwell')],
         'target=broadwell'),
        ([Token(sp.ID, 'target'),
          Token(sp.EQ, '='),
          Token(sp.VAL, ':broadwell,icelake')],
         'target=:broadwell,icelake')
    ])
    def test_target_tokenization(self, expected_tokens, spec_string):
        self.check_lex(expected_tokens, spec_string)

    @pytest.mark.regression('20310')
    def test_compare_abstract_specs(self):
        """Spec comparisons must be valid for abstract specs.

        Check that the spec cmp_key appropriately handles comparing specs for
        which some attributes are None in exactly one of two specs"""
        # Add fields in order they appear in `Spec._cmp_node`
        constraints = [
            None,
            'foo',
            'foo.foo',
            'foo.foo@foo',
            'foo.foo@foo+foo',
            'foo.foo@foo+foo arch=foo-foo-foo',
            'foo.foo@foo+foo arch=foo-foo-foo %foo',
            'foo.foo@foo+foo arch=foo-foo-foo %foo cflags=foo',
        ]
        specs = [Spec(s) for s in constraints]

        for a, b in itertools.product(specs, repeat=2):
            # Check that we can compare without raising an error
            assert a <= b or b < a
