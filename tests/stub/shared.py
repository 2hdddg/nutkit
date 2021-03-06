"""
Shared utilities for writing stub tests

Uses environment variables for configuration:

TEST_STUB_ADDRESS   Address that stub server should be listenig on (no port)
"""
import subprocess, os, time

# TODO: Fix!!!
stubserver_repo = "/home/peter/code/neo4j-drivers/boltstub"
# Needed to run boltstub server as a module
os.environ['PYTHONPATH'] = stubserver_repo

env_host_address = "TEST_STUB_ADDRESS"

class StubServer:
    def __init__(self, port):
        address = os.environ.get(env_host_address, 'localhost')
        self._port = port
        self._process = None
        self.address = "%s:%d" % (address, port)

    def start(self, script):
        print("Starting stubserver on %s with script %s" % (self.address, script))
        if self._process:
            raise Exception("Stub server in use")

        self._process = subprocess.Popen(
            ["python3", "-m", "boltstub", "-v", "-l", self.address, script],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, encoding='utf-8')
        # TODO: Fix
        time.sleep(1)
        # Double check that the process started, a script that doesn't exist would exit the process
        self._process.poll()
        if self._process.returncode:
            self._dump()
            self._process = None
            raise Exception("Stub server didn't start")

    def _dump(self):
        print("")
        print(">>>> Captured stub server %s stdout" % self.address)
        for line in self._process.stdout:
            print(line)
        print("<<<< Captured stub server %s stdout" % self.address)
        print(">>>> Captured stub server %s stderr" % self.address)
        for line in self._process.stderr:
            print(line)
        print("<<<< Captured stub server %s stderr" % self.address)
        self._close_pipes()

    def _close_pipes(self):
        self._process.stdout.close()
        self._process.stderr.close()

    def _kill(self):
        self._process.kill()
        self._process.wait()
        self._dump()
        self._process = None

    def done(self):
        """ Checks if the server stopped nicely (processes exited with 0), if so this method is done.
        If the server process exited with non 0, an exception will be raised.
        If the server process is running it will be polled until timeout and proceed as above.
        If the server process is still running after polling it will be killed and an exception will be raised.
        """
        polls = 20
        while polls:
            self._process.poll()
            if self._process.returncode is None:
                time.sleep(0.5)
                polls -= 1
            else:
                if self._process.returncode:
                    self._dump()
                    self._process = None
                    raise Exception("Stub server exited unclean")
                self._close_pipes()
                self._process = None
                return

        self._kill()
        raise Exception("Stub server hanged")

    def reset(self):
        if self._process:
            self._kill()

scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")

