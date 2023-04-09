.. _basic-part-d:

Part D - Defining Custom Signals
=======================================

Just like you can :ref:`define a custom result type<basic-part-c>`, you can also define custom
:class:`signals<PySink.AsyncWorkerSignals>` for your worker to emit. The signals that a worker can emit are stored in
the :attr:`~PySink.AsyncWorker.signals` attribute.

By default, an :class:`~PySink.AsyncWorker` emits three kinds of signals:

* :attr:`~PySink.AsyncWorkerSignals.started`: Signifies that the worker has started performing it's task (fired when :meth:`~PySink.AsyncWorker.emit_start` is called)
* :attr:`~PySink.AsyncWorkerSignals.progress`: Signifies that the worker has updated its progress. This usually gets connected to a function that displays progress to the user, possibly within a :class:`~PySink.Widgets.ProgressBarWidget`
* :attr:`~PySink.AsyncWorkerSignals.finished`: Signifies that the worker has completed it's task. This signal also passes along the results of the worker (see :ref:`Part C<basic-part-c>`)

In most cases, these signals are sufficient for the worker to fully communicate its state. However, it is sometimes
useful for your worker to have additional signals on top of those described above. In this example, our worker will
perform two distinct tasks sequentially, and it will fire a custom signal once the first task is completed.

First, let's define the custom signal type. Just like custom results inherit from :class:`~PySink.AsyncWorkerResults`,
custom signals inherit from :class:`~PySink.AsyncWorkerSignals`. PySide6 signals can pass along any value type, but in
this example it will pass along a simple string:

..  code-block:: python
    :linenos:

    class CustomWorkerSignals(AsyncWorkerSignals):
        part_1_complete_signal = Signal(str)

Now that the signals are defined, let's take a look at this example's worker:

..  code-block:: python
    :linenos:

    class CustomAsyncWorker(AsyncWorker):
        def __init__(self, delay_seconds: int, cycles=4):
            super(CustomAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles
            # Redefine the 'results' and 'signals' attributes
            self.results = CustomWorkerResults()
            self.signals = CustomWorkerSignals()

        def do_part_1(self):
            progress = 5
            self.update_progress(progress, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / (2 * self.cycles)
                self.update_progress(progress, f'Progress message from part 1 #{ii + 1}')
            self.results.custom_result_1 = 'result 1'

        def do_part_2(self):
            progress = 50
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / (2 * self.cycles)
                self.update_progress(progress, f'Progress message from part 2 #{ii + 1}')
            self.results.custom_result_2 = 'result 2'

        def run(self):
            self.emit_start()
            self.do_part_1()
            self.signals.part_1_complete_signal.emit('Part 1 Complete')
            self.do_part_2()
            self.complete()


Within the :class:`~PySink.AsyncWorker.__init__` method, the :attr:`~PySink.AsyncWorker.signals` attribute and the
:attr:`~PySink.AsyncWorker.results` attributes are redefined (this example will use the same result type as
:ref:`Part C<basic-part-c>`). This worker has two tasks that are separated out into their own methods. Within
:meth:`~PySink.AsyncWorker.run`, we emit the :attr:`~PySink.AsyncWorkerSignals.started` signal, perform the first task,
emit the custom part_1_complete signal, perform the second task, and finally emit the :attr:`~PySink.AsyncWorkerSignals.finished`
signal.

Just like the :attr:`~PySink.AsyncWorkerSignals.progress` and :attr:`~PySink.AsyncWorkerSignals.finished` signals get
connected to callbacks, the custom signal needs to be connected to a callback as well. This callback receives a string
from the signal and prints it to the console:

..  code-block:: python
    :linenos:

    def custom_signal_callback(signal_value: str):
        print(f'\nCustom Signal received! Value: {signal_value}\n')

Now that everything is defined, let's see the full example:

..  code-block:: python
    :linenos:

    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Signal
    from PySink import AsyncManager, AsyncWorker, AsyncWorkerProgress, AsyncWorkerResults, AsyncWorkerSignals
    import sys
    import time


    # Define a class representing your result type, storing result values as attributes
    class CustomWorkerResults(AsyncWorkerResults):
        custom_result_1 = None
        custom_result_2 = None


    # Define a class representing your signal type, storing signals as attributes
    class CustomWorkerSignals(AsyncWorkerSignals):
        part_1_complete_signal = Signal(str)


    class CustomAsyncWorker(AsyncWorker):
        def __init__(self, delay_seconds: int, cycles=4):
            super(CustomAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles
            # Redefine the 'results' and 'signals' attributes
            self.results = CustomWorkerResults()
            self.signals = CustomWorkerSignals()

        def do_part_1(self):
            progress = 5
            self.update_progress(progress, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / (2 * self.cycles)
                self.update_progress(progress, f'Progress message from part 1 #{ii + 1}')
            self.results.custom_result_1 = 'result 1'

        def do_part_2(self):
            progress = 50
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += 90 / (2 * self.cycles)
                self.update_progress(progress, f'Progress message from part 2 #{ii + 1}')
            self.results.custom_result_2 = 'result 2'

        def run(self):
            self.emit_start()
            self.do_part_1()
            self.signals.part_1_complete_signal.emit('Part 1 Complete')
            self.do_part_2()
            self.complete()


    # Function to be called when the custom signal is emitted
    def custom_signal_callback(signal_value: str):
        print(f'\nCustom Signal received! Value: {signal_value}\n')


    # Function to be called whenever a worker's task has started
    def worker_started_callback(worker_id: str):
        print(f'Worker with id {worker_id} has started its task\n')


    # Function to be called whenever progress is updated
    def progress_callback(progress: AsyncWorkerProgress):
        print(f'Progress Received, value: {progress.value}, message: {progress.message}')


    # Function to be called when the worker is finished. The results are now of type CustomWorkerResults.
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
        worker.signals.part_1_complete_signal.connect(custom_signal_callback)
        worker.signals.started.connect(worker_started_callback)
        worker.signals.progress.connect(progress_callback)
        worker.signals.finished.connect(completion_callback)
        #   Start the Worker and App event loop
        manager.start_worker(worker)
        app.exec()


    run_main()


Running this script prints the following to the console:

..  code-block:: console
    :linenos:

    Worker with id cd5575e0-5ec2-4dd9-b15a-daae136c3528 has started its task

    Progress Received, value: 5, message: Starting Task
    Progress Received, value: 20.0, message: Progress message from part 1 #1
    Progress Received, value: 35.0, message: Progress message from part 1 #2
    Progress Received, value: 50.0, message: Progress message from part 1 #3

    Custom Signal received! Value: Part 1 Complete

    Progress Received, value: 65.0, message: Progress message from part 2 #1
    Progress Received, value: 80.0, message: Progress message from part 2 #2
    Progress Received, value: 95.0, message: Progress message from part 2 #3

    Worker Complete!
        Errors: []
        Warnings: []
        Result Attribute 1: result 1
        Result Attribute 2: result 2


