from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User,Designation
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Group, Marks
from django.contrib import messages
from django.shortcuts import render
from .models import Group, Marks
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponse
import csv
from django.http import HttpResponse
from .models import Group, Marks


# def login_view(request):
#     if request.method == "GET":
#         designation1 = Designation.objects.all()
#         content={
#             'designation1': designation1
#         }
#         return render(request, 'login.html',content)

#     if request.method == "POST":
#         role_name = request.POST.get('role')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             designation = Designation.objects.get(designationname=role_name)
#             user = User.objects.get(email=email, designation=designation)

#             if user.check_password(password):
#                 messages.success(request, f"Welcome {user.name}!")
#                 request.session['is_logged_in'] = True 
#                 request.session['user_id'] = user.id 
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, "Invalid password.")
#         except (User.DoesNotExist, Designation.DoesNotExist):
#             messages.error(request, "User or role does not exist.")

#     return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Designation

designation1 = Designation.objects.all()
content_login = {
            'designation1': designation1
        }
def login_view(request):
    if request.method == "GET":
        # designation1 = Designation.objects.all()
        # content = {
        #     'designation1': designation1
        # }
        return render(request, 'login.html', content_login)

    if request.method == "POST":
        role_name = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            designation = Designation.objects.get(designationname=role_name)
            user = User.objects.get(email=email, designation=designation)

            if user.check_password(password):
                messages.success(request, f"Welcome {user.name}!")
                request.session['is_logged_in'] = True
                request.session['user_id'] = user.id

                # Check designation and redirect accordingly
                if designation.designationname in ["faculty", "Faculty","FACULTY"]:
                    return redirect('dashboard')  # Add this name in your urls.py
                else:
                    return redirect('dashboard')  # General dashboard

            else:
                messages.error(request, "Invalid password.")
        except (User.DoesNotExist, Designation.DoesNotExist):
            messages.error(request, "User or role does not exist.")

    return render(request, 'login.html',content_login)


# def staff_dashboard(request):
#     user_id = request.session.get('user_id')  # Assuming you stored the user ID in the session
#     user = User.objects.get(id=user_id)  # Fetch the user from the database
#     group=Group.objects.all().count()
#     role=user.designation.designationname.lower()
#     content={
        
#         'user_name':user.name,
#         'group':group,
#         'user_role':role

#     }
#     return render(request, 'staff_dashboard.html')

# add for admin and employee setting


def dashboard(request):
     # Get user information from the session or database
    user_id = request.session.get('user_id')  # Assuming you stored the user ID in the session
    user = User.objects.get(id=user_id)  # Fetch the user from the database
    group=Group.objects.all().count()
    role=user.designation.designationname.lower()
    if role in ["director", "manager", "coordinator"]:
        role="admin"
    else:
        role="faculty"
    # add coordinator = admin
    content={
        
        'user_name':user.name,
        'group':group,
        'user_role':role

    }
    return render(request, 'dashboard.html' ,content)

def add_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phoneno = request.POST['phoneno']
        designation_id = request.POST['designation']

        try:
            designation = Designation.objects.get(id=designation_id)
        except Designation.DoesNotExist:
            messages.error(request, 'Invalid designation selected.')
            return redirect('add_user')

        new_user = User(
            name=name,
            email=email,
            password=password,
            phoneno=phoneno,
            designation=designation
        )

        new_user.save()
        messages.success(request, 'User added successfully!')
        return redirect('dashboard')

    # Fetch designations for dropdown
    designations = Designation.objects.all()
    return render(request, 'add_user.html', {'designations': designations})

def success(request):
    return render(request, 'sucess.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def add_marks(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        project_marks = int(request.POST.get('project_marks'))
        poster_marks = int(request.POST.get('poster_marks'))

        if not (1 <= project_marks <= 5 and 1 <= poster_marks <= 5):
            messages.error(request, "Marks must be between 1 and 5.")
            return redirect('add_marks')

        try:
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "Session expired. Please login again.")
                return redirect('login')

            user = User.objects.get(id=user_id)
            group = Group.objects.get(id=group_id)

            if Marks.objects.filter(group=group, user=user).exists():
                messages.warning(request, "You have already added marks for this group.")
                return redirect('add_marks')

            Marks.objects.create(
                user=user,
                group=group,
                project_marks=project_marks,
                poster_marks=poster_marks
            )
            messages.success(request, "Marks added successfully.")
        except Group.DoesNotExist:
            messages.error(request, "Group not found.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")

        return redirect('add_marks')

    # ✅ Only exclude groups marked by this user
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    marked_groups = Marks.objects.filter(user=user).values_list('group_id', flat=True)
    groups = Group.objects.exclude(id__in=marked_groups)

    return render(request, 'add_marks.html', {'groups': groups})




def marksheet(request):
    groups = Group.objects.all()
    data = []

    for group in groups:
        group_marks = group.marks.all()
        total_project = sum(m.project_marks for m in group_marks)
        total_poster = sum(m.poster_marks for m in group_marks)
        count = group_marks.count()

        avg_project = total_project / count if count else 0
        avg_poster = total_poster / count if count else 0

        data.append({
            'group': group.groupname,
            'group_shift':group.shift,
            'members': group.get_members(),
            'avg_project': avg_project,
            'avg_poster': avg_poster,
        })

    return render(request, 'marksheet.html', {'data': data})

def group_all_marks(request):
    groups = Group.objects.all()
    group_data = []

    for group in groups:
        marks = Marks.objects.filter(group=group)
        entries = []

        for mark in marks:
            entries.append({
                'user': mark.user.name,
                'project_marks': mark.project_marks,
                'poster_marks': mark.poster_marks
            })

        group_data.append({
            'groupname': group.groupname,
            'shift': group.shift,
            'members': group.get_members(),
            'marks_entries': entries
        })

    return render(request, 'group_all_marks.html', {'group_data': group_data})



import csv
from django.http import HttpResponse
from .models import Group, Marks  # Make sure these are correctly imported

def export_marks_pdf(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="group_marks.csv"'

    writer = csv.writer(response)
    
    # CSV header
    writer.writerow(['GROUP NAME', 'SHIFT', 'USER NAME', 'PROJECT MARKS', 'POSTER MARKS', 'TOTAL MARKS', 'RESULT'])
    writer.writerow(['' for _ in range(7)])  # Empty row for spacing

    groups = Group.objects.all()

    for group in groups:
        writer.writerow(['-' * 80])
        writer.writerow([f"Group: {group.groupname}", f"Shift: {group.shift}"])
        writer.writerow([])

        marks = Marks.objects.filter(group=group)

        for mark in marks:
            total_marks = mark.project_marks + mark.poster_marks  # Example result logic
            writer.writerow([
                group.groupname,
                group.shift,
                mark.user.name,
                mark.project_marks,
                mark.poster_marks,
                total_marks
            ])

        writer.writerow([])

    return response
