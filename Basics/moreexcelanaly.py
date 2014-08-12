import xlrd
book = xlrd.open_workbook("data.xls") #open our xls file, there's lots of extra default options in this call, for logging etc. take a look at the docs
 
sheet = book.sheets()[0] #book.sheets() returns a list of sheet objects... alternatively...
sheet = book.sheet_by_name("qqqq") #we can pull by name
sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection
 
r = sheet.row(0) #returns all the CELLS of row 0,
c = sheet.col_values(0) #returns all the VALUES of row 0,
 
data = [] #make a data store
for i in xrange(sheet.nrows):
  data.append(sheet.row_values(i)) #drop all the values in the rows into data
