# AI MTCNN Template

## Examples

![](https://i.imgur.com/XVjGKso.png)

![](https://i.imgur.com/XRdjCdd.png)

## Start

### Build the docker image

```bash
$ docker build -t ai_mtcnn_template .
```

### Run the docker container

```bash
$ docker run -d -e SCRIPT=app.py -e PORT=5001 -p 5001:5001 ai_mtcnn_template
```

or

```bash
$ docker run -d -e SCRIPT=stream_app.py -e PORT=5001 -p 5001:5001 ai_mtcnn_template
```