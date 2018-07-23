from celery import Celery
import subprocess
import os

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@celery_app.task
def debug_task():
    print('Request: {0!r}'.format(11))


@celery_app.task
def run_v90_commands(calc_id: int):
    command_list = [['wine', '/home/vnc/.wine/drive_c/V90/Import.exe',
                     'C:\\V90\\TP\\import\\{0}.xls'.format(calc_id),
                     '/FORMAT:20', '/overwrite', '/NOWRTBRD'],
                    ['wine', '/home/vnc/.wine/drive_c/V90/Batch.exe',
                     '{0}.btc'.format(calc_id), '/AUTO', '/OPTIMISE'],
                    ['wine', '/home/vnc/.wine/drive_c/V90/Output.exe', '/RUN={0}'.format(calc_id), '/PDF',
                     '/REPORTS:J'],
                    ['wine', '/home/vnc/.wine/drive_c/V90/SawLink.exe', '/AUTO', '/run={0}'.format(calc_id),
                             '/SAWPATH=C:\\v90\\tp\\robland', '/TRANSMODE=12']]

    for elem in command_list:
        res = subprocess.run(elem, cwd='/home/vnc/.wine/drive_c/V90/TP')
        if res.returncode != 0:
            print('ERROR command V90: ', elem)
            return -1

    return 0
