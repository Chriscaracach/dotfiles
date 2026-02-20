# from libqtile import widget
# from libqtile.widget import base
# import subprocess

# class FanStatus(base.ThreadPoolText):
#     def __init__(self, **config):
#         super().__init__('', **config)
#         self.update_interval = 5

#     def poll(self):
#         try:
#             output = subprocess.check_output(['sensors']).decode()
#             for line in output.splitlines():
#                 if 'cpu_fan' in line.lower() and 'rpm' in line.lower():
#                     stripped_line = line.strip()
#                     parts = stripped_line.split()
#                     if len(parts) >= 2 and parts[-1].upper() == "RPM":
#                         try:
#                             rpm_value = int(parts[-2])
#                             if rpm_value > 0:
#                                 return "ON"
#                             else:
#                                 return "OFF"
#                         except ValueError:
#                             return "OFF"
#                     else:
#                         return "OFF"
#             return 'OFF'
#         except Exception as e:q
#             return f'Error {e}'
