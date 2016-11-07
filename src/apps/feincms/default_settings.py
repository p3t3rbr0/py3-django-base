from __future__ import absolute_import, unicode_literals

from django.conf import settings


#: Include ancestors in filtered tree editor lists
FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = getattr(settings, 'FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS', False)

#: Enable checking of object level permissions. Note that if this option is
#: enabled, you must plug in an authentication backend that actually does
#: implement object level permissions or no page will be editable.
FEINCMS_TREE_EDITOR_OBJECT_PERMISSIONS = getattr(settings, 'FEINCMS_TREE_EDITOR_OBJECT_PERMISSIONS', False)
