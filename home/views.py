
######### Imports ##########33

from django.shortcuts import render,  redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
import os
import datetime
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users import forms
from home.models import Assignment, Submission
from users.models import Profile, Notification, Notification_general
import datetime
import os
from django.core.exceptions import ValidationError

###################################################################################################################################################

@login_required
def dashboard(request):
    assignment_form = forms.AssignmentForm(request.POST or None)
    search_form = forms.AssignmentSearchForm(request.GET or None)
    user_id = request.user.id
    user = request.user.profile
    created_assignment = request.user.assignments.all()
    assignments = Assignment.objects.all()
    assignments_list = Assignment.objects.all().order_by('-created_at')[0:3]
    assignment_count = assignments_list.count()
    created_assignment_count = created_assignment.count()


    if user.role == 'Teacher':
        paginator = Paginator(assignments_list, 10)
        page = request.GET.get('page')
        try:
            assignments_list = paginator.page(page)
        except PageNotAnInteger:
            assignments_list = paginator.page(1)
        except EmptyPage:
            assignments_list = paginator.page(paginator.num_pages)

        if request.method == 'GET':
            if search_form.is_valid():
                q = request.GET['q']
                assignments = assignments.annotate(
                    search=SearchVector('title', 'course_code', 'course_title'),
                    ).filter(search=SearchQuery(q))

                paginator = Paginator(assignments, 10)
                page = request.GET.get('page')
                try:
                    assignments = paginator.page(page)
                except PageNotAnInteger:
                    assignments = paginator.page(1)
                except EmptyPage:
                    assignments = paginator.page(paginator.num_pages)
            else:
                for error in search_form.errors.values():
                    messages(request, error)
                    
                context = {
                    "search_form": search_form,
                    "assignment": assignment_form,
                    "created_assignment_count": created_assignment_count,
                    'created_assignment': created_assignment,
                }
                return render(request, 'home/dashboard.html', context=context)
        context = {
            "created_assignment": created_assignment,
            "assignment": assignment_form,
            "search_form": search_form,

        }
        return render(request, 'home/dashboard.html', context=context)
    else:
        submissions = request.user.submissions.all()
        submissions_list = submissions
        search_form = forms.SubmissionSearchForm(request.GET or None)
        paginator = Paginator(submissions_list, 10)
        page = request.GET.get('page')
        try:
            submissions_list = paginator.page(page)
        except PageNotAnInteger:
            submissions_list = paginator.page(1)
        except EmptyPage:
            submissions_list = paginator.page(paginator.num_pages)

        if request.method == 'GET':
            if search_form.is_valid():
                q = request.GET['q']
                submissions = submissions.annotate(
                    search=SearchVector('matric_number'),
                    ).filter(search=SearchQuery(q))

                paginator = Paginator(submissions, 10)
                page = request.GET.get('page')
                try:
                    submissions = paginator.page(page)
                except PageNotAnInteger:
                    submissions = paginator.page(1)
                except EmptyPage:
                    submissions = paginator.page(paginator.num_pages)

                context = {
                    "search_form": search_form,
                    "submissions": submissions,
                    "assignments_list": assignments_list,
                    }
                return render(request, 'home/studs_home.html', context=context)
        context = {
            "search_form": search_form,
            "submissions": submissions,
            'assignments_list': assignments_list,
            'assignment_count': assignment_count,
        }
        return render(request, 'home/studs_home.html', context=context)


###################################################################################################################################################


@login_required
def assignment_detail(request, id):
    assignment = Assignment.objects.get(id=id)
    initial = {
        "title": assignment.title,
        "upload": assignment.upload,
        "due_date": assignment.due_date,
        "course_code": assignment.course_code,
        "course_title": assignment.course_title
        }
    assignment_form = forms.AssignmentForm(initial=initial)
    context = {
        "single_assignment": assignment,
        "assignment_id": id,
        "assignment": assignment_form
    }
    return render(request, 'home/assignment-detail.html', context=context)

