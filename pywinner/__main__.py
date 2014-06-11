"""Welcome to pywinner, to build and operate EC2 Windows Python build bots.

Here are the modules inside of pywinner that you can run from your Unix
command line:

python -m pywinner.generate

    Creates a "selfsigned.pem" certificate and private key with which
    the pywinner client running from your Windows prompt can establish a
    secure connection to the small Python server that starts up on your
    Windows EC2 instance.

python -m pywinner.ec2

    Creates the Windows buildbot itself.

python -m pywinner.client

    Lets you run commands on the Windows buildbot once it is up and
    running.

"""
print(__doc__[:-1])
