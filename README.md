# foffinf

A way to use stdlib's logging with the new Format Specification Mini-Language.

# What?

We know it's bad to do this:

```python
logger.info(f"The result is {result:05d}")
```

We should never build the log message ourselves, basically because two situations that are avoided by properly using logging:
- performance: if the logging level is below INFO (in the case of the example) the resulting message is not really built
- robustness: if `result` happens to not be a number, that example will crash, but the `logging` infrastructure will just present some error message (and everything will continue)

The recommended way is:

```python
logger.info("The result is %05d", result)
```

But wait, we're living in the 21st century, are we still using _printf-style_ string formatting?

With `foffinf` we can now write:

```python
logger.info("The result is {:05d}", result)
```

Welcome to the future!

![dino](https://github.com/facundobatista/foffinf/blob/main/dino.png?raw=True)

Trust the dino :)


# How to use it

Sadly we can not set up *the whole* logging system in our process to this new format, because most probably we will be using 3rd party libraries that actually have log calls using the old way, and we shall not break them.

So we need to indicate which module (the one we're writing, of course) shall use it. This is done with a `foffinf.formatize` call. As is standard to use the module's name, we can just:

```python
import logging
import foffinf

foffinf.formatize(__name__)
logger = logging.getLogger(__name__)

# ...

logger.info("The result is {:05d}", result)
```

Affecting a specific logger module will not affect its parent or any sibling.

```
fofinff.formatize("mylib.mod1")

logging.getLogger("mylib.mod1")  # affected!
logging.getLogger("mylib")  # NOT affected
logging.getLogger("mylib.mod2")  # NOT affected
logging.getLogger()  # NOT affected
logging.getLogger("otherlib")  # NOT affected
logging.getLogger("mylib.mod1.submod")  # NOT affected
```

Note (in that last line) that by default it will neither affect submodules. To affect all children of a logger tree node:

```
fofinff.formatize("mylib.mod1", scatter=True)

logging.getLogger("mylib.mod1")  # affected!
logging.getLogger("mylib")  # NOT affected
logging.getLogger("mylib.mod2")  # NOT affected
logging.getLogger("mylib.mod1.submod_a")  # affected!
logging.getLogger("mylib.mod1.submod_b")  # affected!
```

## I can't make it work when setup logging in a helper file

It's typical to have this structure:
```
.
├── somefile
├── LICENSE
├── otherfiles
├── the_super_lib
│   ├── magic_code.py
│   ├── some_log_setup.py
│   ├── etc.py
├── README.md
└── ...
```

In all parts of your code, you just do
```
logger = logging.getLogger(__name__)
```

But the logging setup is done in a module inside your lib, `some_log_setup.py`. In this case is exactly where you need to use the `scatter` parameter explained before, stating explicitly the root of your lib.

So, inside `some_log_setup.py`:

```
import foffinf
...
foffinf.formatize("the_super_lib", scatter=True)
```

This will _formatize_ the calls in all your library's logging tree without affecting other libraries.


## What about using named replacements?

The logging module treats a passed single dictionary as the possible replacements for named values. We honour that, so this is supported:

```python
>>> info = {"foo": 3, "bar": 5}
>>> logger.info("The result is {foo} and {bar}", result)
The result is 3 and 5
```

If a single no-named parameter is used the dictionary is just shown:

```python
>>> info = {"foo": 3, "bar": 5}
>>> logger.info("The result is {}", result)
The result is {"foo": 3, "bar": 5}
```
