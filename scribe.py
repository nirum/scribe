import time
VERSION = '0.0.1'
IGNORE = {
    'exact': ('ls', 'pwd', 'whos'),
    'start': ('plt', 'cd', 'print', 'mkdir', '!', '%', 'close'),
    'end': ('shape', '?'),
}


def isvalid(code):
    """Determines if the code fragment should be logged or not

    Parameters
    ----------
    code : str
        A code snippet

    Returns
    -------
    valid : bool
        Whether or not this code snippet should be logged to the log file
    """
    if code in IGNORE['exact']:
        return False

    if any(code.startswith(s) for s in IGNORE['start']):
        return False

    if any(code.endswith(s) for s in IGNORE['end']):
        return False

    return True


class Stenographer:
    def __init__(self, ip):
        self.shell = ip
        self.history = ip.history_manager

        # make the logfile
        self.filename = f"scribble_{time.strftime('%d.%A')}.py"

        with open(self.filename, 'x') as f:
            f.write(f"# Scribble {time.strftime('%B %d, %Y')}")

        # entry message
        print(f'Logging history to {self.filename}')

    def start(self):
        pass

    def stop(self):
        """Logs the previous IPython command to a file"""
        # get the previous session, line, and code
        session, line, code = next(self.history.get_range(start=-1))

        if isvalid(code):
            with open(self.filename, 'a') as f:
                f.write(f"\n{code}")


def load_ipython_extension(ip):
    """On load"""
    log = Stenographer(ip)
    # ip.events.register('pre_run_cell', log.start)
    ip.events.register('post_run_cell', log.stop)
