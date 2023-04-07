.. _basic-part-c:

Part C - Defining Custom Results
=======================================

Now that you've seen how to :ref:`implement a custom worker<basic-part-b>`, let's see how to customize the results of
your workers. In this example, we will create a new :class:`result<PySink.AsyncWorkerResults>` type and refactor the
CustomWorker from :ref:`Part B<basic-part-b>` so that it uses this new result type.

By default, the results of an :class:`~PySink.AsyncWorker` are contained within an
:class:`~PySink.AsyncWorkerResults` object. This object has the following attributes:

* :attr:`~PySink.AsyncWorkerResults.id`: The unique id of the worker
* :attr:`~PySink.AsyncWorkerResults.warnings`: Custom warnings encountered by the worker
* :attr:`~PySink.AsyncWorkerResults.errors`: Custom errors encountered by the worker
* :attr:`~PySink.AsyncWorkerResults.results_dict`: Result values of the workers task that were passed to :class:`~PySink.AsyncWorker.complete`

For many use cases, this basic result type is good enough. However, to make your application more robust and to take
full advantage of type-hinting, you can define a custom result type that has more descriptive attributes.

To define a custom result type, simply create a new class that inherits from :class:`~PySink.AsyncWorkerResults` and
within the class define your custom results as attributes:

..  code-block:: python
    :linenos:

    class CustomWorkerResults(AsyncWorkerResults):
        custom_result_1 = None
        custom_result_2 = None


To allow your worker to use your new result type, assign the :attr:`~PySink.AsyncWorker.results` attribute
of your worker to a new instance of your custom results within the worker's __init__ method:

..  code-block:: python
    :linenos:

    class CustomAsyncWorker(AsyncWorker):
        def __init__(self, delay_seconds: int, cycles=4):
            super(CustomAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles
            # Redefine the self.results attribute
            self.results = CustomWorkerResults()


Now that the result type has been assigned, your worker can store result data directly into
:attr:`~PySink.AsyncWorker.results`. This is what the :meth:`~PySink.AsyncWorker.run` method looks now like:

..  code-block:: python
    :linenos:

    class CustomAsyncWorker(AsyncWorker):
        ...
        def run(self):
            self.emit_start()
            progress = 5
            self.update_progress(progress, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / self.cycles
                self.update_progress(progress, f'Progress message #{ii + 1}')

            # Store the results directly into the attributes of self.results
            self.results.custom_result_1 = 'result 1'
            self.results.custom_result_2 = 'result 2'
            self.complete()

Storing result values into a custom :attr:`~PySink.AsyncWorker.results` attribute is the best way to emit results from
an :class:`~PySink.AsyncWorker`.

.. note::
    For flexibility, PySink still allows you to pass results as kwargs to
    :meth:`~PySink.AsyncWorker.complete`, even if you've defined a custom result type. In this scenario, the
    :meth:`~PySink.AsyncWorker.complete` will still package the results into the :attr:`~PySink.AsyncWorkerResults.results_dict`.
    However, it will also attempt to map the kwargs to the attributes of the custom result type *if and only if* the
    keywords match the attributes.


Just like we can access the new result attributes directly within :meth:`~PySink.AsyncWorker.run`, we can also access
them directly within the completion callback. We no longer need to extract the values from a dictionary, and type-hinting
makes the data extraction less prone to spelling mistakes and KeyErrors:

..  code-block:: python
    :linenos:

    def completion_callback(results: CustomWorkerResults):
        print(f'\nWorker Complete!')
        print(f'\tErrors: {results.errors}')
        print(f'\tWarnings: {results.warnings}')
        print(f'\tResult Attribute 1: {results.custom_result_1}')
        print(f'\tResult Attribute 2: {results.custom_result_2}')
        sys.exit()  # Exit the App event loop


Below is the full implementation of the worker with a custom result type:

..  code-block:: python
    :linenos:

    from PySide6.QtWidgets import QApplication
    from PySink import AsyncManager, AsyncWorker, AsyncWorkerProgress, AsyncWorkerResults
    import sys
    import time


    # Define a class representing your result type, storing result values as attributes
    class CustomWorkerResults(AsyncWorkerResults):
        custom_result_1 = None
        custom_result_2 = None


    class CustomAsyncWorker(AsyncWorker):
        def __init__(self, delay_seconds: int, cycles=4):
            super(CustomAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles
            # Redefine the self.results attribute
            self.results = CustomWorkerResults()

        def run(self):
            self.emit_start()
            progress = 5
            self.update_progress(progress, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / self.cycles
                self.update_progress(progress, f'Progress message #{ii + 1}')

            # Store the results directly into the attributes of self.results
            self.results.custom_result_1 = 'result 1'
            self.results.custom_result_2 = 'result 2'
            self.complete()


    # Function to be called whenever a worker's task has started
    def worker_started_callback(worker_id: str):
        print(f'Worker with id {worker_id} has started its task\n')


    # Function to be called whenever progress is updated
    def progress_callback(progress: AsyncWorkerProgress):
        print(f'Progress Received, value: {progress.value}, message: {progress.message}')


    # Function to be called when the worker is finished. Note that the results are now of type CustomWorkerResults.
    def completion_callback(results: CustomWorkerResults):
        print(f'\nWorker Complete!')
        print(f'\tErrors: {results.errors}')
        print(f'\tWarnings: {results.warnings}')
        print(f'\tResult Attribute 1: {results.custom_result_1}')
        print(f'\tResult Attribute 2: {results.custom_result_2}')
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


Running this script produces the following console output:

..  code-block:: console
    :linenos:

    Worker with id 0b160ae0-f3b1-4191-852a-fdd1e9c1c76b has started its task

    Progress Received, value: 5, message: Starting Task
    Progress Received, value: 35.0, message: Progress message #1
    Progress Received, value: 65.0, message: Progress message #2
    Progress Received, value: 95.0, message: Progress message #3

    Worker Complete!
        Errors: []
        Warnings: []
        Result Attribute 1: result 1
        Result Attribute 2: result 2


In most use cases, if your custom :class:`~PySink.AsyncWorker` will complete with result values, it is recommended that
a custom result type is created and implemented. This makes your code more understandable and less prone to bugs.
In the :ref:`final part<basic-part-d>` of the Basics, you will see how to customize your workers even further by
defining custom signals.