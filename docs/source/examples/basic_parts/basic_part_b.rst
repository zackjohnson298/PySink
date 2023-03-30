.. _basic-part-b:

Part B - Defining a Custom AsyncWorker
======================================

In :ref:`Part A<basic-part-a>`, we saw a default :class:`~PySink.AsyncWorker` in action. However, the whole point of
PySink is to help you implement *your own* workers, so let's see how that works.

To create a custom :class:`~PySink.AsyncWorker`, create a new class that inherits from :class:`~PySink.AsyncWorker`
and override the :meth:`~PySink.AsyncWorker.run` method to implement your long-running task. This task can be anything
you like, but in this example we will keep it simple. This worker will take perform a similar task to
:class:`AsyncWorker's<PySink.AsyncWorker>` default behavior, but this time you will be able to specify the number
of cycles and how long each cycle takes.

First, create a class called CustomAsyncWorker that inherits from :class:`~PySink.AsyncWorker`. Any values that the
CustomAsyncWorker needs should be passed in via it's __init__() method and stored as attributes. Within this class,
override the :meth:`~PySink.AsyncWorker.run` method to implement the new task, and any result values can be passed in
to the :meth:`~PySink.AsyncWorker.complete` method as keyword arguments (more on this in :ref:`Part C<basic-part-c>`):

..  code-block:: python
    :linenos:

    # Define the custom worker, inheriting from AsyncWorker
    class CustomAsyncWorker(AsyncWorker):
        # Any values needed in self.run are passed in to __init__
        def __init__(self, delay_seconds: int, cycles: int):
            super(CustomAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles

        # Override AsyncWorker's .run() method
        def run(self):
            self.emit_start()   # This can be called to signal the start of the task
            progress = 5
            self.update_progress(progress, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / self.cycles
                self.update_progress(progress, f'Progress message #{ii + 1}')

            # Result values can be passed to self.complete() as kwargs.
            self.complete(custom_result_1='result 1', custom_result_2='result 2')


Let's take a closer look at the :meth:`~PySink.AsyncWorker.run` method. On line 11, the
:meth:`~PySink.AsyncWorker.emit_start` method is called to signal the start of the worker's task (this is not necessary,
however it can be useful if there are a lot of workers running :ref:`simultaneously<example-3>`). In lines 12-17 the
task is actually implemented. Finally, in line 20 the :meth:`~PySink.AsyncWorker.complete` method is called. If your
task ends up having any result values (image data, calculation results, etc.) the simple way to emit those values is to
pass them into the :meth:`~PySink.AsyncWorker.complete` method as keyword arguments. The
:meth:`~PySink.AsyncWorker.complete` method will pack those results into the :attr:`~PySink.AsyncWorkerResults.results_dict`
attribute that gets emitted by the :attr:`~PySink.AsyncWorkerSignals.finished` signal. To access this data, pull it
from :class:`AsyncWorkerResults'<PySink.AsyncWorkerResults>` :attr:`~PySink.AsyncWorkerResults.results_dict` attribute
within the completion callback like this:

..  code-block:: python
    :linenos:

    # Function to be called when the worker is finished
    def completion_callback(results: AsyncWorkerResults):
        print(f'\nWorker Complete!')
        print(f'\tErrors: {results.errors}')
        print(f'\tWarnings: {results.warnings}')
        print(f'\tResult 1: {results.results_dict.get("custom_result_1")}')
        print(f'\tResult 2: {results.results_dict.get("custom_result_2")}')
        sys.exit()  # Exit the App event loop

The keys of the :attr:`~PySink.AsyncWorkerResults.results_dict` are the keywords that were passed to
:meth:`~PySink.AsyncWorker.complete`. (In :ref:`Part C<basic-part-c>`, you will see how these can be passed as attributes
of the results object instead).

And that's it. All of the other callback methods stay the same as :ref:`Part A<basic-part-a>`, so here's the full script:

..  code-block:: python
    :linenos:

    from PySide6.QtWidgets import QApplication
    from PySink import AsyncManager, AsyncWorker, AsyncWorkerProgress, AsyncWorkerResults
    import sys
    import time


    # Define the custom worker, inheriting from AsyncWorker
    class CustomAsyncWorker(AsyncWorker):
        # Any values needed in self.run are passed in to __init__
        def __init__(self, delay_seconds: int, cycles: int):
            super(CustomAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles

        # Override AsyncWorker's .run() method
        def run(self):
            self.emit_start()   # This can be called to signal the start of the task
            progress = 5
            self.update_progress(progress, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / self.cycles
                self.update_progress(progress, f'Progress message #{ii + 1}')

            # Result values can be passed to self.complete() as kwargs.
            self.complete(custom_result_1='result 1', custom_result_2='result 2')


    # Function to be called whenever a worker's task has started
    def worker_started_callback(worker_id: str):
        print(f'Worker with id {worker_id} has started its task\n')


    # Function to be called whenever progress is updated
    def progress_callback(progress: AsyncWorkerProgress):
        print(f'Progress Received, value: {progress.value}, message: {progress.message}')


    # Function to be called when the worker is finished
    def completion_callback(results: AsyncWorkerResults):
        print(f'\nWorker Complete!')
        print(f'\tErrors: {results.errors}')
        print(f'\tWarnings: {results.warnings}')
        print(f'\tResult 1: {results.results_dict.get("custom_result_1")}')
        print(f'\tResult 2: {results.results_dict.get("custom_result_2")}')
        sys.exit()  # Exit the App event loop


    def run_main():
        app = QApplication()
        #   Create the Async Manager
        manager = AsyncManager()
        #   Create the Worker and pass in the necessary values
        worker = CustomAsyncWorker(delay_seconds=1, cycles=3)
        #   Connect the Worker's signals to their callbacks
        worker.signals.started.connect(worker_started_callback)
        worker.signals.progress.connect(progress_callback)
        worker.signals.finished.connect(completion_callback)
        #   Start the Worker and App event loop
        manager.start_worker(worker)
        app.exec()


    run_main()


Running this script gives the following output in the terminal:

..  code-block:: console
    :linenos:

    Worker with id 8597cc8b-043d-4d4d-a252-f92773dbba7b has started its task

    Progress Received, value: 5, message: Starting Task
    Progress Received, value: 35.0, message: Progress message #1
    Progress Received, value: 65.0, message: Progress message #2
    Progress Received, value: 95.0, message: Progress message #3

    Worker Complete!
        Errors: []
        Warnings: []
        Result 1: result 1
        Result 2: result 2