@login_required
def assignment_submissions(request, id):
    assignment_id = id
    if request.user.profile.role != 'Teacher':
        return redirect('home')
    if request.user.profile.role == 'Teacher':
        search_form = forms.SubmissionSearchForm(request.GET or None)
        feedback_form = forms.FeedbackForm(request.POST or None)
        grade_form = forms.GradeForm(request.POST or None)
        assignment = Assignment.objects.get(id=id)
        submissions = assignment.submissions.all()
        submissions_list = submissions
        paginator = Paginator(submissions_list, 10)
        page = request.GET.get('page')
        try:
            submissions_list = paginator.page(page)
        except PageNotAnInteger:
            submissions_list = paginator.page(1)
        except EmptyPage:
            submissions_list = paginator.page(paginator.num_pages)

        if request.method == 'POST':
            if feedback_form.is_valid():
                feedback = request.POST['feedback']
                submission_id = request.POST['submit-feedback']
                submission = Submission.objects.get(id=submission_id)
                submission.feedback = feedback
                submission.save()
            elif grade_form.is_valid():
                grade = request.POST['grade']
                submission_id = request.POST['submit-grade']
                submission = Submission.objects.get(id=submission_id)
                submission.grade = grade
                submission.save()

        if request.method == "GET":
            if search_form.is_valid():
                q = request.GET['q']
                submissions = submissions.annotate(
                    search=SearchVector('matric_number'),
                    ).filter(search=SearchQuery(q))

                paginator = Paginator(submissions, 10)
                page = request.GET.get('page')
                try:
                    submissions = paginator.page(page)
                except PageNotAnInteger:
                    submissions = paginator.page(1)
                except EmptyPage:
                    submissions = paginator.page(paginator.num_pages)

                context = {
                    "search_form": search_form,
                    "submissions": submissions
                }
                return render(request, 'home/assignment-submissions.html', context=context)

        context = {
                "search_form": search_form,
                "submissions": submissions,
                "grade_form": grade_form,
                "feedback_form": feedback_form,
                "assignment_id": assignment_id
            }
        return render(request, 'home/assignment-submissions.html', context=context)

###################################################################################################################################################
@login_required
def delete_assignment(request, id):
    assignment = Assignment.objects.get(id=id)
    user_id = assignment.user_id
    if user_id == request.user.id:
        assignment.delete()
        messages.success(request, "Assignment was successfully deleted")
        return redirect('home')
    else:
        context = {
            "single_assignment": assignment,
            "assignment_id": id
        }
        messages.error(request, "You are not authorized to carry out this operation")
        return render(request, 'home/assignment-detail.html', context=context)


###################################################################################################################################################

@login_required
def edit_assignment(request, id):
    assignment = Assignment.objects.get(id=id)
    user_id = assignment.user_id
    initial = {
        "title": assignment.title,
        "upload": assignment.upload,
        "due_date": assignment.due_date,
        "course_code": assignment.course_code,
        "course_title": assignment.course_title
        }
    assignment_form = forms.AssignmentForm(request.POST, request.FILES, instance=assignment, initial=initial)
    if request.method == "POST":

        if assignment_form.is_valid():
            current_user = request.user.id
            if current_user == user_id:
                assignment_form.save()
                assignment.last_updated = datetime.date.today()
                assignment.save()
                messages.success(request, 'Assignment was successfully edited.')
                new_data = Assignment.objects.last()
                return redirect('assignment_detail', id=new_data.id)
            else:
                messages.error(request, "You are not authorized to carry out this operation")
        else:
            for error in assignment_form.errors.values():
                messages.error(request, error)
            
    context = {
        "assignment": assignment_form,
        "assignment_id": id
    }
    return render(request, "home/assignment-detail.html", context=context)


###################################################################################################################################################

def pre_submission(request, id):
    # if not request.user.is_authenticated():
    #   return redirect('/')  
    pass_form = forms.PassForm(request.POST or None)
    if request.method == "POST":
        assignment = Assignment.objects.get(id=id)
        if pass_form.is_valid():
            passcode = request.POST["passcode"]
            if passcode == assignment.passcode:
                request.session['passcode'] = passcode
                return redirect('assignment_submission', id=id)
            else:
                messages.error(request, "Passcode does not match")
        else:
            for error in pass_form.errors.values():
                messages.error(request, error)

    submission_form = forms.SubmissionForm()
    context = {
        "pass": pass_form,
        "assignment_id": id,
        "submission": submission_form
    }
    return render(request, "home/pass.html", context)


###################################################################################################################################################


@login_required
def all_assignment(request):
    user = request.user.profile
    if user.role == 'Teacher':
        return redirect('home')
    submissions = Submission.objects.all()

    assignment_all = Assignment.objects.all().order_by('-created_at')
    assignment_count = assignment_all.count()
    date = datetime.date.today()
    context={'assignment_all': assignment_all, 'submissions': submissions , 'date':date}
    return render(request, 'home/assignment.html', context)


###################################################################################################################################################


