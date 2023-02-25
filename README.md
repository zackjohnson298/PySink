# PySink

Created by Zack Johnson

<span style="color:red">
Under construction, not ready for use!
</span>

PySink is an extension of the PySide6 Qt Framework that simplifies the implementation
of Asynchronous tasks in your Desktop Applications. It contains several
helper Widgets and Classes that enable you to build powerful and professional
desktop applications without worrying about managing threads or freezing 
UI with long-running tasks. PySink's implementation suggests an MVC 
architecture for your application, but should perform well in other architectures
such as MVVM.

## Getting Started
PySink is based on the concept of Workers and Managers. Workers are custom objects that 
perform your long-running tasks. They inherit from the provided *AsyncWorker* class and 
override the *AsyncWorker.run()* method to perform the tasks, emitting progress values and 
optional status messages along the way. 

These workers are managed by a generalized object called the *AsyncManager*. 
The Manager is an object that manages all the threading, passes along the signals and values 
emitted by the Worker, and handles the cancellation of said threads and workers when necessary.

Let's look at a couple examples to help you get started. Full examples and all source code can be found at https://github.com/zackjohnson298/PySink

### Example 1: Defining and Using a Custom Async Worker
In this first example, we will create a custom AsyncWorker that performs *time.sleep()* 
for a specified duration and number of cycles. To create a new worker, define a class
that inherits from *PySink.AsyncWorker*. Any values needed by the worker should be passed
in via it's *\_\_init\_\_* method: 

```python
from PySink import AsyncWorker


class DemoAsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        super(DemoAsyncWorker, self).__init__()
        # Store the values passed in during initialization
        self.delay_seconds = delay_seconds
        self.cycles = cycles
```
To implement your long-running task, simply override AsyncWorker's *run* method.
This method takes no parameters and returns nothing, it just performs your task. 
Progress/status is emitted by calling the *self.update_progress(progress, message)*
method, and when your task is done you can emit any results via the 
*self.complete(\*\*kwargs)* method:

```python
from PySink import AsyncWorker
import time


class DemoAsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        super(DemoAsyncWorker, self).__init__()
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 0
        progress_increment = 100 / self.cycles
        # Update progress by providing a progress value from 0-10 with an 
        #   optional message
        self.update_progress(0, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += progress_increment
            self.update_progress(progress, f'Progress message #{ii + 1}')
        # Call the self.complete method to end your task, passing any 
        #   results as keyword arguments
        demo_result = 12
        self.complete(demo_result=demo_result)
```
Starting your custom worker is as simple as creating an AsyncManager, tying 
its signals to your callback methods, and passing your custom Worker to its *start_worker(worker)* method. 
*(We also need a QApplication running for the event loop 
to start, which you will already have in your PySide6 Application).* Let's see 
what this looks like in code:

```python
from PySide6.QtWidgets import QApplication
from PySink import AsyncManager

# Function to be called whenever progress is updated
def progress_callback(progress_value: int, message: str):
    print(f'Progress Received, value: {progress_value}, message: {message}')

# Function to be called when the worker is finished
def completion_callback(results: dict):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.get("errors")}')
    print(f'\tWarnings: {results.get("warnings")}')
    print(f'\tResult: {results.get("demo_result")}')


def run_main():
    app = QApplication()
    manager = AsyncManager()
    # Connect the Manager's signals to your callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    # Create your Worker, and pass in the necessary values
    demo_worker = DemoAsyncWorker(1, cycles=3)
    # Start the Worker
    manager.start_worker(demo_worker)
    
    app.exec()

run_main()
```

Let's first take a look at the progress callback. Progress is emitted by the manager's 
*worker_progress_signal* and contains the progress value as well as the optional message.
It should be tied to the callback function that handles progress events. In this example,
the progress callback simply prints out the progress value and the message.
In the next example, we will look at how to tie this to the *ProgressBarWidget* provided 
in the *PySink.Widgets* module.

