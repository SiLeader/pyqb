QB Process Incubator
=========

&copy; 2018 SiLeader and Cerussite.

## Overview
PyQB is process management system.

If process executed by PyQB is dead, restart same command.

## How to use
### --target TARGET
If you want to execute simple command, use this option.

```sh
pyqb --target "{COMMAND LINE}"
```

### --script SCRIPT
If you use this option, you can execute many process.

SCRIPT is python script that has `commands` function or generator.
`commands` function return List like object or generator.

#### ex
You want to execute these programs

```sh
PROGRAM arg_a
PROGRAM arg_b
PROGRAM arg_c
```

Python script is

```python
def commands():
    return ["PROGRAM arg_a", "PROGRAM arg_b", "PROGRAM arg_c"]
```

### --shell
PyQB does not execute in a shell.
PATH environment variable can not use in PyQB.

If you want to execute in the command line shell, you set this option.

## License
Apache License2.0

