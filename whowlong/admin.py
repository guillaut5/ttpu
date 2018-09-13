# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from .models import Place,PlaceAdmin
from .models import Request,RequestAdmin
from .models import Trajet,TrajetAdmin
from .models import TrajetData, TrajetDataAdmin
from .models import Event,EventAdmin
from .models import Param,ParamAdmin


admin.site.register(Place,PlaceAdmin)
admin.site.register(Request,RequestAdmin)
admin.site.register(Trajet,TrajetAdmin)
admin.site.register (TrajetData,TrajetDataAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Param, ParamAdmin)

