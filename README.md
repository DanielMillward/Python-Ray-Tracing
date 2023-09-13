# RayTracing
This is a python implementation of the code found in [Ray Tracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html). This was written before any formal study of programming on my part. Hopefully that excuses the (very) messy code.

 Ray Tracing in Python
 helloray.py is the main function. 
 Current features:
  - Can render multiples frames (change the frames attribute to set it)
  - outputs in ppm (convert to jpg in an external program)
  - adjustable samples per pixel and max depth
  - can move the objects in the scene between frames to allow for smooth motion
  - make max depth map (uncomment all the lines in the main function, outputs to raytracenum.ppm)
  
  Render time for default scene - 3 hours for an 800x800 image on a pentium processor, 50 spp, 25 max depth
  
