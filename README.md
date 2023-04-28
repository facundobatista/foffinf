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
