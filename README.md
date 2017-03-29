1, Try example
(1) Download the source file
(2) Import into IDE
(3) Go to lib folder, running script: python recover.py


2, Recover API description
(1) Recover(excel_name, dict_file="wu.dic")
This API is used to create a Recover object. 
excel_name is the excel file you want to mark or repair, which may
contain error.
dict_file: to mark or repair this excel, we will generate a dic
according to the text of this excel. If you don't specify a name,
default value 'wu.dic' will be used.
(2) mark_error(excel_output)
This API is used to mark error in excel and output to excel. For the 
error cell will be marked red.
(3) repair_excel(excel_output)
This API is used to repair an excel contain error, and output the repair
excel.
For cell contain error will be marked red, for those repaired cell will
be marked yellow.
