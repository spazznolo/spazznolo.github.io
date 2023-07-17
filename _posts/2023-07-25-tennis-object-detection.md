---
layout: post
title:  "Tennis: Summary of Object Detection"
date:   2023-07-25 12:00:00 -0400
---
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DGRHZS5DNM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DGRHZS5DNM');
</script>
</head>
<h2>A summary of the object detection model</h2>
<p>
I stepped away from the first iteration of this project last year when I realized I was going to have to annotate thousands of images to create a robust player/ball detection model. In the next few months, I'll design and build such a modelling framework. This post outlines the methods and services which will be used for the framework.
</p>
<p>
<h5>YOLOv5</h5>
The current object detection model is <a href="https://pytorch.org/hub/ultralytics_yolov5/">YOLOv5</a>. Recall some of the results from the <a href="https://app.roboflow.com/tennistracker-dogbm/tennis-tracker-duufq/deploy/15">latest</a> model iteration were:
overall:      91.0% P, 85.5% R, 85.8 mAP50
front-player: 99.5% P, 99.6% R, 99.5 mAP50
back-player:  99.5% P, 99.4% R, 99.3 mAP50
tennis-ball:  74.1% P, 57.0% R, 58.7 mAP50
</p>
<p>
<h5>Video Example</h5>
For a short example of the inference, click <a href = "https://www.youtube.com/watch?v=DwdfFsjQgFg">here.</a>
</p>
<p>
<h5>When does the model tend to <em>not classify</em> an object?</h5>
<p>
For players, xxx.
</p>
<p>
For tennis balls, xxx.
</p>
<p>
<h5>When does the model tend to <em>mis-classify</em> an object?</h5>
<p>
For players, xxx.
</p>
<p>
For tennis balls, xxx.
</p>
<p>
<h5>Post-Processing of Tennis Players</h5>
The model performs strongly, so a simple imputation strategy using interpolation has worked so far. Interpolation is done through Python's xxx module. Here are the specs:
  - window:
  - function: mean
  - na length: 
</p>
<p>
<h5>Post-Processing of Tennis Ball</h5>
to be continued
</p>

