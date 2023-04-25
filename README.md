# foffinf

A hack lib to use logging with the new Format Specification Mini-Language

# What?

We know it's bad to do this:

```python
logger.info(f"The result is {result:05d}")
```

We should never build the log message ourselves, basically because two details that properly using logging avoids: 
- performance: if the logging level is below INFO the resulting message is not really built
- robustness: if `result` happens to not be a number that code will crash and logging will just present some error message but everything will continue

The recommended way is:

```python
logger.info("The result is %05d", result)
```

But wait, we're living in the 21st century, are we still using _printf-style_ string formatting?

With foffinf we can now write:

```python
logger.info("The result is {:05d}", result)
```

Welcome to the future!

# How to use it

Sadly we can not set up *the whole* logging system in our process to this new format, because most probably we will be using 3rd party libraries that actually have log calls using the old way, and we shall not break them.

So we need to indicate which module (the one we're writing, of course) shall use it. This is done with a `foffinf.contaminate` call. As is standard to use the module's name, we can just:

```python
import logging

import foffinf

foffinf.contaminate(__name__)
logger = logging.getLogger(__name__)

# ...

logger.info("The result is {:05d}", result)
```
