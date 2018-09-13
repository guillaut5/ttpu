# -*- coding: utf-8 -*-
'''
Created on 1 août 2017

@author: guillaume
'''


class Place(object):
    """Famous place"""

    name =u"inconnu"
    street= u"3 rue des rosiers"
    city = u"MONTPELLIER"
    pays = u"FRANCE"
    postaladress = u"500 Avenue Georges Frêche, 34170 Castelnau-le-Lez"
    lat = 0.0
    lon = 0.0
    
    
    
    def __str__(self):
        return "%s %s %s" % (self.name, self.street, self.city)
        