'''
This script reads DICOM files in a source directory or in a list of source directories
and searches for the patients in the given patients' list creates a DICOM DataBase
in the destination directory, copies the files,
and creates a DicomDataBase.csv file and a summary.txt file.

The structure will be:
    destination --> Study_Instance_UID --> Series_Instance_UID --> DICOM_Files

@Date: 01 November 2021
@author: Amal Joseph Varghese
@email: amaljova@gmail.com
@github: https://github.com/amaljova

'''
# =========================================Need Not Modify Block=======================================

import os
from pydicom import dcmread
import shutil
import pandas as pd

def makeFolders(dir_name):
    '''To create a directory/directories if it/they are basent'''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def filterFiles(source, patients, study_dict):
    '''
    filterFiles(source = list of paths or a single path, patients = iterable patient ids,
    study_dict = an empty dict passed by calling function)
    It walks through all directories and reads all DICOM files,
    makes the DataBase and information_CSV file we want
    '''
    for root, dirs, files in os.walk(source):
        for file in files:
            try:
                f_name = os.path.join(root, file)
                header = dcmread(f_name)
                pat_id = header[(0x10, 0x20)].value  # Patient ID
                if pat_id in patients:
                    stu_inst_UID = header[(0x20, 0x0d)].value # Study Instance UID
                    ser_inst_UID = header[(0x20, 0x0e)].value # Series Instance UID
                    # -------------------data Copying---------------------------------
                    dest_dir = os.path.join(destination, stu_inst_UID)
                    dest_dir = os.path.join(dest_dir, ser_inst_UID)
                    makeFolders(dest_dir)
                    dest_file = os.path.join(dest_dir, file)
                    shutil.copy(f_name, dest_file)
                    # -------------------for data sheet (.csv)------------------------
                    modality = header[(0x08, 0x60)].value  # Modality
                    if stu_inst_UID not in study_dict.keys():
                        study_dict[stu_inst_UID] = dict()
                        print(f"Created Empty dict for {stu_inst_UID}")
                        study_dict[stu_inst_UID]['StudyInstanceUID'] = stu_inst_UID
                    study_dict[stu_inst_UID]['Patient ID'] = pat_id
                    study_dict[stu_inst_UID][f'{modality.lower()}SeriesInstanceUID'] = ser_inst_UID
            except:
                pass
    return study_dict


def makeDataBse(source='', destination='', outfile='DicomDataBase.csv', patients=[]):
    '''
    makeDataBse(source='path or list of paths', destination='path', patients=set(Patient_IDs))
    It reads all DICOM files in the source and searches for the patients in the given patients' list,
    creates a DICOM DataBase and a DicomDataBase.csv file in the destination directory.
    '''
    makeFolders(destination)
    study_dict = dict()
    if type(source) == str:
        study_dict = filterFiles(source, patients, study_dict)
    elif type(source) == list:
        for path in source:
            study_dict = filterFiles(path, patients, study_dict)
    # --------------data frame----creating csv----------------
    data_df = pd.DataFrame(study_dict.values())
    data_df.to_csv(outfile, index=False)
    print(f'Exported {outfile}')
    # --------------create summary-----------------------------
    missingPatients = patients ^ set(data_df['Patient ID'])
    summary = '===================SUMMMARY===============================\n'
    summary += f'Total Patients: {len(patients)}\n'
    summary += f"Number of Available Patients: {len(set(data_df['Patient ID']))}\n"
    summary += f'Number of Missing Patients: {len(missingPatients)}\n'
    summary += f'Missing Patients: {missingPatients}\n'
    summary += f"Available Patients: {set(data_df['Patient ID'])}\n"
    with open('summary.txt', 'w') as f:
        f.write(summary)
    print('Created summary.txt')
    #--------------console log missing patients-----------------
    print(f'Missing patients: {missingPatients}')

# =========================================FIXME Block=======================================

source = '$path'
destination = '$path'
outfile = 'DicomDataBase.csv'
patients = set(pd.read_csv('data.csv')['Patient ID'])

# =========================================Need Not Modify====================================
if __name__ == '__main__':
    makeDataBse(
        source=source,
        destination=destination,
        outfile=outfile,
        patients=patients
    )
    print('Done!')