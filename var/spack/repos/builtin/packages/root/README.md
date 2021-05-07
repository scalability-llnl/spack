# ROOT Recipe Notes

ROOT has a significant number of build options. Not all of them are supported by this package recipe at this time. Relevant notes on support (or lack thereof) for various options is below.

## Fixed and unsupported options

### Missing dependencies

The following configuration options are unsupported (set to `OFF`) due to missing dependencies:

#### `alien`

Requires `libgapiUI` from ALICE.

#### `gfal`

#### `http`

ROOT looks for and uses the FastCGI package on the system if found, creating a possible non-portable dependency. There is currently no `fastcgi` recipe, nor any way to unconditionally disable the search for the package.

#### `monalisa`

Monitoring with Monalisa depends on `libapmoncpp`.

#### `odbc`

#### `tcmalloc`

#### `xinetd`

### Discontinued options

Support for several options was discontinued in ROOT without prior support in the recipe:

#### `afdsmgrd`

#### `afs`

#### `bonjour`

#### `castor`

#### `chirp`

#### `geocad`

#### `glite`

#### `globus`

#### `hdfs`

#### `ios`

#### `krb5`

#### `ldap`

#### `rfio`

#### `ruby`

#### `sapdb`

#### `srp`

### Other fixed or unsupported options

### `arrow=OFF`

#### `asimage=ON`, `astiff=ON`, `builtin_afterimage=ON`

Full control of `asimage` and `astiff` would require a package recipe for libAfterImage or Afterstep. In their absence, we use the provided and internally built version of libAfterImage.

#### `ccache=OFF`

Only useful for repeated builds.

#### `cling=OFF`

The use of Cling is assumed.

#### `cxxmodules`

This option should not be confused with `runtime_cxxmodules`. `cxxmodules` is an optimization that affects only the efficiency of building ROOT.

#### `exceptions=ON`

Support for C++ exceptions is assumed.

#### `explicitlink=ON`

Use of explicit linking when making shared libraries is assumed.

#### `fail-on-missing=ON`

Failure on missing dependencies is assumed (_vs_ automatically setting `builtin_XXX`).

#### `gnuinstall=OFF`

GNU-compliant install layout.

#### `libcxx`

This option controls use of the libC++ standard C++ library via compiler options. It is set automatically by ROOT's configuration on macOS >=10.7 when a Clang compiler is configured. Due to complexities related to compiler options and the way a compiler might have been configured, configurable support is disabled until (at least) Spack supports the standard library as a virtual dependency.

#### `pch=ON`

The use of pre-compiled headers when building is assumed.

#### `roottest=OFF`

`roottest` requires access to the network.

#### `runtime_cxxmodules=OFF`

This option tells ROOT to generate and use PCMs for its own libraries. This functionality is experimental for ROOT < 6.20, and is currently not supported by the recipe.

#### `shared=ON`

The use of shared libraries is assumed.

#### `soversion=ON`

The use of versioning for shared libraries is assumed.

#### `testing`

The building of ROOT's test suite and its availability for use by CTest is pegged to Spack's determination of whether testing is required for the current installation procedure.

## Variants and version dependent support for options

Some configuration options are version dependent---unavailable before or after a specific version. The current accounting for such options in the recipe is far from exhaustive, and a survey of the various options and the versions that support them would be useful. However, accounting for them is somewhat clumsy absent a `when` clause for variants, or similar.

### Conflicting variants since 6.18

#### `memstat`

#### `qt4`

Representing the obsolete `qt` and `qtgsi` ROOT build options.

#### `table`

### Temporarily conflicting variants

The `http` variant is currently an unconditional conflict due to the non-portable dependency mentioned above.

## Permanently removed variants

The following variants have been removed from the recipe as they have always been ineffective:

* `avahi`
* `kerberos`
* `ldap`
* `libcxx`
* `odbc`
* `tiff`

In addition, the `test` variant has been removed as its actions are irrelevant to the installed source---the corresponding `testing` ROOT option is enabled if and only if `self.run_tests` is set.
