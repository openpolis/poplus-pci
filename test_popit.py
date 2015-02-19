from time import sleep
from pci import Popit
from requests import HTTPError
from oktest import test, ok, NG, DIFF

__author__ = 'guglielmo'


# load configuration
import config_test
keys = [x for x in dir(config_test) if x.startswith("popit__") and not x.startswith("__")]
vals = map(lambda x: eval('config_test.'+x), keys)
keys = map(lambda x: x[7:], keys)
conf = dict(zip(keys, vals))

class GetterSetterTest(object):

    ## invoked only once before all tests
    @classmethod
    def before_all(cls):
        cls.p = Popit(**conf)

    ## invoked before each test
    def before(self):
        self.p = self.__class__.p

    @test("constructor should set right members")
    def _(self):
        for i, k in enumerate(keys):
            v = vals[i]
            ok(getattr(self.p, k)) == v


class StatusTest(object):
    @classmethod
    def before_all(cls):
        cls.p = Popit(**conf)

    def before(self):
        self.p = self.__class__.p

    @test("is_online should return true")
    def _(self):
        ok(self.p.is_online()) == True

    @test("get_url should return a string")
    def _(self):
        ok(self.p.get_url()).is_a(str)


class AuthenticationTest(object):
    @classmethod
    def before_all(cls):
        wrong_conf = conf.copy()
        wrong_conf['auth_key'] = '3h45hk345h'
        cls.p = Popit(**wrong_conf)

    def before(self):
        self.p = self.__class__.p

    @test("wrong credentials should not fail when only reading")
    def _(self):
        def f():
            self.p.persons.get()
        NG (f).raises(Exception)

    @test("wrong credentials should raise exception when saving")
    def _(self):

        def f():
            self.p.persons.post({'name': 'Albert Keinstein'})
        ok (f).raises(Exception)


class CreateTest(object):
    @classmethod
    def before_all(cls):
        cls.p = Popit(**conf)

    def before(self):
        self.p = self.__class__.p

    @test("can create person")
    def _(self):
        self.type = self.p.persons
        self.new = self.p.persons.post(
            data={'name': 'Albert Keinstein'}
        )

    @test("can create organization")
    def _(self):
        self.type = self.p.organizations
        self.new = self.p.organizations.post(
            data={'name': 'Space Party'}
        )

    def after(self):
        """Remove test objects from popit instance"""
        self.type(self.new.result.id).delete()

class ReadUpdateDeleteTest(object):
    @classmethod
    def before_all(cls):
        cls.p = Popit(**conf)

    def before(self):
        self.p = self.__class__.p
        new = self.p.persons.post(data={
            'name': 'Albert Keinstein',
            'links': [{
                'url': 'http://www.wikipedia.com/AlbertEinstein',
                'note': 'Wikipedia'
               }]
        })
        self.id = new.result.id

    def after(self):
        self.p.persons(self.id).delete()

    @test("can read person's name")
    def _(self):
        result = self.p.persons(self.id).get()
        data = result['result']
        ok(data.name) == "Albert Keinstein"

    @test("can read person's links")
    def _(self):
        result = self.p.persons(self.id).get()
        data = result['result']
        ok(data.links[0].url) == "http://www.wikipedia.com/AlbertEinstein"
        ok(data.links[0].note) == "Wikipedia"

    @test("can edit person's name")
    def _(self):
        self.p.persons(self.id).put(data={"name": "Albert Einstein"})
        result = self.p.persons(self.id).get()
        ok(result.result.name) == "Albert Einstein"

    @test("can delete person")
    def _(self):
        result = self.p.persons(self.id).delete()
        ok(result) == None
        def f():
            result = self.p.persons(self.id).get()
        ok (f).raises(HTTPError)

    @test("deleting a person more than once doesn't raise an error")
    def _(self):
        result = self.p.persons(self.id).delete()
        ok(result) == None
        result = self.p.persons(self.id).delete()
        ok(result) == None

    @test("deleting a non existing person doesn't raise an error")
    def _(self):
        result = self.p.persons('xxxx').delete()
        ok(result) == None

class SearchTest(object):
    @classmethod
    def before_all(cls):
        cls.p = Popit(**conf)

    def before(self):
        self.p = self.__class__.p
        self.einstein = self.p.persons.post(data={
            'name': 'Albert Einstein',
            'birth_date': '1879-03-14',
            'death_date': '1955-04-18',
            "national_identity": "Stateless",
            'links': [{
                'url': 'http://www.wikipedia.com/Albert_Einstein',
                'note': 'Wikipedia'
               }]
        })
        self.dirac = self.p.persons.post(data={
            'name': 'Paul Dirac',
            'birth_date': '1902-08-08',
            'death_date': '1984-10-20',
            "national_identity": "United Kingdom",
            'links': [{
                'url': 'http://www.wikipedia.com/Paul_Dirac',
                'note': 'Wikipedia'
               }]
        })
        self.bohr = self.p.persons.post(data={
            'name': 'Niels Bohr',
            'birth_date': '1885-10-07',
            'death_date': '1962-11-18',
            "national_identity": "Danish",
            'links': [{
                'url': 'http://www.wikipedia.com/Niels_Bohr',
                'note': 'Wikipedia'
               }]
        })

        # need this, or search results may vary
        # likely due to elastic search indexing
        sleep(1)

    def after(self):
        self.p.persons(self.einstein.result.id).delete()
        self.p.persons(self.dirac.result.id).delete()
        self.p.persons(self.bohr.result.id).delete()

    @test("searching by name")
    def _(self):
        result = self.p.search.persons.get(
            params={'q': 'name:Niels'}
        )
        ok(result.total) == 1

    @test("searching by date range")
    def _(self):
        result = self.p.search.persons.get(
            params={'q': 'birth_date:[* TO 1900]'}
        )
        ok(result.total) == 2

    @test("searching by date range AND name")
    def _(self):
        result = self.p.search.persons.get(
            params={'q': 'birth_date:[* TO 1900] AND name:Niels'}
        )
        ok(result.total) == 1

"""
# some code to test within a python shell

# load configuration
import config_test
keys = [x for x in dir(config_test) if x.startswith("popit__") and not x.startswith("__")]
vals = map(lambda x: eval('config_test.'+x), keys)
keys = map(lambda x: x[7:], keys)
conf = dict(zip(keys, vals))

# setup popit instance
p = Popit(**conf)

# setup samples
einstein = p.persons.post(data={
    'name': 'Albert Einstein',
    'birth_date': '1879-03-14',
    'death_date': '1955-04-18',
    "national_identity": "Stateless",
    'links': [{
        'url': 'http://www.wikipedia.com/Albert_Einstein',
        'note': 'Wikipedia'
       }]
})
dirac = p.persons.post(data={
    'name': 'Paul Dirac',
    'birth_date': '1902-08-08',
    'death_date': '1984-10-20',
    "national_identity": "United Kingdom",
    'links': [{
        'url': 'http://www.wikipedia.com/Paul_Dirac',
        'note': 'Wikipedia'
       }]
})
bohr = p.persons.post(data={
    'name': 'Niels Bohr',
    'birth_date': '1885-10-07',
    'death_date': '1962-11-18',
    "national_identity": "Danish",
    'links': [{
        'url': 'http://www.wikipedia.com/Niels_Bohr',
        'note': 'Wikipedia'
       }]
})

# do search stuff
# this one in particular gshould return two
p.search.persons.get(
    params={'q': 'birth_date:[* TO 1900]'}
)

# tear down samples
p.persons(einstein.result.id).delete()
p.persons(dirac.result.id).delete()
p.persons(bohr.result.id).delete()

"""