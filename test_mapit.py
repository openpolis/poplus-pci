from pci import Mapit
from oktest import test, ok, NG, DIFF

__author__ = 'guglielmo'


# load configuration
import config_test
keys = [
    x for x in dir(config_test)
    if x.startswith("mapit__") and not x.startswith("__")
]
vals = map(lambda x: eval('config_test.'+x), keys)
keys = map(lambda x: x[7:], keys)
conf = dict(zip(keys, vals))

class GetterSetterTest(object):

    ## invoked only once before all tests
    @classmethod
    def before_all(cls):
        cls.m = Mapit(**conf)

    ## invoked before each test
    def before(self):
        self.m = self.__class__.m

    @test("constructor should set right members")
    def _(self):
        for i, k in enumerate(keys):
            v = vals[i]
            ok(getattr(self.m, k)) == v


class StatusTest(object):
    @classmethod
    def before_all(cls):
        cls.m = Mapit(**conf)

    def before(self):
        self.m = self.__class__.m

    @test("is_online should return true")
    def _(self):
        ok(self.m.is_online()) == True

    @test("get_url should return a string")
    def _(self):
        ok(self.m.get_url()).is_a(str)



class ReadTest(object):
    @classmethod
    def before_all(cls):
        cls.m = Mapit(**conf)

    def before(self):
        self.m = self.__class__.m

    @test("extracts all areas over a given point")
    def _(self):
        lat = '41.8981'
        lon = '12.5042'

        result = len(
            self.m.areas_overpoint(lat, lon, srid='4326')
        )
        ok(result) == 3


    @test("extracts all areas of a given type")
    def _(self):
        type = 'REG'
        result = len(
            self.m.areas_oftype(type)
        )
        ok(result) == 20


    @test("extracts all areas having a name starting with ...")
    def _(self):
        name = 'Rom'
        result = len(
            self.m.areas_namestartswith(name)
        )
        ok(result) == 16


"""
from pci import Mapit

mapit = Mapit()

point = '12.5042,41.8981'
srid = '4326'

area_ids = [
    i for i in mapit.point.get('{0}/{1}'.format(srid, point)).keys()
    if i != 'debug_db_queries'
]
print("There are {0} areas over {1}.".format(len(area_ids), point))

for area_id in area_ids:
    area = mapit.area.get(area_id)
    print "{0}area/{1}".format(mapit.get_url(), area_id)
    print "==="
    for k, v in area.items():
        if k == 'debug_db_queries':
            continue
        print "  {0}: {1}".format(k, v)
"""

## invoke tests
if __name__ == '__main__':
    import oktest
    oktest.main()
