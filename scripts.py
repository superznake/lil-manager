import subprocess


def smth():
    proc = subprocess.Popen('./test.sh', stdout=subprocess.PIPE)
    output = proc.stdout.read()
    return output


def start():
    ...


def stop(delay: int = 60):
    ...


def restart(delay: int = 60):
    ...


def say(text: str = "Hello!"):
    ...
