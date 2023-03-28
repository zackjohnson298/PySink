Part A - Starting an AsyncWorker
================================

Let's start by using the :class:`AsyncWorker's<PySink.AsyncWorker>` default task to see the signals it emits and how to receive
those signals by connecting them to callbacks. By default, the :class:`~PySink.AsyncWorker` will perform a demo task of
counting to five with a delay of 1 second between counts. Generally a worker emits three kinds of signals,
a :attr:`~PySink.AsyncWorkerSignals.started` signal, a :attr:`~PySink.AsyncWorkerSignals.progress` signal, and a
:attr:`~PySink.AsyncWorkerSignals.finished` signal (you can also define/emit custom signals, but more on that
:ref:`later<basic-part-d>`).

The :attr:`~PySink.AsyncWorkerSignals.started` signal indicates that a worker has started it's long-running task. It
contains the id of the worker which can be used to differentiate between active workers. Note that to emit this signal,
the worker must call its :meth:`~PySink.AsyncWorker.emit_start` method at the top of :meth:`~PySink.AsyncWorker.run`
(more on overriding the :meth:`~PySink.AsyncWorker.run` method in :ref:`Part B<basic-part-b>`). Below is a callback that will be triggered
on the :attr:`~PySink.AsyncWorkerSignals.started` signal:

..  code-block:: python

    def worker_started_callback(worker_id: str):
        print(f'Worker with id {worker_id} has started its task\n')


The :attr:`~PySink.AsyncWorkerSignals.progress` signal passes along an :class:`~PySink.AsyncWorkerProgress` object
containing a :attr:`progress value<PySink.AsyncWorkerProgress.value>`,
:attr:`status message<PySink.AsyncWorkerProgress.message>`, and the :attr:`worker's id<PySink.AsyncWorkerProgress.id>`.
Here is a simple callback function that will print out the progress of an :class:`~PySink.AsyncWorker`:

..  code-block:: python

    def progress_callback(progress: AsyncWorkerProgress):
        print(f'Progress Received, value: {progress.value}, message: {progress.message}')

The callback receives the progress as a parameter. Within the callback, the progress :attr:`~PySink.AsyncWorkerProgress.value`
and :attr:`~PySink.AsyncWorkerProgress.message` attributes are extracted and printed to the console.

Now let's take a look at the completion callback. This will be connected to the worker's :attr:`~PySink.AsyncWorkerSignals.finished`
signal, and receives the worker's results as an :class:`~PySink.AsyncWorkerResults` object:

..  code-block:: python

    def completion_callback(results: AsyncWorkerResults):
        print(f'\nWorker Complete!')
        print(f'\tWarnings: {results.warnings}')
        print(f'\tErrors: {results.errors}')
        sys.exit()  # Exit the App event loop

The results object contains the worker's warnings and errors (it also contains the results of the worker, those
will be explained in :ref:`Part B<basic-part-b>`). The completion callback prints out the warnings and errors,
then calls sys.exit() to end the App event Loop.

Now that the callbacks are taken care of, let's look at how an :class:`~PySink.AsyncWorker` is started with an
:class:`~PySink.AsyncManager`:

..  code-block:: python
    :linenos:
    :emphasize-lines: 9-11

    def run_main():
        # Create an instance of QApplication. This allows us to start a Qt event loop.
        app = QApplication()
        #   Create the Async Manager
        manager = AsyncManager()
        #   Create the Worker
        worker = AsyncWorker()
        #   Connect the Worker's signals to their callbacks
        worker.signals.started.connect(worker_started_callback)
        worker.signals.progress.connect(progress_callback)
        worker.signals.finished.connect(completion_callback)
        #   Start the Worker
        manager.start_worker(worker)
        #   Start the App Event Loop
        app.exec()

The general logic is as follows:

#. Create an instance of :class:`~PySink.AsyncManager`
#. Create an instance of the worker
#. Connect the worker's signals to their callbacks (line 9-11)
#. Start the worker by passing it to the manager's :meth:`~PySink.AsyncManager.start_worker` method

This logic is wrapped in a QApplication so that it can run within a Qt event loop. Here's what the full python script
looks like:

..  code-block:: python
    :linenos:

    from PySide6.QtWidgets import QApplication
    from PySink import AsyncManager, AsyncWorker
    from PySink import AsyncWorkerProgress, AsyncWorkerResults
    import sys


    # Function to be called whenever a worker's task has started
    def worker_started_callback(worker_id: str):
        print(f'Worker with id {worker_id} has started its task\n')


    # Function to be called whenever progress is updated
    def progress_callback(progress: AsyncWorkerProgress):
        print(f'Progress Received, value: {progress.value}, message: {progress.message}')


    # Function to be called when the worker is finished
    def completion_callback(results: AsyncWorkerResults):
        print(f'\nWorker Complete!')
        print(f'\tWarnings: {results.warnings}')
        print(f'\tErrors: {results.errors}')
        sys.exit()  # Exit the App event loop


    def run_main():
        # Create an instance of QApplication. This allows us to start a Qt event loop.
        app = QApplication()
        #   Create the Async Manager
        manager = AsyncManager()
        #   Create the Worker
        worker = AsyncWorker()
        #   Connect the Worker's signals to their callbacks
        worker.signals.started.connect(worker_started_callback)
        worker.signals.progress.connect(progress_callback)
        worker.signals.finished.connect(completion_callback)
        #   Start the Worker
        manager.start_worker(worker)
        #   Start the App Event Loop
        app.exec()


    run_main()


After running the script, the following lines will be printed to the console as the worker runs:

..  code-block:: console
    :linenos:

    Worker with id d8fa8b9c-5160-48d8-8712-f592bef8addd has started its task

    Progress Received, value: 5, message: Starting
    Progress Received, value: 23.0, message: Step 1
    Progress Received, value: 41.0, message: Step 2
    Progress Received, value: 59.0, message: Step 3
    Progress Received, value: 77.0, message: Step 4
    Progress Received, value: 95.0, message: Step 5

    Worker Complete!
        Warnings: []
        Errors: []


As indicated in the console output, the worker first fired it's :attr:`~PySink.AsyncWorkerSignals.started` signal,
intermittently fired its :attr:`~PySink.AsyncWorkerSignals.progress` signal as it worked, then finally fired it's
:attr:`~PySink.AsyncWorkerSignals.finished` signal when its task was complete. All of this was done in a background
thread which frees up the UI thread to handle user input (if there was one present). In :ref:`Example 1<example-1>`, we will see
how to actually set up a full PySide Application with PySink, but before that let's see how to customize an :class:`~PySink.AsyncWorker` in
:ref:`basic-part-b` and :ref:`basic-part-c`.