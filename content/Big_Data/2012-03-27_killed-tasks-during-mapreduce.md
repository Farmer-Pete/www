Title: Killed Tasks During MapReduce
Summary: While trying to run an HBase backup, I kept seeing "killed tasks". It turns out the killed tasks are very different from failed ones. Failed tasks are tasks that ran into some programmatic problem and self-destructed. Killed tasks, on the other hand are terminated by their task tracker. There are several reason why a task will be killed.
Thumb: http://cdn.morguefile.com/imageData/public/files/d/duboix/preview/fldr_2010_04_05/file921270483562.jpg

Killed Tasks
------------

While trying to run an [HBase](tag:HBase) backup, I kept seeing "killed tasks". It turns out the killed tasks are very different from failed ones. Failed tasks are tasks that ran into some programmatic problem and self-destructed. Killed tasks, on the other hand are terminated by their task tracker.

There are several reason why a task will be killed during a [MapReduce](tag:MapReduce) job:

The task master dies
:   If the task master dies, then all the tasks belonging to this master will be killed

Task times out
:   If a task reports no progress for a long time, then it will be killed. This timeout value can be configured by setting `mapred.task.timeout property` in `mapred.xml`

Speculative execution
:   The [MapReduce](tag:MapReduce) model is to break jobs into many tasks and running them in parallel. One drawback to this model is that it only takes on slow task to slow down the entire system. Tasks can be slow for various reasons, but it can be very difficult to determine why. Rather than try to diagnose the problem, [Hadoop](tag:Hadoop) launches a duplicate as a backup when a task is running slower than expected. This is called _speculative execution_ of tasks. When one of the tasks finishes, any duplicate tasks are killed.

Speculative execution can be disabled via the `mapred.map.tasks.speculative.execution` and `mapred.reduce.tasks.speculative.execution` settings in `mapred.xml`

How do you know which reason killed the task?
---------------------------------------------

Unfortunately, I don't think the reason is documented in the logfile. If anyone knows for sure, I'd love to know!
