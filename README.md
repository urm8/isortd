# isortd
Simple http handler for [isort](https://github.com/PyCQA/isort) util. I liked the idea of putting 
[black[d]](https://black.readthedocs.io/en/stable/blackd.html) into my docker compose file and using
[BlackConnect](https://plugins.jetbrains.com/plugin/14321-blackconnect) plugin for auto sort without setting up
my dev env every time, but I was still missing sort formatting tool, that would work the same way. So its here...
Mb I'll release [IsortConnect](https://github.com/urm8/IsortConnect) and it will be more usable.
## install
```
$ pip install isortd
$ python -m isortd
``` 