The completion callback is tied to the manager's *worker_finished_signal*. This signal
emits the results of the worker's task as a dictionary. It is keyed by the keyword arguments
defined when the *self.complete(\*\*kwargs)* method is called within the worker. This
dictionary also contains the worker's *warnings* and *errors*.

Running the code above results in the following being printed to the console:
```commandline
Progress Received, value: 0, message: Starting Task
Progress Received, value: 33, message: Progress message #1
Progress Received, value: 66, message: Progress message #2
Progress Received, value: 100, message: Progress message #3

Worker Complete!
	Errors: []
	Warnings: []
	Result: 12
```
Congratulations! You've just implemented an AsyncWorker that runs a task in a background thread.
Running the task like this has freed up the UI thread, allowing your users to still interact
with your application without freezing the UI. In the next example, we will see how to use the
provided ProgressBarWidget to display this task to users in a simple app


[//]: # ()
[//]: # (```python)

[//]: # (from PySink import AsyncWorker)

[//]: # (import time)

[//]: # ()
[//]: # ()
[//]: # (class DemoAsyncWorker&#40;AsyncWorker&#41;:)

[//]: # (    def __init__&#40;self, delay_seconds: int, cycles=4&#41;:)

[//]: # (        super&#40;DemoAsyncWorker, self&#41;.__init__&#40;&#41;)

[//]: # (        self.delay_seconds = delay_seconds)

[//]: # (        self.cycles = cycles)

[//]: # ()
[//]: # (    def run&#40;self&#41;:)

[//]: # (        progress = 0)

[//]: # (        progress_increment = 100 / self.cycles)

[//]: # (        # Update progress by providing a progress value from 0-10 with an optional message)

[//]: # (        self.update_progress&#40;0, 'Starting Task'&#41;)

[//]: # (        for ii in range&#40;self.cycles&#41;:)

[//]: # (            time.sleep&#40;self.delay_seconds&#41;)

[//]: # (            progress += progress_increment)

[//]: # (            self.update_progress&#40;progress, f'Progress message #{ii + 1}'&#41;)

[//]: # (            # Store any errors/warnings in the provided attributes. They are emitted by default)

[//]: # (            self.warnings.append&#40;f'Demo Warning {ii + 1}'&#41;)

[//]: # (            self.errors.append&#40;f'Demo Error {ii + 1}'&#41;)

[//]: # (        # Call the self.complete method to end your task, passing any results as keyword arguments)

[//]: # (        demo_result = 12)

[//]: # (        self.complete&#40;demo_result=demo_result&#41;)

[//]: # (        )
[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # (When you want to start a long-running task, initialize an AsyncManager and run the worker, passing in references to a completion callback and an optionalal)

[//]: # ()
[//]: # (```python)

[//]: # (from PySink import AsyncWorker)

[//]: # (import time)

[//]: # ()
[//]: # ()
[//]: # (class DemoAsyncWorker&#40;AsyncWorker&#41;:)

[//]: # (    def __init__&#40;self, delay_seconds, cycles=4&#41;:)

[//]: # (        super&#40;DemoAsyncWorker, self&#41;.__init__&#40;&#41;)

[//]: # (        self.delay_seconds = delay_seconds)

[//]: # (        self.cycles = delay_count)

[//]: # ()
[//]: # (    def run&#40;self&#41;:)

[//]: # (        progress = 0)

[//]: # (        progress_increment = 100 / self.count)

[//]: # (        for ii in range&#40;self.count&#41;:)

[//]: # (            self.update_progress&#40;progress, f'Progress message #{ii + 1}'&#41;)

[//]: # (            time.sleep&#40;self.delay_seconds&#41;)

[//]: # (            progress += progress_increment)

[//]: # (        self.update_progress&#40;100, 'Complete'&#41;)

[//]: # (        self.error = 'Demo Error')

[//]: # (        self.complete&#40;error=self.error, value=12&#41;)

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # ([//]: # &#40;Check out: https://www.youtube.com/c/NeuralNine&#41;)