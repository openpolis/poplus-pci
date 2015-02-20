::

      _____               _
     |  __ \             | |
     | |__) |___   _ __  | | _   _  ___
     |  ___// _ \ | '_ \ | || | | |/ __|
     | |   | (_) || |_) || || |_| |\__ \
     |_|    \___/ | .__/ |_| \__,_||___/
       _____      | |                                            _
      / ____|     |_|                                           | |
     | |      ___   _ __ ___   _ __    ___   _ __    ___  _ __  | |_
     | |     / _ \ | '_ ` _ \ | '_ \  / _ \ | '_ \  / _ \| '_ \ | __|
     | |____| (_) || | | | | || |_) || (_) || | | ||  __/| | | || |_
      \_____|\___/ |_| |_| |_|| .__/  \___/ |_| |_| \___||_| |_| \__|
      _____         _         | |                _    _
     |_   _|       | |        |_|               | |  (_)
       | |   _ __  | |_  ___   __ _  _ __  __ _ | |_  _   ___   _ __
       | |  | '_ \ | __|/ _ \ / _` || '__|/ _` || __|| | / _ \ | '_ \
      _| |_ | | | || |_|  __/| (_| || |  | (_| || |_ | || (_) || | | |
     |_____||_| |_| \__|\___| \__, ||_|   \__,_| \__||_| \___/ |_| |_|
                               __/ |
                              |___/

Generic Python bindings to connect to the `Poplus components <http://poplus.org/components/>`_ APIs.

----
|pypi| |unix_build| |coverage| |downloads| |license|
----


Actually, this is only a convenient wrapper around `Tortilla <https://github.com/redodo/tortilla>`_ generic
API wrapper, with some specialized instructions to use Poplus components apis.

The main advantage of Tortilla over other wrappers is that it allows access through a
full object oriented interface, both when requesting data, and when parsing the results.

Results are transformed from JSON into a Python dictionary, and then bunchified.

Installation
------------
poplus-pci is available as a module on PyPi, to install, simply run::

    pip install poplus-pci

Alternatively, you can clone this repo and install as you see fit.


Quick start
-----------

First, let's try read-only access to the ``legisladores-ar`` instance of Popit at mySociety,
and get the paged list of political organizations in the argentinian parliament:

.. code-block:: python

    from pci import Popit

    popit = Popit(
        instance='legisladores-ar',
        host='popit.mysociety.org',
    )

``instance``
  Name of the instance you want to point to.
  There can be more than one for one installation.

``host``
  The hostname of the PopIt server.

Once an instancehas been created, it's easy enough to access data,
using a full object oriented interface:

.. code-block:: python

    os = popit.organizations.get()

    # there are 65 organizations
    print(os.total)


    # but only 30 have been grabbed
    print(o.page)
    for i, o in enumerate(os.result, start=1):
        print("{0}: {1}".format(i, o.name))

    # how to get next page?
    print os.next_url

    # get it
    os = popit.organizations.get(params={'page': 2})


Write access (Popit)
--------------------

Make sure you have all the information you need. Then get the object use the `PopIt` constructor.

.. code-block:: python

    from pci import Popit

    popit = Popit(
        instance='openpolistest',
        host='popit.mysociety.org',
        api_key='-YOUR-API-KEY-',
    )

``api_key`` 
  This is the API key you can request by clicking
  'Get API key' in the PopIt web interface for your instance, as
  `described in the documentation <http://popit.poplus.org/docs/api/#authentication>`_.

Then the basic CRUD operations will be:

.. code-block:: python


    # create
    einstein = popit.persons.post(data={
        'name': 'Albert Einstein',
        'links': [{
            'url': 'http://www.wikipedia.com/AlbertEinstein',
            'note': 'Wikipedia'
           }]
    })

    # read
    popit.persons(einstein.result.id).get()

    # update (note: is PUT, not PATCH)
    popit.persons(einstein.result.id).put(data={"name": "Albert Einstein"})

    # delete
    popit.persons(einstein.result.id).delete()


If you're still using an older PopIt instance and have not upgraded
your account for the new, more secure authentication system, instead
of ``api_key`` you can supply ``user`` and ``password``:

.. code-block:: python

    popit = Popit(
        instance='openpolistest',
        host='popit.mysociety.org',
        user='-USERNAME-',
        password='-PASSWORD-'
    )


``user``
  Your username, the email address that you created the instance with

``password``
  The password you were emailed when creating the instance



Popit Search api
----------------

Almost all APIs can be wrapped around the pci component, easily.

Starting from a popit instance, queries through the search API can be done:

.. code-block:: python

    popit.search.organizations.get(params={'q': 'trabajo'})
    popit.search.organizations.get(params={'q': 'trabajadores'})


Mapit access
------------

Mapit has read-only access, and the API does not adhere to REST standards.

The default Mapit instance is MySociety's Global Mapit:
http://global.mapit.mysociety.org/.

The mapit API call ``/point/SRID/LON,LAT/[box]``, can be invoked directly,
by tortilla wrapping utilities, or by using Mapit helpers.

.. code-block:: python

    mapit = Mapit()
    self.m.point.get('4326/12.5042,41.8981')
    self.m.areas_overpoint(lat='41.8981', lon='12.5042', srid='4326', box=True)

Other helpers are available, and will be implemented as needed in the futures.
You can find them in the ``pci/__init__.py`` file.



Requirements
------------

If you don't use pip to install the module, you'll also need:

* tortilla (``pip install tortilla``)


How to run the tests
--------------------

* Copy the file ``config_sample.py`` to ``config_test.py``
* Change the entries in ``config_test.py`` to refer to your test servers
* Install `oktest <http://www.kuwata-lab.com/oktest/>`_ (``pip install oktest``)
* Make sure components instances are running, and you have access to them.
  You cannot test this wrapper without running instances.
* run ``python test.py``to run all tests,
  ``python test_mapit.py``, or ``python test_popit.py`` to run the specified
  component's tests


Changelog
---------

=== 0.1 (2015-02-20) ===

initial release


Credits
-------

- `tortilla`_
- `popit-python`_
- `slumber`_

.. _tortilla: https://github.com/redodo/tortilla
.. _popit-python: https://github.com/mysociety/popit-python
.. _slumber: https://github.com/samgiles/slumber


.. |pypi| image:: https://img.shields.io/pypi/v/poplus-pci.svg?style=flat-square&label=version
    :target: https://pypi.python.org/pypi/poplus-pci
    :alt: Latest version released on PyPi

.. |coverage| image:: https://img.shields.io/coveralls/openpolis/poplus-pci/master.svg?style=flat-square
    :target: https://coveralls.io/r/openpolis/poplus-pci?branch=master
    :alt: Test coverage

.. |unix_build| image:: https://img.shields.io/travis/openpolis/poplus-pci/master.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/openpolis/poplus-pci
    :alt: Build status of the master branch on Mac/Linux

.. |downloads| image:: https://img.shields.io/pypi/dm/poplus-pci.svg?style=flat-square
    :target: https://pypi.python.org/pypi/poplus-pci
    :alt: Monthly downloads

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/openpolis/poplus-pci/master/LICENSE.txt
    :alt: Package license
