#!/usr/bin/env python

import os
import nose
import cle

test_location = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             os.path.join('..', '..', 'binaries', 'tests'))

def test_stream():
    dirpath = os.path.join(test_location, "i386")
    filepath = os.path.join(dirpath, "fauxware")
    lib1path = os.path.join(dirpath, "libc.so.6")
    lib2path = os.path.join(dirpath, "ld-linux.so.2")

    path_ld = cle.Loader(filepath)

    lib1 = cle.Loader.load_object(open(lib1path, 'rb'))
    lib2 = cle.Loader.load_object(open(lib2path, 'rb'))
    stream_ld = cle.Loader(open(filepath, 'rb'), auto_load_libs=False, force_load_libs=(lib1, lib2))

    nose.tools.assert_equal(path_ld.main_bin.entry, stream_ld.main_bin.entry)
    nose.tools.assert_equal([x for x in path_ld.shared_objects.keys() if x != 'fauxware'], stream_ld.shared_objects.keys())
    nose.tools.assert_equal(path_ld.memory.read_addr_at(path_ld.main_bin.entry),
                            stream_ld.memory.read_addr_at(stream_ld.main_bin.entry))
    strcmp_string = path_ld.whats_at(path_ld.memory.read_addr_at(0x804a000))
    nose.tools.assert_in('libc.so.6', strcmp_string)
    nose.tools.assert_in('strcmp', strcmp_string)
    nose.tools.assert_equal(strcmp_string, stream_ld.whats_at(stream_ld.memory.read_addr_at(0x804a000)))

if __name__ == '__main__':
    test_stream()
