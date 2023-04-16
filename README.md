# PySink

Created by Zack Johnson

## Under construction, not yet ready for use!!

Full documentation can be found at https://pysink.readthedocs.io

PySink is an extension of the PySide6 Qt Framework that simplifies the implementation
of Asynchronous tasks in Desktop Applications. It contains several
helper classes and widgets that enable you to build powerful and professional
desktop applications without worrying about managing threads or freezing 
UI with long-running tasks. PySink's implementation suggests an MVC 
architecture for your application, but should perform well in other architectures
such as MVVM.

## Installation
The latest build of PySink is hosted on PyPi, and can be installed into your environment via the pip command:

```commandline
pip install pysink
```

## Basic Overview
PySink is based on the concept of Workers and Managers. Workers are custom objects that 
perform long-running tasks. They inherit from the provided *AsyncWorker* class and 
override the *AsyncWorker.run()* method to perform the tasks, emitting progress values and 
optional status messages along the way. These workers are managed by a generalized object called the
*AsyncManager*. The AsyncManager is an object that manages all the threading and handles the termination/cancellation 
of said threads and workers when necessary. 

In an MVC architecture, the Controller would store a new AsyncManager as an attribute during initialization. To start
and asynchronous task, the Controller would instantiate a custom AsyncWorker, connect to its signals (progress, 
completion, etc.), then pass the worker to the AsyncManager's *start_worker()* method. 

## Getting Started
Please vist https://pysink.readthedocs.io for in-depth walkthroughs on how to use PySink in your applications.
