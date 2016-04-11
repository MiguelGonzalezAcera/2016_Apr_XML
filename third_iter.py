"""
Third iteration.
"""
from __future__ import print_function
import optparse, os, shutil, subprocess, sys, tempfile


def warning(*objs):
    print("[ERR]: ", *objs, file=sys.stderr)


def __main__():
    descr = "Develop a panel with options to add to an order"
    parser = optparse.OptionParser(description=descr)
    parser.add_option('--args', help='Arguments given by the user')
    parser.add_option('--out', help='Output')
    parser.add_option('--dir', help='Directory, if needed')

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error('Wrong number of arguments')

    buffsize = 1048576
    tmp_dir = tempfile.mkdtemp()

    arguments = "".join(options.args.split(","))

    print(options.dir)
    print(options.dir.startswith(";"))

    if options.dir.startswith(";") or options.dir.startswith("|"):
        warning('You cant input more orders')
    elif not options.dir.startswith("/"):
        warning('Input not valid')
    else:

        cmd = "ls -%s %s >> %s" % (arguments, options.dir, options.out)

        try:
            try:
                tmp = tempfile.NamedTemporaryFile(dir=tmp_dir).name
                tmp_stderr = open(tmp, 'wb')
                proc = subprocess.Popen(args=cmd, shell=True, cwd=tmp_dir, stderr=tmp_stderr.fileno())
                returncode = proc.wait()
                tmp_stderr.close()
                # get stderr, allowing for case where it's very large
                tmp_stderr = open(tmp, 'rb')
                stderr = ''
                try:
                    while True:
                        stderr += tmp_stderr.read(buffsize)
                        if not stderr or len(stderr) % buffsize != 0:
                            break
                except OverflowError:
                    pass
                tmp_stderr.close()
                if returncode != 0:
                    raise Exception, stderr
            except Exception, e:
                raise Exception, 'Error performing the order. ' + str(e)
        finally:
            # clean up temp dir
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    __main__()
