from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .ML_Models.yolo_detections import yolo_detection
from .ML_Models.summarisings import summarizer
from .ML_Models.SemanticSegmentations import run
from .ML_Models.objectclassification import predict_image
from .ML_Models.music_convertor import music_conversion
from .ML_Models.stock_prediction import predict_stock_prices
from .ML_Models.paraphrasing import get_paraphrased_sentences
from .ML_Models.chatGPT import get_completion_from_messages
from .form import UploadImageForm
from django.urls import reverse


def Index(request):
    return render(request, 'index.html')


class CustomObjectDetection(View):
    def get(self, request, *args, **kwargs):  
        return render(request,'models_view/custom-object-detection.html')
    
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('upload_image')
        image_obj = ImageProcessing.objects.create(
            image = image
        )
        user_image = "test.jpg"
        image_path = image_obj.image.path
        result= yolo_detection(image_path,user_image)
        if result:
            count,responded_image = result
            return render(request,'models_view/custom-object-detection.html',{'count':count,"image":image_obj,"custom_object_detection":responded_image})
        return render(request,'models_view/custom-object-detection.html',{"image":image_obj})


class Summarising(View):
    def get(self, request, *args, **kwargs):        
        return render(request,'models_view/summarising.html')
    
    def post(self, request, *args, **kwargs):
        raw_text = request.POST.get('user_input')
        result= summarizer(raw_text)
        print(result,"resultresult")

        (summary, t1, raw_text_length,summary_len) = result
     
        return render(request,'models_view/summarising.html',{'summary':summary,"raw_text":raw_text,"summary_len":summary_len,"raw_text_length":raw_text_length})



class SemanticSegmentation(View):
    def get(self, request, *args, **kwargs): 
       
        return render(request,'models_view/semantic-segmentation.html')
    
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('upload_image')
        image_obj = ImageProcessing.objects.create(
            image = image
        )
        image_paths = run(source=image_obj.image.path)
        return render(request,'models_view/semantic-segmentation.html',{"image_path":image_obj,"image_paths":image_paths})



class ObjectClassification(View):
    
    def get(self, request, *args, **kwargs): 
       
        return render(request,'models_view/object-classification.html')
    
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('upload_image')
        image_obj = ImageProcessing.objects.create(
            image = image
        )
        label_name = predict_image(image_obj.image.path)

        return render(request,'models_view/object-classification.html',{"label_name":label_name,"image_obj":image_obj})



class MusicGenerationn(View):
    '''
    This class is used to convert the music ulploded by user.
    Music format midi.
    '''
    def get(self, request, *args, **kwargs): 
              
        return render(request,'models_view/music-generation.html')
    
    def post(self, request, *args, **kwargs):
        music = request.FILES.get('mid_music')        
        music_obj = MusicGeneration.objects.create(
            music = music
        )
        music = music_conversion(music_obj.music.path)
        split_path = music.split('static/')
        audio_path = str(split_path[1])

        return render(request,'models_view/music-generation.html',{"music":audio_path,"original_sound":music_obj})



class StockPredictions(View):
  
    def get(self, request, *args, **kwargs): 

        return render(request,'models_view/stock-prediction.html')
    
    def post(self, request, *args, **kwargs):
        stock_file = request.FILES.get('csv_upload')        
        upload_object = StockPrediction.objects.create(
            stock_file = stock_file
        )
        path = upload_object.stock_file.path
        plot_image_name = "graph.png"
        predicted_result = predict_stock_prices(path,plot_image_name, n_periods=30)
        return render(request,'models_view/stock-prediction.html',{"predicted_result":predicted_result,"resulted_image":plot_image_name})


class Paraphrasing(View):
  
    def get(self, request, *args, **kwargs): 

        return render(request,'models_view/paraphrasing.html')
    
    def post(self, request, *args, **kwargs):
        senetence = request.POST.get('user_input') 
        resulted_sentence=get_paraphrased_sentences(senetence)
        print(resulted_sentence,">>>>>>>>>>>>>")
        return render(request,'models_view/paraphrasing.html',{"resulted_sentence":resulted_sentence,"raw_text":senetence})


class ChatGPT(View):
  
    def get(self, request, *args, **kwargs): 
            
        return render(request,'models_view/chatgpt.html')
    
    def post(self, request, *args, **kwargs):
     
        message = request.POST.get('message')
        response=get_completion_from_messages(message)
        return redirect(reverse('chat_gpt') + '?response='+response)






