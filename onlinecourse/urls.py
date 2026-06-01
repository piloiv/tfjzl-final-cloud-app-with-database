from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='', view=views.CourseListView.as_view(), name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    # ex: /onlinecourse/5/
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    # ex: /enroll/5/
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # <HINT> Create a route for submit view
    path('<int:course_id>/submit/', views.submit, name="submit"),

    # <HINT> Create a route for show_exam_result view
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name="exam_result"),
    
	def show_exam_result(request, course_id, submission_id):
		context = {}
		course = get_object_or_404(Course, pk=course_id)
		submission = Submission.objects.get(id=submission_id)
		choices = submission.choices.all()

		total_score = 0
		questions = course.question_set.all()  # Assuming course has related questions

		for question in questions:
			correct_choices = question.choice_set.filter(is_correct=True)  # Get all correct choices for the question
			selected_choices = choices.filter(question=question)  # Get the user's selected choices for the question

			# Check if the selected choices are the same as the correct choices
			if set(correct_choices) == set(selected_choices):
				total_score += question.grade  # Add the question's grade only if all correct answers are selected

		context['course'] = course
		context['grade'] = total_score
		context['choices'] = choices

		return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