@login_required
def submit_assignment(request, id):
    user = request.user.profile
    if user.role == 'Teacher':
        return redirect('home')
    assignments_list = Assignment.objects.all()
    assignment_count = assignments_list.count()
    assignment = Assignment.objects.get(id=id)
    if assignment.due_date > datetime.date.today():
        if request.method == "POST":
            file_upload = request.FILES.get('upload')
            if file_upload != None:
                ext = os.path.splitext(file_upload.name)[1]  # [0] returns path+filename
                valid_img_extensions = ['.jpeg' , '.jpg', '.png', '.pdf']
                if ext.lower() not in valid_img_extensions:
                    messages.error(request, 'File extension not valid')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_id = request.user.id
            assignment_id = id
            description = request.POST.get('description')
            print(len(description))
            if  file_upload == None and  len(description) < 1:
                messages.error(request, 'Please upload an image or description')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
            following = Assignment.objects.get(id=id)
            following.submmetted_by.add(request.user)
            submission = Submission(user_id=user_id, upload=file_upload,descprition=description, assignment_id=assignment_id)
            messages.success(request, 'Assignment successfully submitted')
            submission.save()
            return redirect('submission_detail', id=submission.id)


        context = {
            # "submission": submission_form,
            "assignment_id": id,
            "assignment": assignment,
            'assignments_list':assignments_list,
            'assignment_count':assignment_count,
        }
        return render(request, "home/submit_assignment.html", context=context)
    else:
        context = {
            "assignment_id": id,
        }
        return render(request, "home/deadline.html", context=context)


###################################################################################################################################################


@login_required
def all_assignment_submmission(request):
    user = request.user.profile
    if user.role != 'Teacher':
        return redirect('home') 
    user_id = request.user.id
    user = request.user.profile
    assignments = request.user.assignments.all().order_by('-created_at')
    assignments_list = assignments

    context = {
        "assignments": assignments,

    }
    return render(request, 'home/all_assignment_submmission.html', context)



###################################################################################################################################################

@login_required
def create_assignment(request):
    assignment_form = forms.AssignmentForm(request.POST or None)
    if request.user.profile.role == 'Teacher':
        if request.method == "POST":
            title =  request.POST.get('title')
            if len(title) < 1:
                messages.error(request, 'Please enter your Assignment title')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            file_upload = request.FILES.get('upload')
            if file_upload != None:
                ext = os.path.splitext(file_upload.name)[1]  # [0] returns path+filename
                valid_img_extensions = ['.jpeg' , '.jpg', '.png', '.pdf']
                if ext.lower() not in valid_img_extensions:
                    messages.error(request, 'File extension not valid')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            due_date = request.POST.get('due_date')
            if len(due_date) < 5:
                messages.error(request, 'Please enter the Deadline')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            description = request.POST.get('description')
            Assignment_sub =  Assignment(upload=file_upload,title=title, descprition=description,due_date=due_date,user_id=request.user.id)
            Assignment_sub.save()
            messages.success(request, 'Assignment was successfully created.')
            usr = Profile.objects.filter(role='Student')
            mess = f"{request.user.first_name} {request.user.last_name} added an Assignment"
            for user in usr:
                noti = Notification(user =user.user, message=mess, link = f"/assignments/{Assignment_sub.id}/submission/")
                noti.save()
            return redirect('home')
        #     if assignment_form.is_valid():
        #         assignment = assignment_form.save(commit=False)
        #         assignment.user_id = request.user.id
        #         assignment.save()
        #         new_data = Assignment.objects.last()
        #         messages.success(request, 'Assignment was successfully created.')
        #         return redirect('home')
        #     else:
        #         for error in assignment_form.errors.values():
        #             messages.error(request, error)
        # context = {
        #     "assignment": assignment_form,
        # }


        return render(request, "home/create_assignment.html")
    else:
        messages.error(request, 'Only Lecturer accounts can create assignments')
        context = {
            "assignment": assignment_form
        }
        return render(request, "home/create_assignment.html", context=context)


###################################################################################################################################################

@login_required
def all_submmission(request):
    user = request.user.profile
    if user.role == 'Teacher':
        return redirect('home') 
    submission = Submission.objects.filter(user=request.user)
    context = {
        'submission':submission,
    }
    return render(request, 'home/all_submmission.html', context)

###################################################################################################################################################



@login_required
def submission_detail(request, id):
    submission = Submission.objects.get(id=id)
    context = {
        "single_submission": submission,
        "submission_id": id
    }
    return render(request, 'home/submission-detail.html', context=context)


###################################################################################################################################################

@login_required
def delete_submission(request, id):
    submission = Submission.objects.get(id=id)
    if submission.user_id == request.user.id:
        assignment_id = submission.assignment_id
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.submmetted_by.remove(request.user)
        submission.delete()
        messages.success(request, 'Assignment successfully deleted')
        return redirect('home')
    else:
        context = {
            "single_submission": submission,
            "submission_id": id
        }
        messages.error(request, "You are not authorized to carry out this operation")
        return render(request, 'home/submission-detail.html', context=context)

###################################################################################################################################################

