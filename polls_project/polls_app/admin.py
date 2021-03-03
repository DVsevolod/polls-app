from django.contrib import admin

from .models import *


admin.site.register(UserModel)
admin.site.register(PollModel)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)
