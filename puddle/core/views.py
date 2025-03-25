from django.shortcuts import render, redirect, get_object_or_404  
from item.models import Category, Item  
from django.contrib import messages  
import pandas as pd  
from .forms import SignUpForm, ExcelUploadForm, ExcelDataForm  
from .models import ExcelData  
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import logout 
from django.contrib import messages 

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

def logoutUser(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('core:login')
@login_required
def sql_data(request):  
    if request.method == 'POST':  
        form = ExcelUploadForm(request.POST, request.FILES)  
        if form.is_valid():  
            excel_file = request.FILES['excel_file']  
            try:  
                # Read the Excel file  
                df = pd.read_excel(excel_file)  
                
                # Get the column names from the Excel file  
                columns = df.columns.tolist()  
                
                # Check if required columns exist (case-insensitive)  
                name_col = None  
                marks_col = None  
                email_col = None  
                
                for col in columns:  
                    if col.lower() == 'name':  
                        name_col = col  
                    elif col.lower() == 'marks':  
                        marks_col = col  
                    elif col.lower() == 'email':  
                        email_col = col  
                
                if not name_col or not marks_col or not email_col:  
                    missing_cols = []  
                    if not name_col:  
                        missing_cols.append("'name'")  
                    if not marks_col:  
                        missing_cols.append("'marks'")  
                    if not email_col:  
                        missing_cols.append("'email'")  
                    error_msg = f"Excel file must contain columns: {' and '.join(missing_cols)}. Found columns: {', '.join(columns)}"  
                    messages.error(request, error_msg)  
                    return redirect('core:sql_data')  
                
                # Process each row and save to database  
                for index, row in df.iterrows():  
                    ExcelData.objects.create(  
                        name=str(row[name_col]),  
                        marks=int(row[marks_col]),  
                        email=str(row[email_col])  
                    )  
                messages.success(request, f'Successfully imported {len(df)} records from Excel!')  
                return redirect('core:sql_data')  
            except Exception as e:  
                messages.error(request, f'Error importing Excel data: {str(e)}. Please ensure your Excel file has "name", "marks", and "email" columns.')  
    else:  
        form = ExcelUploadForm()  
    
    records = ExcelData.objects.all()  
    
    return render(request, 'core/sql_data.html', {  
        'form': form,  
        'records': records,  
    })  

@login_required
def edit_sql(request):  
    records = ExcelData.objects.all()  
    return render(request, 'core/edit_sql.html', {  
        'records': records,  
    })  

@login_required
def add_record(request):  
    if request.method == 'POST':  
        form = ExcelDataForm(request.POST)  
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Record added successfully!')  
            return redirect('core:edit_sql')  
    else:  
        form = ExcelDataForm()  
    
    return render(request, 'core/add_record.html', {  
        'form': form,  
    })  

@login_required
def edit_record(request, pk):  
    record = get_object_or_404(ExcelData, pk=pk)  
    if request.method == 'POST':  
        form = ExcelDataForm(request.POST, instance=record)  
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Record updated successfully!')  
            return redirect('core:edit_sql')  
    else:  
        form = ExcelDataForm(instance=record)  
    
    return render(request, 'core/edit_record.html', {  
        'form': form,  
        'record': record,  
    })  

@login_required
def delete_record(request, pk):  
    record = get_object_or_404(ExcelData, pk=pk)  
    if request.method == 'POST':  
        record.delete()  
        messages.success(request, 'Record deleted successfully!')  
        return redirect('core:edit_sql')  
    
    return render(request, 'core/delete_record.html', {  
        'record': record,  
    })  