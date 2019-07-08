+++
date = "2017-05-23T08:59:49-07:00"
icon = ""
title = "Contributing"
weight = 5
chapter = false

+++

### Developing Clipper

Development of Clipper is coordinated through GitHub.

Clipper is under active development. Please create issues on our GitHub [repository](https://github.com/ucbrise/clipper) if you have any questions or feature requests. 

To get started, clone the [repository](https://github.com/ucbrise/clipper)
including submodules:

```sh
git clone --recursive https://github.com/ucbrise/clipper.git
```

{{% notice note %}}
If you've already cloned the repository at this point without the submodules,
you can include them by running `git submodule update --init --recursive` in
the Clipper repo.
{{% /notice %}}

__Build Dependencies:__

+ Boost
+ cmake >= 3.2
+ zeromq >= 4.1.0
+ hiredis
+ libev
+ redis-server >= 3.2
+ [Facebook Folly](https://github.com/facebook/folly)



__Building Clipper:__

First generate the CMake files with `./configure`. This generates an out-of-source build directory called `debug`.
Go into this directory and then run `make` to actually
compile the code. You should only need to re-run the configuration script if you change one of the `CMakeLists.txt` files.
To build for release, run `./configure --release` which generates the `release` build directory instead of debug.
If you want to clean everything up, you can run `./configure --cleanup` (if you get tired of being prompted, you can run `./configure --cleanup-quiet` to force cleanup without prompting).


{{% notice note %}}
Redis must be installed and on your path to run both the query REST frontend and the unit-tests.
You can test this with `redis-server --version`.
{{% /notice %}}

For example:

```sh
cd $CLIPPER_ROOT_DIR
./configure
cd debug
make

# write some code and compile it
make

# build and run unit tests with googletest
../bin/run_unittests.sh
```

Clipper has been tested on OSX 10.12 and on Debian stretch/sid and Ubuntu 12.04 and 16.04. It does not support Windows.

To file a bug or request a feature, please file a GitHub issue. Pull requests are welcome.

Before filing a pull request, make sure that C++ and Java code conforms to the project's Clang-Format style file and Python code conforms to the PEP 8 style. To automatically format your code before submitting a pull request, you can use
the provided formatting script:

```sh
./bin/format_code.sh
```

### Clipper Dev Docker Image

We packaged all dev dependency in Docker Image as well. You can use the following to avoid set up local environment and use Docker instead:

```sh
docker run -it --network=host -v <LOCAL_PATH_TO_CLIPPER>:/clipper -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp clipper/dev:develop
```
```sh
docker run -it --network=host -v /home/ubuntu/clipper:/clipper -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp clipper/py35-dev:develop
```

<!-- Development planning and progress is tracked with the [Clipper Jira](https://clipper.atlassian.net/projects/CLIPPER/issues). -->

