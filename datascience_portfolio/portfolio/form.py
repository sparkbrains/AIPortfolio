from django.forms import ModelForm
from portfolio.models import ImageProcessing

class UploadImageForm(ModelForm):
    
    class Meta:
        model = ImageProcessing
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super(UploadImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True 
        
uplaodImageForm = UploadImageForm()
