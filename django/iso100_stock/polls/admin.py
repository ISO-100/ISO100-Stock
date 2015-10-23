from django.contrib import admin

# Register your models here.
from .models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    
#admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice, ChoiceInline)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)