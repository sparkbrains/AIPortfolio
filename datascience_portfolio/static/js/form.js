$("#file-upload-form").validate({
    rules:{
        upload_image:{
            required:true,
        },   
    },
    messages:{
        upload_image:{
            required:"Please select your experience",
        },
     
        
    },
});
