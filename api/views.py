from .serializers import (AssignmentSerializer, AssistantSerializer,
                          CommentSerializer, CoordinatorSerializer,
                          FileSerializer, GradeSerializer,
                          GroupRequestSerializer, GuideSerializer,
                          PreferenceSerializer, ProjectRequestSerializer,
                          ProjectSerializer, StudentSerializer, TeamSerializer)
from .models import (Assignment, Assistant, Comment, Coordinator, File, Grade,
                     GroupRequest, Guide, Preference, Project, ProjectRequest,
                     Student, Team)
import constants
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from django.utils import timezone
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout


# * COORDINATOR


@api_view()
def coordinatorStudent(request):
    response = []
    for student in Student.objects.all().order_by('roll_number'):
        student_data = {
            "student_branch": student.branch,
            "student_email": student.email,
            "student_id": student.id,
            "student_name": student.name,
            "student_roll_number": student.roll_number,
        }
        try:
            project = Project.objects.get(student=student)
            student_data.setdefault("project_id", project.id)
            student_data.setdefault("project_name", project.title)
        except:
            student_data.setdefault("project_id", None)
            student_data.setdefault("project_name", None)
        try:
            team = Team.objects.get(id=student.team.id)
            student_data.setdefault("group_id", team.id)
        except:
            student_data.setdefault("group_id", None)
        try:
            guide = Guide.objects.get(id=team.guide_id)
            student_data.setdefault("guide_id", guide.id)
            student_data.setdefault("guide_name", guide.name)
        except:
            student_data.setdefault("guide_id", None)
            student_data.setdefault("guide_name", None)
        response.append(student_data)
    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorStudentDetail(request, id):
    response = {}
    try:
        student = Student.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    student_data = {
        "student_branch": student.branch,
        "student_email": student.email,
        "student_id": student.id,
        "student_name": student.name,
        "student_roll_number": student.roll_number,
    }
    try:
        project = Project.objects.get(student=student)
        student_data.setdefault("project_id", project.id)
        student_data.setdefault("project_name", project.title)
    except:
        student_data.setdefault("project_id", None)
        student_data.setdefault("project_name", None)
    try:
        team = Team.objects.get(id=student.team.id)
        student_data.setdefault("group_id", team.id)
    except:
        student_data.setdefault("group_id", None)
    try:
        guide = Guide.objects.get(id=team.guide_id)
        student_data.setdefault("guide_id", guide.id)
        student_data.setdefault("guide_name", guide.name)
    except:
        student_data.setdefault("guide_id", None)
        student_data.setdefault("guide_name", None)
    response = student_data
    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorGroup(request):
    response = []
    for team in Team.objects.all().order_by('id'):
        team_data = {
            "team_id": team.id,
        }
        project_data = {}
        try:
            project = Project.objects.get(team_id=team.id)
            project_data.setdefault("project_id", project.id)
            project_data.setdefault("project_name", project.title)
            project_data.setdefault("project_type", project.category)
        except:
            project_data.setdefault("project_id", None)
            project_data.setdefault("project_name", None)
            project_data.setdefault("project_type", None)
        team_data.setdefault("project_data", project_data)
        try:
            # ! team without students should not exist
            students = Student.objects.filter(team_id=team.id)
            leader = Student.objects.get(id=team.leader_id)
            students_data_array = []
            for student in students:
                student_data = {}
                student_data.setdefault("student_id", student.id)
                student_data.setdefault("student_name", student.name)
                student_data.setdefault(
                    "student_photo", student.photo or None)
                students_data_array.append(student_data)
            team_data.setdefault("leader_name", leader.name)
            team_data.setdefault("student_data", students_data_array)
        except:
            team_data.setdefault("leader_name", None)
            team_data.setdefault("student_data", None)
        guide_data = {}
        try:
            guide = Guide.objects.get(id=team.guide_id)
            guide_data.setdefault("guide_id", guide.id)
            guide_data.setdefault("guide_photo", guide.photo or None)
            guide_data.setdefault("guide_name", guide.name)
        except:
            guide_data.setdefault("guide_id", None)
            guide_data.setdefault("guide_name", None)
            guide_data.setdefault("guide_photo", None)
        team_data.setdefault("guide_data", guide_data)
        response.append(team_data)
    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorGuide(request):
    response = []
    for guide in Guide.objects.all():
        guide_data = {
            "guide_branch": guide.branch,
            "guide_id": guide.id,
            "guide_name": guide.name
        }
        try:
            teams = Team.objects.filter(guide=guide)
            team_data = []
            for team in teams:
                temp_team_data = {
                    "team_id": team.id
                }
                try:
                    project = Project.objects.get(team=team)
                    temp_team_data.setdefault("project_id", project.id)
                    temp_team_data.setdefault("project_title", project.title)
                except:
                    temp_team_data.setdefault("project_id", None)
                    temp_team_data.setdefault("project_title", None)
                finally:
                    team_data.append(temp_team_data)
            guide_data.setdefault("team_data", team_data)
        except:
            guide_data.setdefault("team_data", None)
        response.append(guide_data)

    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorGuideDetail(request, id):
    response = {}
    try:
        guide = Guide.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    preferences = []
    for preference in guide.preferences.all():
        p = Preference.objects.get(id=preference.id)
        preferences.append(
            {"area_of_interest": p.area_of_interest, "thrust_area": p.thrust_area})
    guide_data = {
        "guide_branch": guide.branch,
        "guide_id": guide.id,
        "guide_name": guide.name,
        "guide_email": guide.email,
        "guide_preferences": preferences,
    }
    try:
        teams = Team.objects.filter(guide=guide)
        team_data = []
        for team in teams:
            temp_team_data = {
                "team_id": team.id
            }
            try:
                project = Project.objects.get(team=team)
                temp_team_data.setdefault("project_id", project.id)
                temp_team_data.setdefault("project_title", project.title)
            except:
                temp_team_data.setdefault("project_id", None)
                temp_team_data.setdefault("project_title", None)
            finally:
                team_data.append(temp_team_data)
        guide_data.setdefault("team_data", team_data)
    except:
        guide_data.setdefault("team_data", None)

    response = guide_data
    print(response)
    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorProject(request):
    # todo: if submitted link should be disabled
    response = []
    for team in Team.objects.all().order_by("id"):
        project_data = {
            "team_id": team.id
        }
        try:
            project = Project.objects.get(team=team)
            project_data.setdefault("project_exists", True)
            project_data.setdefault("project_id", project.id)
            project_data.setdefault("project_status", project.status)
            project_data.setdefault("project_title", project.title)
            project_data.setdefault("project_category", project.category)
            project_data.setdefault("project_domain", project.domain)
            project_data.setdefault("project_description", project.description)
            project_data.setdefault(
                "project_explanatory_field", project.explanatory_field or None)
        except:
            project_data.setdefault("project_exists", False)
        try:
            guide = Guide.objects.get(id=team.guide.id)
            project_data.setdefault("guide_name", guide.name)
            project_data.setdefault("guide_id", guide.id)
        except:
            project_data.setdefault("guide_name", None)
            project_data.setdefault("guide_id", None)
        response.append(project_data)
    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorProjectDetail(request, id):
    response = {}
    try:
        project = Project.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    team = Team.objects.get(team_id=project.team.id)
    project_data = {
        "team_id": team.id
    }
    try:
        project_data.setdefault("project_exists", True)
        project_data.setdefault("project_id", project.id)
        project_data.setdefault("project_status", project.status)
        project_data.setdefault("project_title", project.title)
        project_data.setdefault("project_category", project.category)
        project_data.setdefault("project_domain", project.domain)
        project_data.setdefault("project_description", project.description)
        project_data.setdefault(
            "project_explanatory_field", project.explanatory_field or None)
    except:
        project_data.setdefault("project_exists", False)
    try:
        guide = Guide.objects.get(team=team)
        project_data.setdefault("guide_name", guide.name)
        project_data.setdefault("guide_id", guide.id)
    except:
        project_data.setdefault("guide_name", None)
        project_data.setdefault("guide_id", None)
    response = project_data

    return Response(data=response, status=status.HTTP_200_OK)