@login_required
def edit_submission(request, id):
    submission = Submission.objects.get(id=id)
    assignment_id = submission.assignment_id
    assignment = Assignment.objects.get(id=assignment_id)
    user_id = submission.user_id
    initial = {
        "upload": submission.upload
        }
    submission_form = forms.SubmissionForm(request.POST, request.FILES, instance=submission, initial=initial)
    if request.method == "POST":
        if assignment.due_date > datetime.date.today():
            if submission_form.is_valid():
                current_user = request.user.id
                if current_user == user_id:
                    submission_form.save()
                    submission.last_updated = datetime.date.today()
                    submission.save()
                    messages.success(request, 'Submission was successfully edited.')
                    new_data = Submission.objects.last()
                    return redirect('submission_detail', id=new_data.id)
                else:
                    messages.error(request, "You are not authorized to carry out this operation")
            else:
                for error in submission_form.values():
                    messages.error(request, error)
                
        else:
            messages.error(request, "The due date for this assignment has passed")
    context = {
        "submission": submission_form,
        "submission_id": id,
        "single_submission": submission
    }
    return render(request, "home/submission-detail.html", context=context)


###################################################################################################################################################


@login_required
def assignments_detail(request, id):
    user = request.user.profile
    if user.role == 'Teacher':
        return redirect('home')
    assignments_list = Assignment.objects.all()
    assignment_count = assignments_list.count()
    assignment = Assignment.objects.get(id=id)




    ext = os.path.splitext(assignment.upload.name)[1]  # [0] returns path+filename
    valid_img_extensions = ['.jpeg' , '.jpg', '.png']
    if ext.lower() in valid_img_extensions:

        context = {
            "assignment_id": id,
            "assignment": assignment,
            'assignments_list':assignments_list,
            'assignment_count':assignment_count,
            'ext': ext,
            'valid_img_extensions': valid_img_extensions,
        }
        return render(request, "home/assignment_detail.html", context=context)



    # if assignment.upload 
    # print(assignment.upload)

    context = {
        "assignment_id": id,
        "assignment": assignment,
        'assignments_list':assignments_list,
        'assignment_count':assignment_count,
    }

    return render(request, "home/assignment_detail.html", context=context)


###################################################################################################################################################

@login_required
def all_notification(request):
    user = request.user.profile
    if user.role == 'Teacher':
        return redirect('home')
    noti = Notification.objects.filter(user=request.user).order_by('-created_at')
    noti_general = Notification_general.objects.filter(user=request.user).order_by('-created_at')
    # noti = serializers.serialize('json', noti)
    Notification.objects.filter(user=request.user, seen = False).update(seen = True)
    Notification_general.objects.filter(user=request.user, seen = False).update(seen = True)
    context = {
        'noti':noti,
        'noti_general':noti_general,
    }
    return render(request, 'home/notifications.html', context)

###################################################################################################################################################


@login_required
def notifications_seen(request):
    Notification.objects.filter(user=request.user, seen = False).update(seen = True)
    return HttpResponse(True)

###################################################################################################################################################

@login_required
def gen_notification_seen(request):
    Notification_general.objects.filter(user=request.user, seen = False).update(seen = True)
    return HttpResponse(True)



###################################################################################################################################################



def create_Notification(request):
    user = request.user.profile
    if user.role != 'Teacher':
        return redirect('home')
    if request.method == "POST":   
        message = request.POST.get('message')
        if len(message) < 5:
            messages.error(request, 'You must add atleast 5 words in your discprition')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        title = request.POST.get('ann_title')
        if len(title) < 1:
            messages.error(request, 'Plese add your title')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        files =  request.FILES.get('ann_upload')


        if files != None:

            ext = os.path.splitext(files.name)[1] 
            valid_img_extensions = ['.jpeg' , '.jpg', '.png']

            if ext.lower() not in valid_img_extensions:
                messages.error(request, 'Only Images are allowed')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        parents_avaviality = request.POST.get('selector')
        if parents_avaviality != 'Yes' and 'No':
            messages.error(request, 'You cannot change the parents avaviality option')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




        usr = Profile.objects.filter(role='Student')
        for user in usr:
            noti_gen = Notification_general(user = user.user,  message=message, title=title ,files = files, parents_avaviality=parents_avaviality )
            noti_gen.save()
            print(user.user)

        messages.success(request, 'You announcement has been successfully sent')
        # print(message, title, parents_avaviality)

    return render(request, 'home/add_announcement.html')



###################################################################################################################################################


def csrf_failure(request,  reason=""):
    return render(request, 'home/crsf_faliure.html')

################################################################################################################################################################################################################################################################



def test(request):
    return render(request, 'test.html')