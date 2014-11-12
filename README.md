# debug

`debug` is a debug output tool for Python. It has two modes of function:

- A generic debug print when used as a function
- A function debugger when used as a function decorator

## Usage

### Debug Print
Use `from debug import debug` to include the object. Then you can use `debug` as a function just as you would use [the `print` function](https://docs.python.org/3/library/functions.html#print):

```python
from debug import debug

debug('this is a string')
debug('another', 'string', 'here', sep=' ')
```

You can also pass the keyword argument `pretty=True` to use `debug` as though it were [the pretty print function `pprint`](https://docs.python.org/3.4/library/pprint.html#pprint.pprint):

```python
debug([1, 2, 3], pretty=True, width=5)
```
yields
```
[1,
 2,
 3]
```

Because `debug` is overloaded as a decorator, if you want to debug print a single callable (function, class, etc.), you should pass it to `debug.out`:

```python
def my_function():
    pass

debug.out(my_function)
```
### Function Debugger

If you decorate a function with `debug`, each time the function is called, its arguments and return value will be printed to the console:

```python
@debug
def my_function(a, b, mult=1):
    return (a + b) * mult

my_function(2, 3)
my_function(5, -1, mult=2)
```
yields
```
my_function called with args:
(2, 3)
returned:
5

my_function called with args:
(5, -1)
kwargs:
{'mult': 2}
returned:
8
```
### Enabling and Disabling
`debug` is enabled by default, but can be toggled on and off by calling `debug.on()` and `debug.off()`.
When off, `debug` will have no effect: 
- Debug prints will do nothing
- Decorations will still run the function but will not print the arguments or return value 

Additionally, `debug` can be temporarily toggled on/off using `with` blocks:
```python
debug.off()

with debug.on:
	debug('debug is on for now')

debug('this will not print because debug is off again')
```

### Forcing Enabled State

You can have a specific use of `debug` function even when `debug` is turned off by using `debug.now` just as you would `debug`:
```python
@debug.now
def my_function(*args):
    # This function will always print it's args
    return

debug.off()
debug.now('this will print even though debug is turned off')
```

The behavior when nesting `with` blocks and `debug.now` is largely undefined. I would like to implement a better system for handling such cases and am open to suggestions for how they should behave. In the mean time, I would recommend using multiple debuggers (see below) if such control is needed.

### Multiple Debuggers
Complex management of enabled state can be achieved through multiple instances of the `Debug` class:

```python
from debug import Debug

debug = [Debug() for _ in range(2)]

debug[1].off()
debug[0]('test')
```

