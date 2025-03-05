from django.shortcuts import render, redirect  
from item.models import Category, Item  
from django.contrib import messages  
import pandas as pd  
from .forms import SignUpForm, ExcelUploadForm  
from item.models import Person  
from .models import UploadedImage  # Assuming you have an Image model  

# Create your views here.  
def index(request):  
    Items = Item.objects.filter(is_sold=False)[0:6]  
    categories = Category.objects.all()  

    return render(request, 'core/index.html', {  
        'Items': Items,  
        'categories': categories,  
    })  

def contact(request):  
    return render(request, 'core/contact.html')  

def signup(request):  
    if request.method == 'POST':  
        form = SignUpForm(request.POST)  
        if form.is_valid():  
            form.save()  
            return redirect('/login/')  
    else:  
        form = SignUpForm()  

    return render(request, 'core/signup.html', {  
        'form': form,  
    })  

def sql_data(request):  
    if request.method == 'POST':  
        form = ExcelUploadForm(request.POST, request.FILES)  
        if form.is_valid():  
            # Handle Excel file upload  
            if 'excel_file' in request.FILES:  
                excel_file = request.FILES['excel_file']  
                try:  
                    # Read the Excel file  
                    df = pd.read_excel(excel_file)  
                    
                    # Get the column names from the Excel file  
                    columns = df.columns.tolist()  
                    
                    # Print column names for debugging  
                    print("Excel columns:", columns)  
                    
                    # Check if required columns exist (case-insensitive)  
                    name_col = None  
                    marks_col = None  
                    
                    for col in columns:  
                        if col.lower() == 'name':  
                            name_col = col  
                        elif col.lower() == 'marks':  
                            marks_col = col  
                    
                    if not name_col or not marks_col:  
                        missing_cols = []  
                        if not name_col:  
                            missing_cols.append("'name'")  
                        if not marks_col:  
                            missing_cols.append("'marks'")  
                        error_msg = f"Excel file must contain columns: {' and '.join(missing_cols)}. Found columns: {', '.join(columns)}"  
                        messages.error(request, error_msg)  
                        return redirect('core:sql_data')  
                    
                    # Process each row and save to database  
                    for index, row in df.iterrows():  
                        Person.objects.create(  
                            name=str(row[name_col]),  
                            marks=str(row[marks_col])  
                        )  
                    messages.success(request, f'Successfully imported {len(df)} records from Excel!')  
                except Exception as e:  
                    messages.error(request, f'Error importing Excel data: {str(e)}. Please ensure your Excel file has "name" and "marks" columns.')  
            

            if 'image' in request.FILES:  
                image_file = request.FILES['image']  
                try:  
                    UploadedImage.objects.create(image=image_file)  
                    messages.success(request, 'Image uploaded successfully!')  
                except Exception as e:  
                    messages.error(request, f'Error uploading image: {str(e)}')  
            
            return redirect('core:sql_data')  
    else:  
        form = ExcelUploadForm()  
    

    records = Person.objects.all()  
    images = UploadedImage.objects.all()  
    
    return render(request, 'core/sql_data.html', {  
        'form': form,  
        'records': records,  
        'images': images  
    })  