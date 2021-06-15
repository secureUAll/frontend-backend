# Edit superuser attributes
from login.models import User
import os
import json
print("Creating super users...")
# Get env var for super users
env = os.getenv('DJANGO_SUPERUSERS')
print('Env DJANGO_SUPERUSERS:', env)
if not env:
    exit()
# Parse it to an array
emails = json.loads(env)
# For each email, create superuser
for e in emails:
    u = User.objects.create_user(username=e, email=e, is_superuser=True, is_staff=True)
    u.is_admin = True
    u.save()
    print(f"Superuser ({u.username}) created, with admin status! :)")