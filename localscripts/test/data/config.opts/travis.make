
CMAKE_FLAGS="-Wno-dev -DCMAKE_INSTALL_PREFIX=$HOME/dune -DCMAKE_BUILD_TYPE=DEBUG \
    -DCMAKE_CXX_FLAGS='-DDEBUG -g3 -ggdb -std=c++11  -O0 -DDUNE_GRID_EXPERIMENTAL_GRID_EXTENSIONS=1 -w -fprofile-arcs -ftest-coverage' \
    -DENABLE_HEADERCHECK=1 -DDISABLE_UBUNTU_WORKAROUND=1 -DDUNE_PYTHON_INSTALL_USER=travis"

MAKE_FLAGS="-j2 -l2"