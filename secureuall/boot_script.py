# Edit superuser attributes
from login.models import User
import os
import json
env = os.getenv('DJANGO_SUPERUSERS')
if not env:
        exit()
emails = json.loads(env)
for e in emails:
    u = User.objects.get(username=e)
    u.is_admin = True
    u.save()
    print(f"Superuser ({u.username}) granted admin status! :)")