# v0.16.1 (2021-02-22)

This minor release includes a new feature and associated fixes:
* intel-oneapi support through new packages (#20411, #20686, #20693, #20717,
  #20732, #20808, #21377, #21448)

This release also contains bug fixes/enhancements for:
* HIP/ROCm support (#19715, #20095)
* concretization (#19988, #20020, #20082, #20086, #20099, #20102, #20128,
  #20182, #20193, #20194, #20196, #20203, #20247, #20259, #20307, #20362,
  #20383, #20423, #20473, #20506, #20507, #20604, #20638, #20649, #20677,
  #20680, #20790)
* environment install reporting fix (#20004)
* avoid import in ABI compatibility info (#20236)
* restore ability of dev-build to skip patches (#20351)
* spack find -d spec grouping (#20028)
* spack smoke test support (#19987, #20298)
* macOS fixes (#20038, #21662)
* abstract spec comparisons (#20341)
* continuous integration (#17563)
* performance improvements for binary relocation (#19690, #20768)
* additional sanity checks for variants in builtin packages (#20373)
* do not pollute auto-generated configuration files with empty lists or
  dicts (#20526)

plus assorted documentation (#20021, #20174) and package bug fixes/enhancements
(#19617, #19933, #19986, #20006, #20097, #20198, #20794, #20906, #21411).


# v0.16.0 (2020-11-18)

`v0.16.0` is a major feature release.

## Major features in this release

1. **New concretizer (experimental)** Our new backtracking concretizer is
   now in Spack as an experimental feature. You will need to install
   `clingo@master+python` and set `concretizer: clingo` in `config.yaml`
   to use it. The original concretizer is not exhaustive and is not
   guaranteed to find a solution if one exists. We encourage you to use
   the new concretizer and to report any bugs you find with it. We
   anticipate making the new concretizer the default and including all
   required dependencies for it in Spack `v0.17`. For more details, see
   #19501.

2. **spack test (experimental)** Users can add `test()` methods to their
   packages to run smoke tests on installations with the new `spack test`
   command (the old `spack test` is now `spack unit-test`). `spack test`
   is environment-aware, so you can `spack install` an environment and
   `spack test run` smoke tests on all of its packages. Historical test
   logs can be perused with `spack test results`. Generic smoke tests for
   MPI implementations, C, C++, and Fortran compilers as well as specific
   smoke tests for 18 packages. This is marked experimental because the
   test API (`self.run_test()`) is likely to be change, but we encourage
   users to upstream tests, and we will maintain and refactor any that
   are added to mainline packages (#15702).

3. **spack develop** New `spack develop` command allows you to develop
   several packages at once within a Spack environment. Running
   `spack develop foo@v1` and `spack develop bar@v2` will check
    out specific versions of `foo` and `bar` into subdirectories, which you
    can then build incrementally with `spack install ` (#15256).

4. **More parallelism** Spack previously installed the dependencies of a
   _single_ spec in parallel. Entire environments can now be installed in
   parallel, greatly accelerating builds of large environments. get
   parallelism from individual specs. Spack now parallelizes entire
   environment builds (#18131).

5. **Customizable base images for spack containerize**
    `spack containerize` previously only output a `Dockerfile` based
    on `ubuntu`. You may now specify any base image of your choosing (#15028).

6. **more external finding** `spack external find` was added in `v0.15`,
   but only `cmake` had support. `spack external find` can now find
   `bison`, `cuda`, `findutils`, `flex`, `git`, `lustre` `m4`, `mpich`,
   `mvapich2`, `ncurses`, `openmpi`, `perl`, `spectrum-mpi`, `tar`, and
   `texinfo` on your system and add them automatically to
   `packages.yaml`.

7. **Support aocc, nvhpc, and oneapi compilers** We are aggressively
   pursuing support for the newest vendor compilers, especially those for
   the U.S. exascale and pre-exascale systems. Compiler classes and
   auto-detection for `aocc`, `nvhpc`, `oneapi` are now in Spack (#19345,
   #19294, #19330).

## Additional new features of note

* New `spack mark` command can be used to designate packages as explicitly
  installed, so that `spack gc` will not garbage-collect them (#16662).
* `install_tree` can be customized with Spack's projection format (#18341)
* `sbang` now lives in the `install_tree` so that all users can access it (#11598)
* `csh` and `tcsh` users no longer need to set `SPACK_ROOT` before
  sourcing `setup-env.csh` (#18225)
* Spec syntax now supports `variant=*` syntax for finding any package
  that has a particular variant (#19381).
* Spack respects `SPACK_GNUPGHOME` variable for custom GPG directories (#17139)
* Spack now recognizes Graviton chips

## Major refactors

* Use spawn instead of fork on Python >= 3.8 on macOS (#18205)
* Use indexes for public build caches (#19101, #19117, #19132, #19141,  #19209)
* `sbang` is an external package now (https://github.com/spack/sbang, #19582)
* `archspec` is an external package now (https://github.com/archspec/archspec, #19600)

## Deprecations and Removals

* `spack bootstrap` was deprecated in v0.14.0, and has now been removed.
* `spack setup` is deprecated as of v0.16.0.
* What was `spack test` is now called `spack unit-test`. `spack test` is
  now the smoke testing feature in (2) above.

## Bugfixes

Some of the most notable bugfixes in this release include:

* Better warning messages for deprecated syntax in `packages.yaml` (#18013)
* `buildcache list --allarch` now works properly (#17827)
* Many fixes and tests for buildcaches and binary relcoation (#15687,
  *#17455, #17418, #17455, #15687, #18110)

## Package Improvements

Spack now has 5050 total packages, 720 of which were added since `v0.15`.

* ROCm packages (`hip`, `aomp`, more) added by AMD (#19957, #19832, others)
* Many improvements for ARM support
* `llvm-flang`, `flang`, and `f18` removed, as `llvm` has real `flang`
  support since Flang was merged to LLVM mainline
* Emerging support for `spack external find` and `spack test` in packages.

## Infrastructure

* Major infrastructure improvements to pipelines on `gitlab.spack.io`
* Support for testing PRs from forks (#19248) is being enabled for all
  forks to enable rolling, up-to-date binary builds on `develop`


# v0.15.4 (2020-08-12)

This release contains one feature addition:

* Users can set `SPACK_GNUPGHOME` to override Spack's GPG path (#17139)

Several bugfixes for CUDA, binary packaging, and `spack -V`:

* CUDA package's `.libs` method searches for `libcudart` instead of `libcuda` (#18000)
* Don't set `CUDAHOSTCXX` in environments that contain CUDA (#17826)
* `buildcache create`: `NoOverwriteException` is a warning, not an error (#17832)
* Fix `spack buildcache list --allarch` (#17884)
* `spack -V` works with `releases/latest` tag and shallow clones (#17884)

And fixes for GitHub Actions and tests to ensure that CI passes on the
release branch (#15687, #17279, #17328, #17377, #17732).

# v0.15.3 (2020-07-28)

This release contains the following bugfixes:

* Fix handling of relative view paths (#17721)
* Fixes for binary relocation (#17418, #17455)
* Fix redundant printing of error messages in build environment (#17709)

It also adds a support script for Spack tutorials:

* Add a tutorial setup script to share/spack (#17705, #17722)

# v0.15.2 (2020-07-23)

This minor release includes two new features:

* Spack install verbosity is decreased, and more debug levels are added (#17546)
* The $spack/share/spack/keys directory contains public keys that may be optionally trusted for public binary mirrors (#17684)

This release also includes several important fixes:

* MPICC and related variables are now cleand in the build environment (#17450)
* LLVM flang only builds CUDA offload components when +cuda (#17466)
* CI pipelines no longer upload user environments that can contain secrets to the internet (#17545)
* CI pipelines add bootstrapped compilers to the compiler config (#17536)
* `spack buildcache list` does not exit on first failure and lists later mirrors (#17565)
* Apple's "gcc" executable that is an apple-clang compiler does not generate a gcc compiler config (#17589)
* Mixed compiler toolchains are merged more naturally across different compiler suffixes (#17590)
* Cray Shasta platforms detect the OS properly (#17467)
* Additional more minor fixes.

# v0.15.1 (2020-07-10)

This minor release includes several important fixes:

* Fix shell support on Cray (#17386)
* Fix use of externals installed with other Spack instances (#16954)
* Fix gcc+binutils build (#9024)
* Fixes for usage of intel-mpi (#17378 and #17382)
* Fixes to Autotools config.guess detection (#17333 and #17356)
* Update `spack install` message to prompt user when an environment is not
  explicitly activated (#17454)

This release also adds a mirror for all sources that are
fetched in Spack (#17077). It is expected to be useful when the
official website for a Spack package is unavailable.

# v0.15.0 (2020-06-28)

`v0.15.0` is a major feature release.

## Major Features in this release

1. **Cray support** Spack will now work properly on Cray "Cluster"
systems (non XC systems) and after a `module purge` command on Cray
systems. See #12989

2. **Virtual package configuration** Virtual packages are allowed in
packages.yaml configuration. This allows users to specify a virtual
package as non-buildable without needing to specify for each
implementation. See #14934

3. **New config subcommands** This release adds `spack config add` and
`spack config remove` commands to add to and remove from yaml
configuration files from the CLI. See #13920

4. **Environment activation** Anonymous environments are **no longer**
automatically activated in the current working directory. To activate
an environment from a `spack.yaml` file in the current directory, use
the `spack env activate .` command. This removes a concern that users
were too easily polluting their anonymous environments with accidental
installations. See #17258

5. **Apple clang compiler** The clang compiler and the apple-clang
compiler are now separate compilers in Spack. This allows Spack to
improve support for the apple-clang compiler. See #17110

6. **Finding external packages** Spack packages can now support an API
for finding external installations. This allows the `spack external
find` command to automatically add installations of those packages to
the user's configuration. See #15158


## Additional new features of note

* support for using Spack with the fish shell (#9279)
* `spack load --first` option to load first match (instead of prompting user) (#15622)
* support the Cray cce compiler both new and classic versions (#17256, #12989)
* `spack dev-build` command:
  * supports stopping before a specified phase (#14699)
  * supports automatically launching a shell in the build environment (#14887)
* `spack install --fail-fast` allows builds to fail at the first error (rather than best-effort) (#15295)
* environments: SpecList references can be dereferenced as compiler or dependency constraints (#15245)
* `spack view` command: new support for a copy/relocate view type (#16480)
* ci pipelines: see documentation for several improvements
* `spack mirror -a` command now supports excluding packages (#14154)
* `spack buildcache create` is now environment-aware (#16580)
* module generation: more flexible format for specifying naming schemes (#16629)
* lmod module generation: packages can be configured as core specs for lmod hierarchy (#16517)

## Deprecations and Removals

The following commands were deprecated in v0.13.0, and have now been removed:

* `spack configure`
* `spack build`
* `spack diy`

The following commands were deprecated in v0.14.0, and will be removed in the next major release:

* `spack bootstrap`

## Bugfixes

Some of the most notable bugfixes in this release include:

* Spack environments can now contain the string `-h` (#15429)
* The `spack install` gracefully handles being backgrounded (#15723, #14682)
* Spack uses `-isystem` instead of `-I` in cases that the underlying build system does as well (#16077)
* Spack no longer prints any specs that cannot be safely copied into a Spack command (#16462)
* Incomplete Spack environments containing python no longer cause problems (#16473)
* Several improvements to binary package relocation

## Package Improvements

The Spack project is constantly engaged in routine maintenance,
bugfixes, and improvements for the package ecosystem. Of particular
note in this release are the following:

* Spack now contains 4339 packages. There are 430 newly supported packages in v0.15.0
* GCC now builds properly on ARM architectures (#17280)
* Python: patched to support compiling mixed C/C++ python modules through distutils (#16856)
* improvements to pytorch and py-tensorflow packages
* improvements to major MPI implementations: mvapich2, mpich, openmpi, and others

## Spack Project Management:

* Much of the Spack CI infrastructure has moved from Travis to GitHub Actions (#16610, #14220, #16345)
* All merges to the `develop` branch run E4S CI pipeline (#16338)
* New `spack debug report` command makes reporting bugs easier (#15834)

# v0.14.2 (2020-04-15)

This is a minor release on the `0.14` series. It includes performance
improvements and bug fixes:

* Improvements to how `spack install` handles foreground/background (#15723)
* Major performance improvements for reading the package DB (#14693, #15777)
* No longer check for the old `index.yaml` database file (#15298)
* Properly activate environments with '-h' in the name (#15429)
* External packages have correct `.prefix` in environments/views (#15475)
* Improvements to computing env modifications from sourcing files (#15791)
* Bugfix on Cray machines when getting `TERM` env variable (#15630)
* Avoid adding spurious `LMOD` env vars to Intel modules (#15778)
* Don't output [+] for mock installs run during tests (#15609)

# v0.14.1 (2020-03-20)

This is a bugfix release on top of `v0.14.0`.  Specific fixes include:

* several bugfixes for parallel installation (#15339, #15341, #15220, #15197)
* `spack load` now works with packages that have been renamed (#14348)
* bugfix for `suite-sparse` installation (#15326)
* deduplicate identical suffixes added to module names (#14920)
* fix issues with `configure_args` during module refresh (#11084)
* increased test coverage and test fixes (#15237, #15354, #15346)
* remove some unused code (#15431)

# v0.14.0 (2020-02-23)

`v0.14.0` is a major feature release, with 3 highlighted features:

1. **Distributed builds.** Multiple Spack instances will now coordinate
   properly with each other through locks. This works on a single node
   (where you've called `spack` several times) or across multiple nodes
   with a shared filesystem. For example, with SLURM, you could build
   `trilinos` and its dependencies on 2 24-core nodes, with 3 Spack
   instances per node and 8 build jobs per instance, with `srun -N 2 -n 6
   spack install -j 8 trilinos`. This requires a filesystem with locking
   enabled, but not MPI or any other library for parallelism.

2.  **Build pipelines.** You can also build in parallel through Gitlab
   CI. Simply create a Spack environment and push it to Gitlab to build
   on Gitlab runners. Pipeline support is now integrated into a single
   `spack ci` command, so setting it up is easier than ever.  See the
   [Pipelines section](https://spack.readthedocs.io/en/v0.14.0/pipelines.html)
   in the docs.

3. **Container builds.** The new `spack containerize` command allows you
   to create a Docker or Singularity recipe from any Spack environment.
   There are options to customize the build if you need them. See the
   [Container Images section](https://spack.readthedocs.io/en/latest/containers.html)
   in the docs.

In addition, there are several other new commands, many bugfixes and
improvements, and `spack load` no longer requires modules, so you can use
it the same way on your laptop or on your supercomputer.

Spack grew by over 300 packages since our last release in November 2019,
and the project grew to over 500 contributors.  Thanks to all of you for
making yet another great release possible. Detailed notes below.

## Major new core features
* Distributed builds: spack instances coordinate and build in parallel (#13100)
* New `spack ci` command to manage CI pipelines (#12854)
* Generate container recipes from environments: `spack containerize` (#14202)
* `spack load` now works without using modules (#14062, #14628)
* Garbage collect old/unused installations with `spack gc` (#13534)
* Configuration files all set environment modifications the same way (#14372,
  [docs](https://spack.readthedocs.io/en/v0.14.0/configuration.html#environment-modifications))
* `spack commands --format=bash` auto-generates completion (#14393, #14607)
* Packages can specify alternate fetch URLs in case one fails (#13881)

## Improvements
* Improved locking for concurrency with environments (#14676, #14621, #14692)
* `spack test` sends args to `pytest`, supports better listing (#14319)
* Better support for aarch64 and cascadelake microarch (#13825, #13780, #13820)
* Archspec is now a separate library (see https://github.com/archspec/archspec)
* Many improvements to the `spack buildcache` command (#14237, #14346,
  #14466, #14467, #14639, #14642, #14659, #14696, #14698, #14714, #14732,
  #14929, #15003, #15086, #15134)

## Selected Bugfixes
* Compilers now require an exact match on version (#8735, #14730, #14752)
* Bugfix for patches that specified specific versions (#13989)
* `spack find -p` now works in environments (#10019, #13972)
* Dependency queries work correctly in `spack find` (#14757)
* Bugfixes for locking upstream Spack instances chains (#13364)
* Fixes for PowerPC clang optimization flags (#14196)
* Fix for issue with compilers and specific microarchitectures (#13733, #14798)

## New commands and options
* `spack ci` (#12854)
* `spack containerize` (#14202)
* `spack gc` (#13534)
* `spack load` accepts `--only package`, `--only dependencies` (#14062, #14628)
* `spack commands --format=bash` (#14393)
* `spack commands --update-completion` (#14607)
* `spack install --with-cache` has new option: `--no-check-signature` (#11107)
* `spack test` now has `--list`, `--list-long`, and `--list-names` (#14319)
* `spack install --help-cdash` moves CDash help out of the main help (#13704)

## Deprecations
* `spack release-jobs` has been rolled into `spack ci`
* `spack bootstrap` will be removed in a future version, as it is no longer
  needed to set up modules (see `spack load` improvements above)

## Documentation
* New section on building container images with Spack (see
  [docs](https://spack.readthedocs.io/en/latest/containers.html))
* New section on using `spack ci` command to build pipelines (see
  [docs](https://spack.readthedocs.io/en/latest/pipelines.html))
* Document how to add conditional dependencies (#14694)
* Document how to use Spack to replace Homebrew/Conda (#13083, see
  [docs](https://spack.readthedocs.io/en/latest/workflows.html#using-spack-to-replace-homebrew-conda))

## Important package changes
* 3,908 total packages (345 added since 0.13.0)
* Added first cut at a TensorFlow package (#13112)
* We now build R without "recommended" packages, manage them w/Spack (#12015)
* Elpa and OpenBLAS now leverage microarchitecture support (#13655, #14380)
* Fix `octave` compiler wrapper usage (#14726)
* Enforce that packages in `builtin` aren't missing dependencies (#13949)


# v0.13.4 (2020-02-07)

This release contains several bugfixes:

* bugfixes for invoking python in various environments (#14349, #14496, #14569)
* brought tab completion up to date (#14392)
* bugfix for removing extensions from views in order (#12961)
* bugfix for nondeterministic hashing for specs with externals (#14390)

# v0.13.3 (2019-12-23)

This release contains more major performance improvements for Spack
environments, as well as bugfixes for mirrors and a `python` issue with
RHEL8.

* mirror bugfixes: symlinks, duplicate patches, and exception handling (#13789)
* don't try to fetch `BundlePackages` (#13908)
* avoid re-fetching patches already added to a mirror (#13908)
* avoid re-fetching already added patches (#13908)
* avoid re-fetching already added patches (#13908)
* allow repeated invocations of `spack mirror create` on the same dir (#13908)
* bugfix for RHEL8 when `python` is unavailable (#14252)
* improve concretization performance in environments (#14190)
* improve installation performance in environments (#14263)

# v0.13.2 (2019-12-04)

This release contains major performance improvements for Spack environments, as
well as some bugfixes and minor changes.

* allow missing modules if they are blacklisted (#13540)
* speed up environment activation (#13557)
* mirror path works for unknown versions (#13626)
* environments: don't try to modify run-env if a spec is not installed (#13589)
* use semicolons instead of newlines in module/python command (#13904)
* verify.py: os.path.exists exception handling (#13656)
* Document use of the maintainers field (#13479)
* bugfix with config caching (#13755)
* hwloc: added 'master' version pointing at the HEAD of the master branch (#13734)
* config option to allow gpg warning suppression (#13744)
* fix for relative symlinks when relocating binary packages (#13727)
* allow binary relocation of strings in relative binaries (#13724)

# v0.13.1 (2019-11-05)

This is a bugfix release on top of `v0.13.0`.  Specific fixes include:

* `spack find` now displays variants and other spec constraints
* bugfix: uninstall should find concrete specs by DAG hash (#13598)
* environments: make shell modifications partially unconditional (#13523)
* binary distribution: relocate text files properly in relative binaries (#13578)
* bugfix: fetch prefers to fetch local mirrors over remote resources (#13545)
* environments: only write when necessary (#13546)
* bugfix: spack.util.url.join() now handles absolute paths correctly (#13488)
* sbang: use utf-8 for encoding when patching (#13490)
* Specs with quoted flags containing spaces are parsed correctly (#13521)
* targets: print a warning message before downgrading (#13513)
* Travis CI: Test Python 3.8 (#13347)
* Documentation: Database.query methods share docstrings (#13515)
* cuda: fix conflict statements for x86-64 targets (#13472)
* cpu: fix clang flags for generic x86_64 (#13491)
* syaml_int type should use int.__repr__ rather than str.__repr__ (#13487)
* elpa: prefer 2016.05.004 until sse/avx/avx2 issues are resolved (#13530)
* trilinos: temporarily constrain netcdf@:4.7.1 (#13526)

# v0.13.0 (2019-10-25)

`v0.13.0` is our biggest Spack release yet, with *many* new major features.
From facility deployment to improved environments, microarchitecture
support, and auto-generated build farms, this release has features for all of
our users.

Spack grew by over 700 packages in the past year, and the project now has
over 450 contributors.  Thanks to all of you for making this release possible.

## Major new core features
- Chaining: use dependencies from external "upstream" Spack instances
- Environments now behave more like virtualenv/conda
  - Each env has a *view*: a directory with all packages symlinked in
  - Activating an environment sets `PATH`, `LD_LIBRARY_PATH`, `CPATH`,
    `CMAKE_PREFIX_PATH`, `PKG_CONFIG_PATH`, etc. to point to this view.
- Spack detects and builds specifically for your microarchitecture
  - named, understandable targets like `skylake`, `broadwell`, `power9`, `zen2`
  - Spack knows which compilers can build for which architectures
  - Packages can easily query support for features like `avx512` and `sse3`
  - You can pick a target with, e.g. `spack install foo target=icelake`
- Spack stacks: combinatorial environments for facility deployment
  - Environments can now build cartesian products of specs (with `matrix:`)
  - Conditional syntax support to exclude certain builds from the stack
- Projections: ability to build easily navigable symlink trees environments
- Support no-source packages (BundlePackage) to aggregate related packages
- Extensions: users can write custom commands that live outside of Spack repo
- Support ARM and Fujitsu compilers

## CI/build farm support
- `spack release-jobs` can detect `package.py` changes and generate
    `.gitlab-ci.yml` to create binaries for an environment or stack
	in parallel (initial support -- will change in future release).
- Results of build pipelines can be uploaded to a CDash server.
- Spack can now upload/fetch from package mirrors in Amazon S3

## New commands/options
- `spack mirror create --all` downloads *all* package sources/resources/patches
- `spack dev-build` runs phases of the install pipeline on the working directory
- `spack deprecate` permanently symlinks an old, unwanted package to a new one
- `spack verify` chcecks that packages' files match what was originally installed
- `spack find --json` prints `JSON` that is easy to parse with, e.g. `jq`
- `spack find --format FORMAT` allows you to flexibly print package metadata
- `spack spec --json` prints JSON version of `spec.yaml`

## Selected improvements
- Auto-build requested compilers if they do not exist
- Spack automatically adds `RPATHs` needed to make executables find compiler
    runtime libraries (e.g., path to newer `libstdc++` in `icpc` or `g++`)
- setup-env.sh is now compatible with Bash, Dash, and Zsh
- Spack now caps build jobs at min(16, ncores) by default
- `spack compiler find` now also throttles number of spawned processes
- Spack now writes stage directories directly to `$TMPDIR` instead of
    symlinking stages within `$spack/var/spack/cache`.
- Improved and more powerful `spec` format strings
- You can pass a `spec.yaml` file anywhere in the CLI you can type a spec.
- Many improvements to binary caching
- Gradually supporting new features from Environment Modules v4
- `spack edit` respects `VISUAL` environment variable
- Simplified package syntax for specifying build/run environment modifications
- Numerous improvements to support for environments across Spack commands
- Concretization improvements

## Documentation
- Multi-lingual documentation (Started a Japanese translation)
- Tutorial now has its own site at spack-tutorial.readthedocs.io
  - This enables us to keep multiple versions of the tutorial around

## Deprecations
- Spack no longer supports dotkit (LLNL's homegrown, now deprecated module tool)
- `spack build`, `spack configure`, `spack diy` deprecated in favor of
    `spack dev-build` and `spack install`

## Important package changes
- 3,563 total packages (718 added since 0.12.1)
- Spack now defaults to Python 3 (previously preferred 2.7 by default)
- Much improved ARM support thanks to Fugaku (RIKEN) and SNL teams
- Support new special versions: master, trunk, and head (in addition to develop)
- Better finding logic for libraries and headers


# v0.12.1 (2018-11-13)

This is a minor bugfix release, with a minor fix in the tutorial and a `flake8` fix.

Bugfixes
* Add `r` back to regex strings in binary distribution
* Fix gcc install version in the tutorial


# v0.12.0 (2018-11-13)

## Major new features
- Spack environments
- `spack.yaml` and `spack.lock` files for tracking dependencies
- Custom configurations via command line
- Better support for linking Python packages into view directories
- Packages have more control over compiler flags via flag handlers
- Better support for module file generation
- Better support for Intel compilers, Intel MPI, etc.
- Many performance improvements, improved startup time

## License
- As of this release, all of Spack is permissively licensed under Apache-2.0 or MIT, at the user's option.
- Consents from over 300 contributors were obtained to make this relicense possible.
- Previous versions were distributed under the LGPL license, version 2.1.

## New packages
Over 2,900 packages (800 added since last year)

Spack would not be possible without our community.  Thanks to all of our
[contributors](https://github.com/spack/spack/graphs/contributors) for the
new features and packages in this release!


# v0.11.2 (2018-02-07)

This release contains the following fixes:

* Fixes for `gfortran` 7 compiler detection (#7017)
* Fixes for exceptions thrown during module generation (#7173)


# v0.11.1 (2018-01-19)

This release contains bugfixes for compiler flag handling.  There were issues in `v0.11.0` that caused some packages to be built without proper optimization.

Fixes:
* Issue #6999: FFTW installed with Spack 0.11.0 gets built without optimisations

Includes:
* PR #6415: Fixes for flag handling behavior
* PR #6960: Fix type issues with setting flag handlers
* 880e319: Upstream fixes to `list_url` in various R packages


# v0.11.0 (2018-01-17)

Spack v0.11.0 contains many improvements since v0.10.0.
Below is a summary of the major features, broken down by category.

## New packages
- Spack now has 2,178 packages (from 1,114 in v0.10.0)
- Many more Python packages (356) and R packages (471)
- 48 Exascale Proxy Apps (try `spack list -t proxy-app`)


## Core features for users
- Relocatable binary packages (`spack buildcache`, #4854)
- Spack now fully supports Python 3 (#3395)
- Packages can be tagged and searched by tags (#4786)
- Custom module file templates using Jinja (#3183)
- `spack bootstrap` command now sets up a basic module environment (#3057)
- Simplified and better organized help output (#3033)
- Improved, less redundant `spack install` output (#5714, #5950)
- Reworked `spack dependents` and `spack dependencies` commands (#4478)


## Major new features for packagers
- Multi-valued variants (#2386)
- New `conflicts()` directive (#3125)
- New dependency type: `test` dependencies (#5132)
- Packages can require their own patches on dependencies (#5476)
  - `depends_on(..., patches=<patch list>)`
- Build interface for passing linker information through Specs (#1875)
  - Major packages that use blas/lapack now use this interface
- Flag handlers allow packages more control over compiler flags (#6415)
- Package subclasses support many more build systems:
  - autotools, perl, qmake, scons, cmake, makefile, python, R, WAF
  - package-level support for installing Intel HPC products (#4300)
- `spack blame` command shows contributors to packages (#5522)
- `spack create` now guesses many more build systems (#2707)
- Better URL parsing to guess package version URLs (#2972)
- Much improved `PythonPackage` support (#3367)


## Core
- Much faster concretization (#5716, #5783)
- Improved output redirection (redirecting build output works properly #5084)
- Numerous improvements to internal structure and APIs


## Tutorials & Documentation
- Many updates to documentation
- [New tutorial material from SC17](https://spack.readthedocs.io/en/latest/tutorial.html)
  - configuration
  - build systems
  - build interface
  - working with module generation
- Documentation on docker workflows and best practices


## Selected improvements and bug fixes
- No longer build Python eggs -- installations are plain directories (#3587)
- Improved filtering of system paths from build PATHs and RPATHs (#2083, #3910)
- Git submodules are properly handled on fetch (#3956)
- Can now set default number of parallel build jobs in `config.yaml`
- Improvements to `setup-env.csh` (#4044)
- Better default compiler discovery on Mac OS X (#3427)
  - clang will automatically mix with gfortran
- Improved compiler detection on Cray machines (#3075)
- Better support for IBM XL compilers
- Better tab completion
- Resume gracefully after prematurely terminated partial installs (#4331)
- Better mesa support (#5170)


Spack would not be possible without our community.  Thanks to all of our
[contributors](https://github.com/spack/spack/graphs/contributors) for the
new features and packages in this release!


# v0.10.0 (2017-01-17)

This is Spack `v0.10.0`.  With this release, we will start to push Spack
releases more regularly.  This is the last Spack release without
automated package testing.  With the next release, we will begin to run
package tests in addition to unit tests.

Spack has grown rapidly from 422 to
[1,114 packages](https://spack.readthedocs.io/en/v0.10.0/package_list.html),
thanks to the hard work of over 100 contributors.  Below is a condensed
version of all the changes since `v0.9.1`.

### Packages
- Grew from 422 to 1,114 packages
  - Includes major updates like X11, Qt
  - Expanded HPC, R, and Python ecosystems

### Core
- Major speed improvements for spack find and concretization
- Completely reworked architecture support
  - Platforms can have front-end and back-end OS/target combinations
  - Much better support for Cray and BG/Q cross-compiled environments
- Downloads are now cached locally
- Support installations in deeply nested directories: patch long shebangs using `sbang`

### Basic usage
- Easier global configuration via config.yaml
  - customize install, stage, and cache locations
- Hierarchical configuration scopes: default, site, user
  - Platform-specific scopes allow better per-platform defaults
- Ability to set `cflags`, `cxxflags`, `fflags` on the command line
- YAML-configurable support for both Lmod and tcl modules in mainline
- `spack install` supports --dirty option for emergencies

### For developers
- Support multiple dependency types: `build`, `link`, and `run`
- Added `Package` base classes for custom build systems
  - `AutotoolsPackage`, `CMakePackage`, `PythonPackage`, etc.
  - `spack create` now guesses many more build systems
- Development environment integration with `spack setup`
- New interface to pass linking information via `spec` objects
  - Currently used for `BLAS`/`LAPACK`/`SCALAPACK` libraries
  - Polymorphic virtual dependency attributes: `spec['blas'].blas_libs`

### Testing & Documentation
- Unit tests run continuously on Travis CI for Mac and Linux
- Switched from `nose` to `pytest` for unit tests.
  - Unit tests take 1 minute now instead of 8
- Massively expanded documentation
- Docs are now hosted on [spack.readthedocs.io](https://spack.readthedocs.io)
