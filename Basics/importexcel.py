#import xlrd
import xlrd
 
#Open a workbook
workbook = xlrd.open_workbook('statistics.xls')
 
#Get a sheet by index
sheet = workbook.sheet_by_index(0)
 
#Or by name
sheet = workbook.sheet_by_name('Sheet1')
 
#Access the cell value at (2,2)
print sheet.cell_value(2,2)
