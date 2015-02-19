poplus-pci
==========

Generic python bindings to connect to the `Poplus components <http://poplus.org/components/>`_ APIs.
You can *create*, *read*, *update* and *delete* any items from PopIt through this Binding.

Actually, this is only a convenient wrapper around `Tortilla <https://github.com/redodo/tortilla>`_ generic
API wrapper.


Installation
------------
poplus-pci is available as a module on PyPi, to install, simply run::

    pip install poplus-pci

Alternatively, you can clone this repo and install as you see fit.

How do I ...
------------

First, you'll need to bind to a component.

Let's try Popit at first.

Make sure you have all the information you need. Then get the object use the `PopIt` constructor. ::

    from pci import Popit

    popit = Popit(
        instance='openpolistest',
        host='popit.mysociety.org',
        api_key='-YOUR-API-KEY-',
    )

* ``instance`` Name of the instance you want to point to. There can be more than one for one installation.
* ``host`` The hostname of the PopIt server.
* ``api_key`` This is the API key you can request by clicking
  'Get API key' in the PopIt web interface for your instance, as
  `described in the documentation <http://popit.poplus.org/docs/api/#authentication>`_.

If you're still using an older PopIt instance and have not upgraded
your account for the new, more secure authentication system, instead
of ``api_key`` you can supply ``user`` and ``password``::

    popit = Popit(
        instance='openpolistest',
        host='popit.mysociety.org',
        api_key='-YOUR-API-KEY-',
    )


* ``user`` Your username, the email address that you created the instance with
* ``password`` The password you were emailed when creating the instance


Starting from popit instance, queries can be done using an object oriented interface::

    n_orgs = popit.organizations.get()
    ix_persons = self.p.search.persons.get(
            params={'q': 'birth_date:[1800 TO 1900]'}
    )

And results are accessible through a similar object oriented interface (bunch at work)::

    print("There are {0} organizations at openpolistest instance on popit.mysociety.org.".format(n_orgs.total))
    print(ix_persons.result[0].name)


Requirements
------------

If you don't use pip to install the module, you'll also need:

* tortilla (``pip install tortilla``)


How to run the tests
--------------------

* Copy the file ``config_example.py`` to ``config_test.py``
* Change the entries in ``config_test.py`` to refer to your test servers
* Install `oktest <http://www.kuwata-lab.com/oktest/>`_ (``pip install oktest``)
* Make sure components instances are running, and you have access to them.
  You cannot test this wrapper without running instances.
* run ``python test.py``
