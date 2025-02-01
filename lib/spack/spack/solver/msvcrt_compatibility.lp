% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% msvcrt compatibility rules for reusing solves.
%
% These rules are used on Windows w/ MSVC
%=============================================================================

% A package cannot be reused if the msvcrt is not compatible with it
error(100, "Cannot reuse {0} since we cannot determine msvcrt compatibility", ReusedPackage)
  :- provider(node(X, MsvcPackage), node(0, "msvcrt")),
     attr("version", node(X, MsvcPackage), MsvcrtVersion),
     attr("hash", node(R, ReusedPackage), Hash),
     % msvcrt packages can be reused without the "compatible_msvcrt" attribute
     ReusedPackage != MsvcPackage,
     not attr("compatible_msvcrt", node(R, ReusedPackage), MsvcPackage, MsvcrtVersion).

% A msvcrt is needed in the DAG
:- has_built_packages(), not provider(_, node(0, "msvcrt")).

% Non-msvcrt reused specs must be host msvcrt compatible. In case we build packages, we get a
% host compatible msvcrt provider from other rules. If nothing is built, there is no msvcrt provider,
% since it's pruned from reusable specs, meaning we have to explicitly impose reused specs are host
% compatible.
:- attr("hash", node(R, ReusedPackage), Hash),
   not provider(node(R, ReusedPackage), node(0, "msvcrt")),
   not attr("compatible_msvcrt", node(R, ReusedPackage), _, _).

% The msvcrt provider must be one that a compiler can target
:- has_built_packages(),
   provider(node(X, MsvcPackage), node(0, "msvcrt")),
   attr("node", node(X, MsvcPackage)),
   attr("version", node(X, MsvcPackage), MsvcrtVersion),
   not host_msvcrt(MsvcPackage, MsvcrtVersion).

% A built node must depend on msvcrt
:- build(PackageNode),
   provider(msvcrtNode, node(0, "msvcrt")),
   not external(PackageNode),
   not depends_on(PackageNode, msvcrtNode).
