from django.shortcuts import render,HttpResponse
import openpyxl
from geopy.geocoders import Nominatim

def getlatlng(addr):
    geolocator = Nominatim(user_agent="sambathsam76@gmail.com")
    location   = geolocator.geocode(addr)
    if location:
        return location.latitude, location.longitude
    else:
        return 0,0
    
def home(request):
    try:
        if "GET" == request.method:
            return render(request, 'home.html')
        else:
            excel_file = request.FILES["excel_file"]
            response   = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{excel_file}"'
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb["Sheet1"]
            for row in worksheet.iter_rows():
                for cell in row:
                    xcel_val = getlatlng(str(cell.value))
                    for i,value_ in enumerate(xcel_val,1):
                        worksheet.cell(row=cell.row, column=cell.column+i, value=value_)
            wb.save(response)
            return response
    except Exception as e:
        print("Error:-",e)
        return HttpResponse(f"Error:-{e}")
    
    
    
    
    