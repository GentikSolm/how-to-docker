# How To Docker

This is a template / reference repo for adding docker to projects.
I made this for a presentation for my university's Senior Seminar class,
where students are building some really cool, semester long projects.

## Presentation

To view the presentation, you can download [slides](https://github.com/maaslalani/slides) and run
`slides slides.md`, or just open the `slides.md` file with your preferred markdown viewer.

## Contents

There are 3 examples in this project.  
First, and most basic, is the `simple-nginx` folder.
This is a small nginx docker image, that demonstrates using `just`,
docker compose, and a simple Dockerfile.

Next, is the `flask-app` project. This demonstrates everything from the nginx example,
along with multiple build targets, and using python for a docker image contents.

Finally, we have the most complex `fullstack-app`. This is a t3 boilerplate app hooked up to
postgres, networked with docker-compose, tested with gh-actions on pull requests, multiple build targets,
linting, and more.

## References

The following links may be useful to continue learning docker

- [Docker docs](https://docs.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/)
- [How to docker](https://docker-curriculum.com/)

Some more resources that are not docker related, but help with docker

- [Just](https://github.com/casey/just)
