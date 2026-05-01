from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(["Test"])
wb.save("test.xlsx")
print("Berhasil menulis test.xlsx")