@api_view()
def coordinatorAssignmentList(request):
    data = Assignment.objects.all()
    serializer = AssignmentSerializer(
        data, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def coordinatorAssignmentDetail(request, id):
    if request.method == "GET":
        try:
            assignment = Assignment.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response = {}
        # assignment details
        assignment_details = {}
        files = File.objects.filter(assignment=assignment).filter(team=None)
        _files = []
        for file in files:
            _files.append({
                "file_id": file.id,
                "file_name": file.file.name,
                "file_url": file.file.url,
            })
        _assignment = {
            "assignment_id": assignment.id,
            "assignment_title": assignment.title,
            "assignment_weightage": assignment.weightage,
            "assignment_description": assignment.description,
            "assignment_due_on": assignment.due,
            "assignment_posted_on": assignment.posted
        }
        assignment_details.setdefault("assignment", _assignment)
        assignment_details.setdefault("files", _files)
        response.setdefault("assignment_details", assignment_details)
        # submission status
        submission_status = []
        for team in Team.objects.all():
            _submission_status = {
                "team_id": team.id
            }
            try:
                grade = Grade.objects.get(student=team.leader)
                if grade.turned_in:
                    _submission_status.setdefault("status", "Submitted")
                    if grade.marks_obtained != None:
                        _submission_status["status"] = "Graded"
                else:
                    _submission_status.setdefault("status", "Unsubmitted")
            except:
                # ! this condition wont be reached as when assignment is deleted grades associated with that assignments are deleted as well.
                _submission_status.setdefault("status", None)
            submission_status.append(_submission_status)
        response.setdefault("submissionStatus", submission_status)
        return Response(data=response)
    elif request.method == "DELETE":
        try:
            assignment = Assignment.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        try:
            assignment = Assignment.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        assignment.title = request.data.title
        assignment.due = request.data.due
        assignment.weightage = request.data.weightage
        assignment.description = request.data.description


@api_view()
def coordinatorGroupSubmissionDetails(request, assignmentId, teamId):
    response = {}
    team = Team.objects.get(id=teamId)
    assignment = Assignment.objects.get(id=assignmentId)
    weightage = assignment.weightage
    students = Student.objects.filter(team=team)
    student_data = []
    for student in students:
        _student_data = {
            "student_id": student.id,
            "student_roll_number": student.roll_number
        }
        try:
            grade = Grade.objects.filter(student=student).filter(
                assignment=assignment).first()
            _student_data.setdefault(
                "student_marks", grade.marks_obtained)
        except:
            _student_data.setdefault(
                "student_marks", None)
        student_data.append(_student_data)
    leader = Student.objects.get(id=team.leader.id)
    try:
        files = File.objects.filter(assignment_id=assignmentId).filter(
            team=team)
        file_list = []
        for file in files:
            _file = {
                "id": file.id,
                "file_name": file.file.name,
                "file_url": file.file.url
            }
            file_list.append(_file)
    except:
        pass
    response.setdefault("students_data", student_data)
    response.setdefault("file_list", file_list)
    response.setdefault("weightage", weightage)
    return Response(data=response)


@api_view(['POST'])
def coordinatorCreateAssignment(request):
    title = request.data.get('title')
    description = request.data.get('description')
    weightage = int(request.data.get('weightage'))
    posted = request.data.get('posted')
    due = timezone.datetime.fromtimestamp(int(request.data.get('due')))
    coordinator = request.data.get("coordinator")

    data = {
        "title": title,
        "description": description,
        "due": due,
        "posted": posted,
        "weightage": weightage,
        "coordinator": coordinator
    }
    # file handling remaining
    serializer = AssignmentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        assignment = Assignment.objects.get(title=title)
        for student in Student.objects.all():
            Grade.objects.create(
                student=student, guide=None, assignment=assignment)
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def coordinatorSubmissionStatistics(request):
    response = []
    for team in Team.objects.all():
        _team_data_item = {
            "team_id": team.id
        }
        grade_list = []
        try:
            grades = Grade.objects.filter(team=team)
            for grade in grades:
                submission_status = "Not submitted"
                _t_grade = {}
                if grade.turned_in:
                    submission_status = "Submitted"
                    if grade.marks_obtained != None:
                        submission_status = "Graded"
                _t_grade.setdefault("submission_status", submission_status)
                _t_grade.setdefault(
                    "assignment_name", Assignment.objects.get(id=grade.assignment.id).title)
                grade_list.append(_t_grade)
        except:
            pass
        _team_data_item.setdefault("grades", grade_list)
        response.append(_team_data_item)
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['GET'])
def coordinatorGradingStatistics(request):
    response = []
    for student in Student.objects.all():
        student_data = {
            "roll_number": student.roll_number
        }
        grade_list = []
        try:
            grades = Grade.objects.filter(student=student)
            for grade in grades:
                _grade = {
                    "assignment_name": Assignment.objects.get(id=grade.assignment.id).title
                }
                submission_status = "Not Submitted"
                if grade.turned_in:
                    submission_status = "Submitted"
                    if grade.marks_obtained != None:
                        submission_status = int(grade.marks_obtained)
                _grade.setdefault("marks", submission_status)
                grade_list.append(_grade)
        except:
            pass
        student_data.setdefault("grade_list", grade_list)
        response.append(student_data)
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(["GET"])
def coordinatorGroupRequest(request):
    response = {}
    # GET
    group_requests = []
    for group_request in GroupRequest.objects.all():
        _t = {
            "id": group_request.id,
            "action": group_request.action,
            "status": group_request.status,
            "new_leader": group_request.new_leader,
            "old_leader": group_request.old_leader,
            "add_student": group_request.add_student,
            "remove_student": group_request.remove_student,
            "team": group_request.team.id,
            "description": group_request.description,
            "generated": group_request.generated.strftime("%d/%m/%Y, %H:%M:%S"),
            "processed": group_request.processed.strftime("%d/%m/%Y, %H:%M:%S"),
        }
        group_requests.append(_t)
    response.setdefault("group requests", group_requests)
    return Response(data=response)


