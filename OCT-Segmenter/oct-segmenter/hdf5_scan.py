#!/usr/bin/python

import sys
import os
import getopt
import numpy as np
import h5py

# Scan any hdf5 file
def scan_hdf52(path, recursive=True, tab_step=2):
    def scan_node(g, tabs=0):
        elems = []
        for k, v in g.items():
            if isinstance(v, h5py.Dataset):
                elems.append(v.name)
            elif isinstance(v, h5py.Group) and recursive:
                elems.append((v.name, scan_node(v, tabs=tabs + tab_step)))
        return elems

    with h5py.File(path, "r") as f:
        return scan_node(f)


def main(argv):
    infile = ""
    outfile = ""
    outpath = ""
    cmdhelpstr = "hdf5scan.py -i <inputfile> -o <outputpath>"
    # Example: Run with 'python hdf5scan.py -i model_epoch858.hdf5 -o .'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "opath="])

        for opt, arg in opts:
            if opt == "-h":
                print(cmdhelpstr)
                sys.exit()
            elif opt in ("-i", "--ifile"):
                infile = arg
            elif opt in ("-o", "--ofile"):
                outpath = arg
    except getopt.GetoptError:
        print(cmdhelpstr)
        sys.exit(2)
    if infile == "" or outpath == "":
        print(cmdhelpstr)
        sys.exit(2)

    # write hdf5 contents to file
    elems = scan_hdf52(infile, True, 2)

    outfile = os.path.join(outpath, "out.txt")
    ffile = open(outfile, "w+")

    for e in elems:
        content = str(e) + str("\n")
        ffile.write(content)

    ffile.close()

    # print summary to stdout
    f = h5py.File(infile, "r")
    keys = list(f.keys())

    for k in keys:
        filename = os.path.join(outpath, str(k) + ".txt")
        n1 = f.get(k)
        n1 = np.array(n1)
        np.savetxt(filename, n1, fmt="%s")
        print("Keys: " + str(k) + ", Dims: " + str(n1.shape))


if __name__ == "__main__":
    main(sys.argv[1:])