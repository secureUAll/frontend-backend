# Edit superuser attributes
from login.models import User
import os
u=User.objects.get(username=os.environ.get('DJANGO_SUPERUSER_USERNAME', ''))
u.is_admin=True
u.save()
print(f"Superuser ({u.username}) with admin status created! :)")