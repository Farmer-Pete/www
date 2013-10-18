Title: Optimize Python functions with the @subsequent decorator
Summary: Often I write code where a function must do something special on the first execution. This usually leads to a constant polling where a condition must be checked, possibly millions of times, even though the condition will only ever be met once. I created a `@subsequent` decorator to help optimize this problem.
Thumb: http://upload.wikimedia.org/wikipedia/commons/6/69/Electrical_Machinery_1917_-_knife_switch.jpg

Context
-------

Let's say we have class method, `List` and a method `append()` that required the following logic:

  * If `List.append()` has never been run, `List.data` must be `None`
  * `List.append()` takes an integer as an argument and then appends it to `List.data`
     * If this is the first time `List.append()` is being run, it must first create a list and assign it to `List.data`

Here is a simple way to implement this class and method in [Python](tag:python):


    #!python
    Class List(object):

        def __init__(self):
            self.data = None

        def append(self, integer):
            if self.data is None:
                self.data = [ integer ]
            else:
                self.data.append(integer)

This implementation performs fairly well (about 400ms for 1 million calls to `List.append`) but is wasteful as every time `List.append` is executed, it must:

   * resolve `self.data` three times
   * test to see if `self.data` is `None`

For the sake of argument, let's say that the appending logic and first run logic is a lot more in-depth and must be split into reusable functions. One way to accomplish this would be:

    #!python
    Class List(object):

        def __init__(self):
            self.data = None

        def append(self, integer):
            if self.data is None:
                self._appendFirst()
            else:
                self._appendSubsequent(integer)

        def _appendFirst(self):
            self.data = list()

        def _appendSubsequent(self, integer):
            self.data.append(integer)

This implementation performs slower (about 600ms for 1 million calls to `List.append`). For larger, more complicated functions, this type of implementation may be required.

Subsequent to the rescue
------------------------

I created a small [decorator](tag:decorator), called `@subsequent` (code is at the bottom of this post). As it's names suggests, it will run the decorated function during the first invocation. However, subsequent calls will invoke the function specified in the decorator. This eliminates the need to constantly checking to see if this is the first execution, boosting [performance](tag:performance).

Using the `@subsequent` decorator, the `List` class can be implemented as:

    #!python
    Class List(object):

        def __init__(self):
            self.data = None

        @subsequent('_appendSubsequent')
        def append(self, integer):
            self.data = [ integer ]

        def _appendSubsequent(self, integer):
            self.data.append(integer)

Or, the reusable version:

    #!python
    Class List(object):

        def __init__(self):
            self.data = None

        @subsequent('_appendSubsequent', fallthrough=True)
        def append(self, integer):
            self._appendFirst(self)

        def _appendFist(self, integer):
            self.data = list()

        def _appendSubsequent(self, integer):
            self.data.append(integer)

The cool thing about `@subsequent` is that both versions have the same [performance](tag:performance) (300ms for 1 million calls to `List.append`). That's 33% faster than the simple version and 100% faster then the reusable version. Not bad for a little [decorator](tag:decorator) `:)`

And now for the code
--------------------

    #!python
    def subsequent(functionName, fallthrough=False, toggleVar=None, toggleInit=False):
        """
        First runs decorated function (if fallthrough is True, provided function is also run)
        Then the decorated function points to the function provided
        Otherwise, the decorated function turns into a noop

        A couple of special attributes are added:
            .reset() # Resets the decorated function back to it's first-run functionality
            .<toggleVar> # A boolean that will indicate what mode it is in (first or subsequent mode)
        """

        if toggleVar is None:
            toggleVar = 'isFirst'

        def setup(function):
            setattr(function, toggleVar, toggleInit)
            setattr(function, 'reset', lambda *args, **kwargs: None)

        if functionName:
            def getSubsequent(self):
                for classObj in inspect.getmro(self.__class__):
                    if functionName in classObj.__dict__:
                        return classObj.__dict__[functionName], getattr(self, functionName)
        else:
            def getSubsequent(self):
                function = lambda *args, **kwargs: None
                return function, function

        def decorator(target):

            def reset(self):
                # Resets back to the first function
                function = partial(firstWrapper, self)
                setup(function)
                setattr(self, target.__name__, function)

            def firstWrapper(self, *args, **kwargs):
                # Call first function
                result = target(self, *args, **kwargs)

                # Point to subsequent function and set up reset function
                functionObj, functionPtr = getSubsequent(self)
                setattr(functionObj, 'reset', partial(reset, self))
                setattr(functionObj, toggleVar, not toggleInit)
                setattr(self, target.__name__, functionPtr)

                if fallthrough:
                    result = functionPtr(*args, **kwargs)

                # Return result
                return result

            setup(firstWrapper)

            return firstWrapper

        return decorator
