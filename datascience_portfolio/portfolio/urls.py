
from django.urls import path
from .views import CustomObjectDetection,Summarising,SemanticSegmentation,ObjectClassification,MusicGenerationn,StockPredictions,Paraphrasing,ChatGPT,MCQ,MCQSubmit
# from .views import CustomObjectDetection,ObjectClassification


urlpatterns = [
    path('', CustomObjectDetection.as_view(), name='custom_object_detection'),
    path('summarising/', Summarising.as_view(), name='summarising'),
    path('semantic-segmentation/', SemanticSegmentation.as_view(), name='semantic_segmentation'),
    path('object-classification/', ObjectClassification.as_view(), name='object_classification'),
    path('music-generation/', MusicGenerationn.as_view(), name='music_generation'),
    path('stock-prediction/', StockPredictions.as_view(), name='stock_prediction'),
    path('paraphrasing/', Paraphrasing.as_view(), name='paraphrasing'),
    path('chat-gpt/', ChatGPT.as_view(), name='chat_gpt'),
    path('mcq/', MCQ.as_view(), name='mcq'),
    path('mcq_submit/', MCQSubmit.as_view(), name='mcq_submit'),


]
