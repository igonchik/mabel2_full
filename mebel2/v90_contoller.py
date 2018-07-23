import codecs
import os

import xlwt
from django.conf import settings
from wand.image import Image

from tasks import run_v90_commands


def xlwt_write_line(ws, row, line):
    for i, elem in enumerate(line):
        ws.write(row, i, elem)


class V90Controller:
    def __init__(self, calc_id: int, base_path='/mnt/share/', media_path='/mnt/share/request_export/'):
        self.id = calc_id
        self.base_path = base_path
        self.media_path = media_path

    def create_xls_file(self, rows: list, material):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('1')
        header = ['код детали', 'код материала', 'длина детали', 'ширина детали', 'требуемое количество',
                  'структура', 'продольная кромка спереди', 'продольная кромка сзади', 'поперечная кромка слева',
                  'поперечная кромка справа']
        xlwt_write_line(ws, 0, header)
        for i, row in enumerate(rows):
            nw_row = [i+1, material, row[0], row[1], row[2], row[4], str(row[3][0]) + "X19",
                      str(row[3][2]) + "X19", str(row[3][3]) + "X19", str(row[3][1]) + "X19"]
            xlwt_write_line(ws, i+1, nw_row)
        wb.save(os.path.join(self.base_path, 'import', '%s.xls' % self.id))

    def set_celery_task_run_commands(self):
        task = run_v90_commands.delay(self.id)
        return task.id

    def get_calc_info(self):
        ptn_name = os.path.join(self.base_path, 'data', str(self.id) + '.ptn')
        edg_name = os.path.join(self.base_path, 'data', str(self.id) + '.edg')
        calc_data = dict()

        with codecs.open(ptn_name, 'r', 'cp1251') as ptn:
            lines = ptn.readlines()
            arr = lines[3].split(',')
            calc_data['detail_area'] = arr[1]
            calc_data['plate_area'] = arr[2]
            calc_data['time_raspil'] = arr[3]
            calc_data['detail_count'] = arr[5]
            calc_data['plate_count'] = arr[6]
            calc_data['waste_percentage'] = arr[9]
            calc_data['rez_length'] = arr[13]

        with codecs.open(edg_name, 'r', 'cp1251') as edg:
            lines = edg.readlines()
            for line in lines:
                if line.startswith('EDGEREC1'):
                    arr = lines[1].split(',')
                    type_line = arr[1]
                    if type_line == '2X19':
                        calc_data['kromka_20'] = arr[9]
                    elif type_line == '0.4X19':
                        calc_data['kromka_04'] = arr[9]
                    elif type_line == '0.8X19':
                        calc_data['kromka_08'] = arr[9]
        return calc_data

    def save_pictures(self):
        pdf_name = os.path.join(self.base_path, 'export', str(self.id) + '.pdf')
        save_path = os.path.join(settings.BASE_DIR, self.media_path, str(self.id))
        with Image(filename=pdf_name, resolution=100) as img:
            page_counts = len(img.sequence)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            for i, elem in enumerate(img.sequence):
                elem[0:826, 190:730].save(filename=save_path + "/%s.jpg" % i)
        return page_counts

    @classmethod
    def get_celery_result_by_task_id(cls, task_id):
        return run_v90_commands.AsyncResult(task_id)
