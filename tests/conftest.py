import os
import sys

import django

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

