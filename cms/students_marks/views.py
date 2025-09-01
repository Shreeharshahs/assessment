from django.shortcuts import render,redirect
from .forms import LoginForm,StudentForm,RegisterForm
from .models import Teacher,Student,AuditLog
from .utils import verify_password,calculate_new_marks,generate_salt,hash_password
from .session_store import create_session, destroy_session, get_teacher_id_from_token
from django.http import JsonResponse
from django.contrib import messages



def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                teacher = Teacher.objects.get(teacher_name=username)
                if verify_password(password, teacher.salt, teacher.password_hash):
                    token = create_session(teacher.id)
                    request.session['teacher_id'] = teacher.id
                    response = redirect('home')  # redirect to home page
                    response.set_cookie('session_token', token, httponly=True, samesite='Strict')
                    return response
                else:
                    messages.error(request, 'Invalid Password')
            except Teacher.DoesNotExist:
                messages.error(request, 'Invalid Username')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})



def logout_view(request):
    token = request.COOKIES.get('session_token')
    destroy_session(token)
    response = redirect('login')
    response.delete_cookie('session_token')
    request.session.flush() # to remove the sessionID cookie
    return response

def home_view(request):
    if not request.teacher:
        return redirect('login')

    students = Student.objects.all().order_by('name')
    form = StudentForm()
    return render(request, 'home.html', {
        'students': students,
        'form': form,
        'teacher': request.teacher
    })

def register_view(request):
    error = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmed_password = form.cleaned_data['c_password']
            if password == confirmed_password:
                try:
                    salt = generate_salt()
                    hashed = hash_password(password, salt)
                #print(salt," ----- ",hashed)

                    Teacher.objects.create(teacher_name=username, salt=salt, password_hash=hashed)
                #print("new teacher created")
                    response = redirect('login')  # redirect to home page
                    return response
        
                except:
                    messages.error(request, 'Something went wrong')
            else:
                messages.error(request,'Passwords not matching')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'error': error})


def add_student_view(request):
    if not request.teacher:
        return redirect('login')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = str(form.cleaned_data['name']).lower
            subject = str(form.cleaned_data['subject']).lower
            new_marks = form.cleaned_data['marks']

            student, created = Student.objects.get_or_create(name=name, subject=subject,defaults={'marks': new_marks})
            old_marks = 0 #for audit log
            if not created:
                total = calculate_new_marks(student.marks, new_marks)
                if total > 100:
                    return JsonResponse({'error': 'Total marks cannot exceed 100'}, status=400)
                student.marks = total
                student.save()
                action = f"Updated marks from {old_marks} to {student.marks} via add_student"
            else:
                old_marks = student.marks
                student.marks = new_marks
                student.save()
                action = "Created student record"

            AuditLog.objects.create(teacher=request.teacher, student=student, action=action)
            return JsonResponse({'success': True})
        
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    

def edit_marks_view(request, student_id):
    if not request.teacher:
        return redirect('login')

    if request.method == 'POST':
        try:
            old_marks=0 # to display in audit log only
            new_marks = int(request.POST.get('marks'))
            if not (0 <= new_marks <= 100):
                return JsonResponse({'error': 'Marks must be between 0 and 100'}, status=400)
            
            student = Student.objects.get(id=student_id)
            old_marks=student.marks
            student.marks = new_marks
            student.save()

            AuditLog.objects.create(
                teacher=request.teacher,
                student=student,
                action=f"Updated marks from {old_marks} to {new_marks}",
                
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def delete_student_view(request, student_id):
    if not request.teacher:
        
        return redirect('login')

    try:
        student = Student.objects.get(id=student_id)
        AuditLog.objects.create(
            teacher=request.teacher,
            student=student,
            action="Deleted student record"
        )
        student.delete()
        return JsonResponse({'success': True})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


def audit_log_view(request):
    token = request.COOKIES.get('session_token')
    teacher = get_teacher_id_from_token(token) 
    if not teacher:
        request.session.flush()
        return redirect("login")
    
    logs = AuditLog.objects.all().order_by("-timestamp")
    return render(request, "audit_log.html", {"logs": logs})