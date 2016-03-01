#!/usr/bin/env python2
import os
import stat

def genLine(base, path, pointer=None):
    fullname = path
    if pointer:
        fullname = os.path.join(path,pointer)
    try:
        # Google's tools are really fragile about filenames, so filter anything with ISO8859-1 chars.
        for char in fullname:
            if ord(char) > 127:
                return
        stats = os.stat(fullname)
        bl = len(base)+1
        subname = fullname[bl:]
        mode = stat.S_IMODE(stats.st_mode)
        realmode = (((7<<6&mode)>>6)*100) + (((7<<3&mode)>>3)*10) + (7&mode)
        print("%s;%s;%s;%s;%s" % (subname, stats.st_uid, stats.st_gid, realmode, "selabel=u:object_r:system_file:s0;capabilities=0x0"))
    except OSError:
        pass # Ignore symlinks that can't be stat-ed.

def genMetaFile(base, directory):
    genLine(base, os.path.join(base, directory))
    for root, dirs, files in os.walk(os.path.join(base, directory)):
        for directory in dirs:
            genLine(base, root, directory)
        for filename in files:
            genLine(base, root, filename)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        genMetaFile(sys.argv[1], sys.argv[2])
        exit(0)
    else:
        exit(1)