@api_view(["GET", "PUT"])
def coordinatorGroupRequestManage(request, id, status):
    group_request = GroupRequest.objects.get(id=id)
    action = group_request.action
    if action == "Change Leader":
        if status == "A":
            team = Team.objects.get(id=group_request.team.id)
            team.leader = group_request.new_leader
            team.save()
            group_request.status = "A"
            group_request.save()
        else:
            group_request.status = "R"
            group_request.save()
    elif action == "Add":
        if status == "A":
            student = Student.objects.get(id=group_request.add_student)
            student.team = group_request.team
            student.save()
            group_request.status = "A"
            group_request.save()
        else:
            group_request.status = "R"
            group_request.save()
    else:
        if status == "A":
            student = Student.objects.get(id=group_request.add_student)
            student.team = None
            student.save()
            group_request.status = "A"
            group_request.save()
        else:
            group_request.status = "R"
            group_request.save()
    return Response()


@api_view(["GET", "PUT"])
def coordinatorProjectRequest(request):
    res = {}
    project_requests = ProjectRequest.objects.all()
    project_req_list = []
    for project_request in project_requests:
        _t = {
            "project": project_request.project.id,
            "description": project_request.description,
            "status": project_request.status,
            "id": project_request.id,
            "created": project_request.created.strftime("%d/%m/%Y, %H:%M:%S"),
            "last_modified": project_request.last_modified.strftime("%d/%m/%Y, %H:%M:%S"),
        }
        project_req_list.append(_t)
    res.setdefault("project_requests", project_req_list)
    return Response(data=res, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
def coordinatorProjectRequestManage(request, id, status):
    project_request = ProjectRequest.objects.get(id=id)
    if status == "A":
        project_request.status = "A"
        project_request.save()
    if status == "R":
        project = Project.objects.get(id=project_request.project.id)
        project.delete()
        project_request.delete()
        project_request.save()
    if status == "R":
        project = Project.objects.get(id=project_request.project.id)
        project.delete()
        project_request.delete()
    return Response()
# * GUIDE


@api_view()
def guideDashboard(request):
    response = {}
    _user = Guide.objects.get(user=request.user)
    group_info = []
    for team in Team.objects.filter(guide=_user):
        member_count = len(Student.objects.filter(team=team))
        _t = {
            "id": team.id,
            "leader_name": team.leader.first_name,
            "member_count": member_count,
        }
        try:
            project = Project.objects.get(team=team)
            _t.setdefault("domain", project.domain)
            group_info.append(_t)
        except:
            _t.setdefault("domain", None)
            group_info.append(_t)
    response.setdefault("group_info", group_info)
    return Response(data=response)


@api_view()
def guideAssignmentDetails(request, pk, groupId):
    response = {}
    studentList = []
    for student in Student.objects.filter(team_id=groupId):
        studentData = {
            "student roll number": student.roll_number
        }
        try:
            grade = Grade.objects.get(
                student=student, assignment=Assignment.objects.get(pk=pk))
            studentData.setdefault("grade", grade.marks_obtained)
        except:
            studentData.setdefault("grade", None)
        studentList.append(studentData)
    assignment = Assignment.objects.get(pk=pk)
    assignmentDetails = {
        "title": assignment.title,
        "description": assignment.description,
        "weightage": assignment.weightage,
        "due": assignment.due.strftime("%d/%m/%Y, %H:%M:%S"),
        "posted": assignment.posted.strftime("%d/%m/%Y, %H:%M:%S")
    }
    fileAttachements = File.objects.filter(team=None)
    _attachments = []
    for file in fileAttachements:
        _file = {
            "id": file.id,
            "file_name": file.file.name,
            "file_url": file.file.url
        }
        _attachments.append(_file)
    assignmentDetails.setdefault("attachments", _attachments)
    teamSubmissions = []
    teamFileUploads = File.objects.filter(team_id=groupId)
    for file in teamFileUploads:
        _file = {
            "id": file.id,
            "file_name": file.file.name,
            "file_url": file.file.url
        }
        teamSubmissions.append(_file)
    response.setdefault("student_list", studentList)
    response.setdefault("assignment_details", assignmentDetails)
    response.setdefault("team_submissions", teamSubmissions)
    return Response(data=response)


@api_view(["PUT"])
def guideAssignGrades(request):
    student_grade = request.data.get("student_grade")
    # print(request.data, type(request.data))
    for i in student_grade:
        _g = Grade.objects.filter(student=i.get("student_id")).filter(
            assignment=request.data.get("assignment_id"))[0]
        if (_g.assignment.weightage >= i.get("marks_obtained")) and (i.get("marks_obtained") >= 0):
            _g.marks_obtained = i.get("marks_obtained")
            _g.save()
            # print(_g.marks_obtained)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response()


@api_view(['GET', 'PUT', 'DELETE'])
def guideAssignmentList(request, groupId):
    team = Team.objects.get(id=groupId)
    grades = Grade.objects.filter(student=team.leader)
    response = []
    for grade in grades:
        _assignment = Assignment.objects.get(grade=grade)
        _t = {
            "assignment_id": _assignment.id,
            "assignment_title": _assignment.title,
            "assignment_due": _assignment.due.strftime("%d/%m/%Y, %H:%M:%S"),
            "assignment_posted": _assignment.posted.strftime("%d/%m/%Y, %H:%M:%S"),
            "assignment_weightage": _assignment.weightage,
        }
        if grade.turned_in:
            _t.setdefault("grading_status", "Submitted")
            if grade.marks_obtained != None:
                _t.setdefault("grading_status", "Graded")
        else:
            _t.setdefault("grading_status", "Not Submitted")
        response.append(_t)
    return Response(data=response)


@api_view(['GET', 'PUT'])
def guideDetailsForm(request):
    if request.method == "GET":
        guide = Guide.objects.all()[0]
        # print(request.user)
        # guide = Guide.objects.get(id=request.user.id)
        response = {
            "guide_initials": guide.initials,
        }
        preferences = guide.preferences.all()
        _preferences = []
        for preference in preferences:
            _t = {
                "area_of_interest": preference.area_of_interest,
                "thrust_area": preference.thrust_area
            }
            _preferences.append(_t)
        response.setdefault("preferences", _preferences)
        return Response(data=response)
    elif request.method == "PUT":
        # guide = Guide.objects.all()[0]
        guide = Guide.objects.get(id=request.user.id)
        data = request.data
        if len(data["preferences"]) > 4:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for preference in data["preferences"]:
            if not preference["area of interest"] in [i[0] for i in domains]:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not preference["thrust area"] in [i[0] for i in thrust_areas]:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        guide.initials = data["guide initials"]
        guide.preferences.clear()
        guide.save()
        for preference in data["preferences"]:
            _p = Preference.objects.filter(area_of_interest=preference["area of interest"]).filter(
                thrust_area=preference["thrust area"]).first()
            if _p == None:
                _p = Preference.objects.create(
                    area_of_interest=preference["area of interest"], thrust_area=preference["thrust area"])
            guide.preferences.add(_p)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def guideProfile(request):
    guide = Guide.objects.all()[0]
    # request.user
    response = {
        "personal": {
            "name": guide.name,
            "initials": guide.initials,
            "email": guide.email
        }
    }
    group_details = []
    teams = Team.objects.filter(guide=guide)
    for team in teams:
        leader = Student.objects.get(id=team.leader.id)
        _t = {
            "team_id": team.id,
            "leader": leader.name,
        }
        students = Student.objects.filter(team=team)
        member_list = []
        for student in students:
            _s = {
                "student_name": student.name,
                "student_photo": student.photo or None,
                "student_email": student.email,
                "student_roll number": student.roll_number,
                "student_branch": student.branch
            }
            member_list.append(_s)
        project = Project.objects.filter(team=team).first()
        if project != None:
            project_details = {
                "project_title": project.title,
                "project_description": project.description,
                "project_domain": project.domain,
                "project_category": project.category,
                "project_explanatory field": project.explanatory_field,
            }
        else:
            project_details = {}
        _t.setdefault("member_list", member_list)
        _t.setdefault("project", project_details)
        group_details.append(_t)
    response.setdefault("group_details", group_details)
    return Response(data=response)
# * STUDENT
# * ASSISTANT
# * AUTHENTICATION AND MISCELLANEOUS


""" change profile picture and password """


@ api_view()
def whoAmI(request):
    try:
        userType = request.user.groups.all()[0].name.lower()
        return Response(data=userType, status=status.HTTP_200_OK)
    except:
        return Response(data=None, status=status.HTTP_200_OK)


@ api_view()
def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@ api_view(['POST'])
@ permission_classes([permissions.AllowAny])
def signIn(request):
    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse()
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
@ permission_classes([permissions.AllowAny])
def signUp(request):
    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        roll_number = request.data.get("roll_number")
        branch = request.data.get("branch")
        if branch == "Information Technology":
            branch = "IT"
        elif branch == "Computer Science":
            branch = "CS"
        elif branch == "Mechanical":
            branch = "MECH"
        elif branch == "Electronics":
            branch = "ETRX"
        elif branch == "Electronics and Telecommunication":
            branch = "EXTC"
        data = {
            "name": " ".join(name.split()).title(),
            "email": email,
            "password": password,
            "branch": branch,
            "roll_number": roll_number,
            "photo": None,
            "is_staff": False,
            "is_active": True
        }
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def guideSignUp(request):
    if request.method == 'POST':
        if request.user.has_perm('api.add_guide'):
            email = request.data.get("email")
            password = request.data.get("password")
            name = request.data.get("name")
            # initials = request.data.get("initials")
            branch = request.data.get("branch")
            if branch == "Information Technology":
                branch = "IT"
            elif branch == "Computer Science":
                branch = "CS"
            elif branch == "Mechanical":
                branch = "MECH"
            elif branch == "Electronics":
                branch = "ETRX"
            elif branch == "Electronics and Telecommunication":
                branch = "EXTC"
            print(request.data)
            data = {
                "name": " ".join(name.split()).title(),
                "email": email,
                "password": password,
                "branch": branch,
                "initials": None,
                "photo": None,
                "is_staff": False,
                "is_active": True
            }

            serializer = GuideSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
