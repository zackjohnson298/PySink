# PySink

Created by Zack Johnson

## Under construction, not yet ready for use!!

Full documentation can be found at https://pysink.readthedocs.io

PySink is an extension of the PySide6 Qt Framework that simplifies the implementation
of Asynchronous tasks in Desktop Applications. It contains several
helper Widgets and Classes that enable you to build powerful and professional
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
*AsyncManager*. 

The Manager is an object that manages all the workers/threading and handles the termination/cancellation 
of said threads and workers when necessary. The Manager can also pass along the signals emitted by 
the worker (you can also connect to the worker's signals directly, see example 5 below).



## Getting Started

Please vist https://pysink.readthedocs.io for in-depth walk-throughs on how to use PySink in you applications.
