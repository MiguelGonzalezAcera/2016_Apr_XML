"""
First iteration.

usage: first_iter.py [options]

See below for options
"""

import optparse, os, shutil, subprocess, tempfile


def __main__():
    descr = "Develop a panel allowing the user to add an order"
    parser = optparse.OptionParser(description=descr)
    parser.add_option('--query', help='Order form the user')
    parser.add_option('--out', help='Order form the user')

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error('Wrong number of arguments')

    buffsize = 1048576
    tmp_dir = tempfile.mkdtemp()

    cmd = "%s >> %s" % (options.query, options.out)

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
