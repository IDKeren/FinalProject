from django.apps import AppConfig
import subprocess
import sys

class ApiConfig(AppConfig):  # The class name should match the convention, usually <AppName>Config
    name = 'api'  # The name should match the app's directory

    # def ready(self):
    #     # Custom startup code: running external Python scripts
    #     subprocess.Popen([sys.executable, '/Final-Project/backend/FinalProject/manager.py'])
        # subprocess.Popen([sys.executable, '/Final-Project/backend/FinalProject/main.py'])
