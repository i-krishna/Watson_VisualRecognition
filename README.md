# Watson-Visual-Recognition (WVR) Summary



# Bigger picture

Watson has various services that you weave together to solve the user’s problem. Watson does not just know. It has to be taught. Cognitive systems are not programmed, they are trained. There are [five key Watson patterns](/Screenshots/Watson%20Patterns.png): [Engagement, Discovery, Decision, Policy, and Exploration](/Watson%20patterns%20description.pdf)

<p float="left">
   
   <img src="/Screenshots/Cognitive%20computing-3%20divisions.png" />   
    
  <img src="/Screenshots/Watson%20api%20services%20overview.png" />  
  
   <img src="/Screenshots/Watson%20api%20learning%20model.png" /> 

</p>

# Discover - Vision - Visual Recognition 

Let us look into Watson API learning model - [visual recognition](https://www.ibm.com/watson/services/visual-recognition/) further. WVR has **6 basic models** as shown below

![alt text](/WVR-Models-IBMCloud.png)

# Working of various models
 
Consider a tyre image from the demo [here](https://www.ibm.com/watson/services/visual-recognition/demo/#demo) and go through the classification results as shown below

![alt text](/Working-demo-images-classified.png)

## From [curl](https://curl.haxx.se/) or [swagger](https://swagger.io/) or [postman](https://www.getpostman.com/), submit the images as input from ![img_db](/master/img_db)

Get the API access key credentials of the visual recognition service from your IBM cloud account

### Image on left as input  - Json response on right as output 

## WVR Food model

<p float="left">
  <img src="/img_db/fruitbowl.jpg" width="400" />
  <img src="/img_responses/Food.png" width="400" /> 

</p>

## WVR Face model

<p float="left">
  <img src="/img_db/ginni.jpg" width="400" />
  <img src="/img_responses/Ginni.png" width="400" /> 

</p>

### WVR General model
<p float="left">
  <img src="/img_db/chip.jpg" width="400" />
  <img src="/object.png" width="400" /> 

</p>

<p float="left">
  <img src="/General_model.png" /> 
</p>


# WVR Custom model

We created a custom model that classifies dogs. We supplied a negative sample of cats. The JSON response below shows the training phase of the custom classifier dogs_2025763446

<p float="left">
  <img src="/Screenshots/Custom%20dog%20classifier.jpg" /> 
</p>

Once the training is done, make a get request to see the status ready before passing test samples. 

<p float="left">
  <img src="/Screenshots/Training%20done%20.png" /> 
</p>

Below you find one positive (dog golden retreiver ) and one negative (apples) JSON responses when passed to custom classifier dogs_2025763446

<p float="left">
  <img src="/Screenshots/Test_golden_retreiver.png" width="400" />
  <img src="/Screenshots/Test_apples.png" width="400" /> 
</p>

[Documentation](https://cloud.ibm.com/docs/services/visual-recognition/customizing.html#customizing-size) specifies the WVR custom model limitations.

# Issues / Limitations

**Assertion 1**: [Documentation](https://cloud.ibm.com/apidocs/visual-recognition
) says that form parameter images_file can be a single file or a zip file with max 20 images. The maximum size of such a zip file is 100MB. Not ideal for cases of real-time video classification that takes more than 20 fps. 

![alt text](/Screenshots/form%20parameter%20-%20image_file.png)


**Assertion 2**: When using the general model, it does not show all the objects like a apple within an image in JSON response. 

```shell
curl -X POST -u "apikey:m2SyTztvn6aR1PFI0i7Lyf9er4Jh8fANO6E0btcYWrAL" --form "images_file=@/Users/krishna/Desktop/img_db/fruitbowl.jpg" "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19"
```

<p float="left">
  <img src="/img_db/fruitbowl.jpg" width="400" />
  <img src="/img_responses/Food.png" width="400" /> 

</p>

**Assertion 3**: As assertion 2 uses the general model and all objects within food image are not shown, We passed the classifier id as food now. Even then, not all fruits like oranges are classified with a default threshold as shown below. 

**Test with image sample of fruitbowl.jpg**
```shell
curl -X POST -u "apikey:m2SyTztvn6aR1PFI0i7Lyf9er4Jh8fANO6E0btcYWrAL" --form "images_file=@/Users/krishna/Desktop/img_db/fruitbowl.jpg"  -F "classifier_ids=food" "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19"
```

**Threshold of 0 and 0.5(default)**

<p float="left">
  <img src="/img_responses/Thresholds%20zero%20and%20point%205%20for%20food%20classifier.png" width="400" />

</p>

 **Threshold of 0.6, 0.9**
 
 <p float="left">
  <img src="/img_responses/Threshold%20point%208%20and%20point%209%20food%20classifier.png" width="400" />

</p>
 
**Note:** 

- In fruitbowl.jpg (640 × 426 pixel image resolution), when the threshold is above 0.6, apples or banana are not recognized. The default threshold of 0.5 and anything below 0.5 recognized the fruits apple and banana. Adjusting the threshold might increase the quality of predictions but sometimes the objects are gone out of predictions completely. 

**Test with another image sample of Apples_green_red.jpg**

**Default threshold of 0.5**

<p float="left">
 <img src="/img_responses/default%20threshold%20response_Apples_red_green.png" width="400" /> 
</p>

 **Threshold of 0.7, 0.8**
  
<p float="left">
 <img src="/img_responses/Apples_green_red_rsponse_threshols_07_08.png" width="400" /> 
</p>

# **Note:** 

- In Apples_green_red.jpg (342 × 147 pixel image resolution), none of the objects are recognized when the threshold is increased to 0.8. The image resolution of Apples_green_red.jpg is less than that of the above fruitbowl.jpg (640 × 426 pixel image resolution). 
- Instead of changing the threshold to improve the prediction results, we can fix the threshold to 0.5 (default) and submit images with higher resolution for better predictions results. 
- On a broader note, Threshold is directly proportional to the image quality. Higher the picture quality, objects in the picture can be recognized with higher thresholds. Lesser the picture quality, objects in the picture can be recognized only with lesser thresholds. Some tips on choosing the right threshold value for custom classifiers is shown here: [3rd point in Questions]( https://cloud.ibm.com/docs/services/visual-recognition/customizing.html#customizing-faq)
- Also, [Documentation](https://www.ibm.com/blogs/bluemix/2016/10/watson-visual-recognition-training-best-practices/) mentions that images in training and testing sets should resemble each other. Significant visual differences between training and testing groups will result in poor performance results. There are number of additional factors that will impact the quality of your training beyond the resolution of your images. Lighting, angle, focus, color, shape, distance from subject, and presence of other objects in the image will all impact your training. 
- So far, we tested images with pre-trained classifiers or built-in models where we have no control of trained images.   Custom classifiers have much more control on training & test samples to improve the accuracy levels taking in view of aforementioned points.

**Assertion 3**: Faces are detected in food image for the following command below

```shell
curl -X POST -u "apikey:m2SyTztvn6aR1PFI0i7Lyf9er4Jh8fANO6E0btcYWrAL" --form "images_file=@/Users/krishna/Desktop/img_db/fruitbowl.jpg" "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2018-03-19"
```
<p float="left">
 <img src="/img_db/fruitbowl.jpg" width="400" />

<img src="/img_responses/Faces_detected_fruitbowl_response.png" width="400" /> 
</p>

**Assertion 4**: [Documentation](https://cloud.ibm.com/apidocs/visual-recognition
) says that for a given image, age and gender is classified using general model. However, JSON responses for the curl requests using a general model for above Ginni / Trump images does not shown such classification.

**Assertion 5**: General model does not detect multiple faces within a single image as shown below

**General model response for face detection**

<p float="left">

<img src="/img_db/6_faces_in_single_image.jpg" width="400" />

<img src="/img_responses/6_faces_in_image.png" width="400" />
/p>

For such classification to happen, we have to explicitly pass the parameter detect_faces while submitting the image through curl request as shown below. Means, we have to know whether we are passing the face/object/food image before passing image.

**detect_faces parameter passed in curl request**

```shell
curl -X POST -u "apikey:m2SyTztvn6aR1PFI0i7Lyf9er4Jh8fANO6E0btcYWrAL" --form "images_file=@/Users/krishna/Desktop/img_db/6_faces_in_single_image.jpg.jpg" "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2018-03-19"
```

<p float="left">

 <img src="/img_responses/6_faces_in_single_image.png" width="400" />

</p>

**Assertion 6**: Delayed responses in cases of increased image files. 1st image below takes <1sec. While the next 2 zipped folders with 5 and 22 images take 2.5 and more than 8 seconds. 

**Time = < 1sec for 1 file**
 <img src="/img_responses/single_image_response_time.png">

**Time = 2.5sec for 5 files**
 <img src="/img_responses/5_files_Zipped_response_time.png">

**Time = >8 sec for 22 files**
 <img src="/Screenshots/22_files_zipped.png">
 
**Detailed JSON response for 20 files** - Note that only [20 files](/json-response-22-files.json) are processed as specified in the documentation 

**Assertion 7**: We can observe from above-detailed JSON response that, images that have faces does not contain any information about their age/gender within the JSON response. Also, we passed images with combinations like images with face and food, food and text, food and hands. In such cases, the JSON responses are restricted to only one particular category. 

**Assertion 8**: Current UI interface does not show any train button to upload images in custom model creation. Hence we trained our custom models by passing training datasets through curl request. Check below demo for further details.


# Relevant studies

- After reviewing lighthouse and other IBM internal assets, we found a close resemblance between **Watson Natural Language Classifier (NLC)** and **WVR Text model**. WLC is used for Text Classification https://www.ibm.com/watson/services/natural-language-classifier/. WVR Text model is used to identify the natural language in the uploaded image

- The **Watson Personality Insights (Waston PI)** https://w3-03.ibm.com/services/lighthouse/documents/61268 uses linguistic analytics to extract a spectrum of cognitive and social characteristics from the text data that a person generates through blogs, tweets, forum posts, and more. 

- The common point with above 2 APIs and WVR Text model is related to identifying and classifying text. There were times when APIs like Alchemy vision   https://www.ibm.com/blogs/watson/2016/05/visual-recognition-update/ deprecated to visual recognition and Q & A service deprecated to Engagement - Conversation due to their similarities in functioning. However, such merges in above 2 API cases to visual recognition or vice versa needs further investigation. 

- Projects that are built with Watson APIs in combination with visual recognition, NLC, etc or standalone are specified below: (Study in progress...)

    - Watson text classification -  https://developer.ibm.com/patterns/extend-watson-text-classification/

    - Ticket categorization - https://developer.ibm.com/patterns/watson-studio-nlc-technical-support-ticket-categorization/
 
    - Customer communications Insights analyzer -  https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/Customer%20Communication%20Insights%20Analyzer
 
    - Text and email analyzer - https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/Text%20and%20email%20analyzer
    
    - Watson health depression pres screening - https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/Watson%20Health%20DEP%20Depression%20Pre-Screening

    - Optimized dictionary of German street names - https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/Optimized%20Dictionary%20of%20Street%20Names%20in%20German

    - Troll patrol - https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/Troll%20Patrol 

    - GDPR Email Triage - https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/GDPR%20Email%20Triage

    - Email routing accelerator - https://apps.na.collabserv.com/wikis/home?lang=en-us#!/wiki/Wfdeebd09058d_481a_945f_bf89b0d58d08/page/Email%20Routing%20Accelerator

# Onpremise offering 

- We can [run IBM Watson services on any cloud](https://newsroom.ibm.com/2019-02-12-IBM-Watson-Now-Available-Anywhere). As visual recognition service is a part of Watson, we can host WVR onpremise.  

- Through the integration with [IBM Cloud Private for Data (ICP for Data)](https://www.youtube.com/watch?time_continue=5&v=wOsg3aIaDxM), Watson and Watson OpenScale can now be run any environment – on premises, or on any private, public or hybrid multi cloud – enabling businesses to apply AI to data wherever it is hosted. 

- [ICP for data purchase details](https://cloud.ibm.com/docs/services/vmwaresolutions/services?topic=vmware-solutions-icp_overview#technical-specifications-for-ibm-cloud-private-hosted)

- [Transform the Enterprise with IBM Cloud Private on OpenShift](https://www.youtube.com/watch?v=XGlBO0-lZck)

# References 
- https://sourcedexter.com/ibm-visual-recognition-api-part-1/
- [WVR as a service in IBM Cloud](https://www.ibm.com/watson/services/visual-recognition/)
- [Visual recognition overview - Data platform](https://dataplatform.cloud.ibm.com/docs/content/analyze-data/visual-recognition-overview.html)
- [Visual recognition overview](https://cloud.ibm.com/apidocs/visual-recognition)
- [Visual recognition getting-started-tutorial](https://cloud.ibm.com/docs/services/visual-recognition/getting-started.html#getting-started-tutorial)
- [Visual recognition Bluemix docs](https://github.com/IBM-Bluemix-Docs/visual-recognition)
- [Visual recognition - customizing guidelines](https://cloud.ibm.com/docs/services/visual-recognition/customizing.html#customizing-guidelines-training)
- [Cognitive analytics community material](https://w3-connections.ibm.com/communities/service/html/communityview?communityUuid=45a3a33e-0cf5-4bb9-86bd-81ed23c7b861#fullpageWidgetId=W350fc0803e00_4321_888d_5cc460c8fbe1)
- [IBM Cloud Private on Data - tl;dr](https://community.ibm.com/community/user/icpfordata/viewdocument/video-ibm-cloud-private-for-data-h-1?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments)
- [IBM Cloud Private on Data - In detail](https://github.ibm.com/Krishna-Damarla1/Watson-Visual-Recognition/blob/master/ICP%20for%20Data.pdf)
- [Visual recognition Blog](https://www.ibm.com/blogs/bluemix/author/kgongus-ibm-com/)
- [Visual recognition - custom model](https://dataplatform.cloud.ibm.com/docs/content/analyze-data/visual-recognition-create-model.html)
- [Visual recognition - custom model video1](https://www.youtube.com/watch?v=o8xxZcmuc2Q)
- [Visual recognition - custom model video2](https://www.youtube.com/watch?time_continue=14&v=3ArhBQ_QxkM)
- [Visual recognition - Redbook](http://www.redbooks.ibm.com/redbooks/pdfs/sg248393.pdf)

