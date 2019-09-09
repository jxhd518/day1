# -*- coding: utf-8 -*-
def export_patients():
    gte__created = '2016-2-10'
    lte__created = '2019-8-12'
    db_handle = CommonDao()

    data_positions = ['TN041', 'TN044', 'TN047', 'TN071', 'TN074', 'GX036', 'GX039', 'GX042',
                      'GX053', 'GX056', 'TJ126', 'TJ131', 'TJ136', 'TJ141', 'TJ146', 'TJ312',
                      'TJ318', 'TJ324', 'TJ330', 'TJ336', 'TN050', 'TN077', 'TN080', 'TN083',
                      'TN086']

    patients = db_handle.fetch_list(Patient, length='ALL',
                                    is_del=0, enabled=1,
                                    gte__created=gte__created,
                                    lte__created=lte__created,
                                    )
    patient_ids = list(set([patient.patient_id for patient in patients]))
    target_list = []
    for patient in patients:
        patient = patient.to_dict()
        medics_data = db_handle.fetch_list(PatientFollowUpFormData,
                                           in__data_position=data_positions,
                                           length='ALL',
                                           patient_id=patient['patient_id'],
                                           # patient_id='0babf2f835ef4f7c9f19a589c031c8e1',
                                           # gte__updated=gte__created,
                                           # lte__updated=lte__created,
                                           data_status=2)

        medicines_list = [medic_data.data_value for medic_data in medics_data]  # 个人所有用药
        med_list = []
        for name in medicines_list:
            obj = re.search('^.*[二甲]', name)
            if obj is not None:
                med_list.append(obj.string)

        if len(med_list) == len(medicines_list) and len(med_list) != 0:
            patient['med'] = med_list
            target_list.append(patient)

    # 写入excel表
    excel_table = xlwt.Workbook()
    columns = ['姓名', '手机号', '加入时间', '用药']

    table = excel_table.add_sheet('数据表', cell_overwrite_ok=True)
    row_number = 0

    for i, column in enumerate(columns):
        table.write(0, i, column)

    for item in target_list:
        row_number += 1
        table.write(row_number, 0, item['real_name'])
        table.write(row_number, 1, item['mobile'])
        table.write(row_number, 2, item['created'])
        table.write(row_number, 3, item['med'])
    filename = '数据'
    excel_table.save(filename + '.xls')
    session_close()


if __name__ == '__main__':
    export_patients()