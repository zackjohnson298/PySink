.. _basic-part-d:

Part D - Defining Custom Signals
=======================================

Just like you can :ref:`define a custom result type<basic-part-c>`, you can also define custom
:class:`signals<PySink.AsyncWorkerSignals>` that your worker can emit. The signals that a worker can emit are stored in
the :attr:`~PySink.AsyncWorker.signals` attribute.

By default, an :class:`~PySink.AsyncWorker` emits three kinds of signals:

* :attr:`~PySink.AsyncWorkerSignals.started`: Signifies that the worker has started performing it's task
* :attr:`~PySink.AsyncWorkerSignals.progress`: Signifies that the worker has updated its progress. This usually gets connected to a function that displays progress to the user, possibly within a :class:`~PySink.Widgets.ProgressBarWidget`
* :attr:`~PySink.AsyncWorkerSignals.finished`: Signifies that the worker has completed it's task. This signal also passes along the results of the worker (see :ref:`Part C<basic-part-c>`)

In most cases, these signals are sufficient for the worker to fully communicate its state. However, it is sometimes
useful for your worker to have additional signals on top of those described above. In this example, our worker will
perform two distinct tasks sequentially, and it will fire a custom signal once the first task is completed.

