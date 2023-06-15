from django.contrib import admin

# Register your models here.
from portfolio.models import Questions,Options



class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["id", "questions", "correct_answer", "get_options"]

    def get_options(self, obj):
        return "\n".join([p.options for p in obj.options.all()])

admin.site.register(Questions, QuestionsAdmin)

class OptionsAdmin(admin.ModelAdmin):
    list_display = ["id", "options"]

   

admin.site.register(Options, OptionsAdmin)
