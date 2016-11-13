def run_seq(cmd):
    """Run `cmd` and yield its output lazily"""
    p = subprocess.Popen(
        cmd, shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    # make STDIN and STDOUT non-blocking
    fcntl.fcntl(p.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
    fcntl.fcntl(p.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

    p.stdin.close()

    while True:
        try:
            chunk = p.stdout.read(32)
            if not chunk:
                break
            yield chunk
        except IOError:
            ex = sys.exc_info()[1]
            if ex[0] != errno.EAGAIN:
                raise
            sys.exc_clear()
        socket.wait_read(p.stdout.fileno())

    p.stdout.close()
