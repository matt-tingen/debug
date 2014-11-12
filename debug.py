from functools import wraps
from pprint import pprint

class Debug:
    enabled = True
    allow_now = True

    def __init__(self):
        class on:
            def __init__(self, parent):
                self.parent = parent

            def __call__(self):
                self.parent.enabled = True

            def __enter__(self):
                self.parent.enabled = True

            def __exit__(self, exc_type, exc_value, traceback):
                self.parent.enabled = False

        class off:
            def __init__(self, parent):
                self.parent = parent

            def __call__(self):
                self.parent.enabled = False

            def __enter__(self):
                self.parent.enabled = False
                self.parent.allow_now = False

            def __exit__(self, exc_type, exc_value, traceback):
                self.parent.enabled = True
                self.parent.allow_now = True

        self.on = on(self)
        self.off = off(self)

    def now(self, val, *args, **kwargs):
        if self.allow_now:
            if callable(val) and not args and not kwargs:
                return self._decorate(val, True)
            else:
                prev_status = self.enabled
                self.enabled = True
                self.out(val, *args, **kwargs)
                self.enabled = prev_status

    def out(self, val, *args, **kwargs):
        if self.enabled:
            if 'pretty' in kwargs and kwargs['pretty']:
                p = pprint
            else:
                p = print

            try:
                del kwargs['pretty']
            except KeyError:
                pass

            p(val, *args, **kwargs)

    def _decorate(self, subject, skip_enable_check):
        @wraps(subject)
        def print_args_and_return(*args, **kwargs):
            if (skip_enable_check or self.enabled) and self.allow_now:
                print(subject.__name__, 'called ', end='')

                if args or kwargs:
                    print('with ', end='')
                else:
                    print('without arguments')

                if args:
                    print('args:')
                    pprint(args)

                if kwargs:
                    print('kwargs:')
                    pprint(kwargs)

                # We have to call the function after the arguments have been
                # printed in case any of them get mutated in the function.
                return_val = subject(*args, **kwargs)


                if return_val:
                    print('returned:')
                    pprint(return_val)

                if args or kwargs or return_val:
                    print('')

                return return_val
            else:
                return subject(*args, **kwargs)

        return print_args_and_return

    def __enter__(self):
        self.enabled = True

    def __exit__(self, exc_type, exc_value, traceback):
        self.enabled = False

    def __call__(self, val, *args, **kwargs):
        # Apply decorator regardless of `enabled`.
        # `enabled` will be checked each time the function is called so `debug`
        # can be toggled freely independent of when the decorator is applied.
        if callable(val) and not args and not kwargs:
            return self._decorate(val, False)
        elif self.enabled:
            self.out(val, *args, **kwargs)


debug = Debug()