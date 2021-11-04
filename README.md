# Fix a DICOM DataBase

This script reads DICOM files in a source directory or in a list of source directories and searches for the patients in the given patients 'list creates a DICOM DataBase in the destination directory, copies the files, and creates a DicomDataBase.csv file and a summary.txt file.

---
The created directory's structure will be:
> destination --> Study_Instance_UID --> Series_Instance_UID --> DICOM_Files
---
>
> * @Date: 01 November 2021
> * @author: Amal Joseph Varghese
> * @email: amaljova@gmail.com
> * @github: <https://github.com/amaljova>
