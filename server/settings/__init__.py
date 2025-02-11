
import os
from .base import *

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *

elif ENVIRONMENT == "testing":
    from .testing import *

else:
    from .development import *