[![Build Status](https://travis-ci.org/fhats/webwol.svg?branch=master)](https://travis-ci.org/fhats/webwol)

# webwol: Generate wake-on-lan packets via a web interface

This script provides one-touch wake-on-lan packet generation from a web interface.
There's not much to it. The only thing it depends on is Python (2.6+).

# How To Use

This script has intentionally attempted to minimize dependencies. It should run
anywhere that has python 2.6, 2.7, 3.2, 3.3, 3.4, or 3.5 installed.

## Install It

Get the code somehow:

* [Download the latest release](https://github.com/fhats/webwol/releases/latest)
* Clone this repository
* [Download a debian package](https://github.com/fhats/webwol/releases/latest)
    * Install it with something like `dpkg -i python-webwol*.deb`
* Copy and paste it from this repo
* pip install it
* Transcribe it by hand??

## Configure It

Here's the magic bit. Write down the MAC addresses you want to send wake-on-lan
packets to. Give those puppies a name, too, cause why not? Do it like this:

```
{
    "deadbeef-dad": "de:ad:be:ef:da:dd",
    "mr-counter": "12:34:56:78:90:ef"
}
```

If you don't know the MAC address you want, try lookin' up how to do it on the
[internet](http://www.wikihow.com/Find-the-MAC-Address-of-Your-Computer).

Save all them juicy bits in a file somewhere on the computer that webwol's gonna
run on. You could put it in a place like /etc/webwol.json if you want. Or your
homedir. I won't judge.

## Run It

`python webwol.py` from the place where you downloaded the code. Or if you
installed from a debian package, it's probably in your path, so try just `webwol.py`?

