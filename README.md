
pywinner — get Windows ready to compile Python extensions
=========================================================

The PyWinner project is a ragtag collection of scripts that sets up a
Windows EC2 instance to build Python extensions.  These are the main
subcommands:

 *  `python -m pywinner.generate`
    creates an SSL private key and self-signed certificate that your
    local machine will use to give orders to the Windows machine.

 *  `python -m pywinner.ec2`
    uses [Boto](http://boto.readthedocs.org/en/latest/) to create a
    Windows EC2 instance that, on first boot, downloads and installs
    every version of Python back to version 2.5 and then also downloads
    (but does not install, because I am not sure how to automate Windows
    installer click-throughs) all of the Microsoft compilers that are
    necessary to build Python extensions under Python 2.5 through 3.4:

    * **Microsoft Visual Studio Express 2008** which builts 32-bit
      Python extensions for Python 3.2 and earlier.

    * **Microsoft Windows SDK for Windows 7 and .NET Framework 3.5 SP1**
      which builds 64-bit Python extensions for Python 3.2 and earlier.

    * **Microsoft Windows SDK for Windows 7 and .NET Framework 4** which
      builds both 32-bit and 64-bit Python extensions for Python 3.3 and
      later.

    These three installers are left sitting on the Administrator desktop
    so you can log in with Remote Desktop, double-click them, and get
    the compilers all installed.  I would love advice or pull requests
    on getting these steps automated away.

    Finally, PyWinner also starts the tiny Python web service that will
    let us give the Windows machine automated instructions from your
    local machine.  (It does all of these steps through a PowerShell
    “user data” script that Amazon EC2 instances run at startup.)

 *  `python -m pywinner.client`
    is there mainly to let you experiment with the tiny RPC service that
    PyWinner runs.  If you give it a command like `print(3+3)` then you
    should see `6` come back, computed in the Python 3.4 runtime that is
    ready to do your bidding on the Windows EC2 box.

 *  `python -m pywinner.build`
    builds my PyEphem package for all Python versions 2.5 through 3.4 by
    calling the little RPC service and telling it to run hand-crafted
    `.BAT` scripts that, for each Python version, get the compilers
    configured exactly the right way to do the compile.  It is the
    script that probably needs the most work before it can serve as a
    general tool for other projects.

The result, for PyEphem, is a whole slew of Windows installers that are
now ready for people to use:

https://pypi.python.org/pypi/ephem/

The RPC service currently just runs `eval()` on the text it is given.
Now that I have had some experience with it, what it mostly needs to let
me do is create and run `.BAT` files, so I might simplify it later as a
real Python XML-RPC endpoint (since that is the only form of RPC
supported in the Standard Library, right?) that offers only one or two
functions, instead of being a general `eval()` as it is today.

Again, please feel welcome to open issues and pull requests to help me
see how this single-purpose get-PyEphem-compiled tool can be expanded
out to help you with your own projects.
