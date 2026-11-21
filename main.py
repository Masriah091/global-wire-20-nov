# main.py - hand-in program for THE GLOBAL WIRE (challenger e2),
# News Image 20261120, account @maseiah990.
# The graded artifact is the pre-rendered entry.png committed beside this
# file (built by draw.py). This program only copies it into the output
# directory named by MAKEFUN_OUTPUT_DIR (default /output), then verifies
# the copy is byte-complete before reporting success.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing beside main.py: %s" % src)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dst) != os.path.abspath(src):
        shutil.copyfile(src, dst)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if dst_size != src_size:
        raise SystemExit(
            "copy incomplete: %s is %d bytes, source is %d"
            % (dst, dst_size, src_size))
    print("wrote", dst, dst_size, "bytes")


if __name__ == "__main__":
    main()
