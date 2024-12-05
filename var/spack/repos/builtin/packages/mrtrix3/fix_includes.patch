--- ./configure.orig    2023-11-12 14:48:25.802025918 -0800
+++ ./configure 2023-11-12 14:48:56.177057419 -0800
@@ -571,10 +571,7 @@
     try:
       flags = []
       for flag in shlex.split (execute ([ 'pkg-config' ] + pkg_config_flags.split(), RunError)[1]):
-        if flag.startswith ('-I'):
-          flags += [ '-idirafter', flag[2:] ]
-        else:
-          flags += [ flag ]
+        flags += [ flag ]
       return flags
     except Exception:
       log('error running "pkg-config ' + pkg_config_flags + '"\n\n')
@@ -1323,10 +1320,7 @@
       for entry in qt:
         if entry[0] != '$' and not entry == '-I.':
           entry = entry.replace('\"','').replace("'",'')
-          if entry.startswith('-I'):
-            qt_cflags += [ '-idirafter', entry[2:] ]
-          else:
-            qt_cflags += [ entry ]
+          qt_cflags += [ entry ]

       qt = qt_ldflags + qt_libs
       qt_ldflags = []
