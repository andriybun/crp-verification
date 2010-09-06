from struct import *
from utils import *
import sys;

class IterableObject(object):
    def __iter__(self):
        for item in self.__dict__:
            yield self.__dict__[item]

class structure(IterableObject):
    field1 = None;
    field2 = None;

person = struct('fname', 'age')

person1 = person('Kevin', 25)
person2 = person(age=42, fname='Terry')

sys.exit();

t = structure()
t.field1 = 9
t.field2 = 'lk'
t.my = 86

for k in t:
    print k



