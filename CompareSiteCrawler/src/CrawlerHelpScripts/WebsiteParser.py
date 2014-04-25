from openpyxl import load_workbook
wb=load_workbook(r'C:\test.xlsx', use_iterators = True)
ws=wb.get_sheet_by_name('Sheet1')
for row in ws.iter_rows(row_offset=1):

    for cell in row:
        print cell.column


