PROJECT_SOURCE_DIR ?= $(abspath ./)
PROJECT_NAME ?= $(shell basename $(PROJECT_SOURCE_DIR))

all:
	@echo nothing special

clean:
	rm -rf build dist wheelhouse *.egg-info
force_clean:
	docker run --rm -v `pwd`:`pwd` -w `pwd` -it alpine/make make clean
.PHONY: clean force_clean

lint:
	pre-commit run -a
lint_install:
	pre-commit install

docs_build:
	mkdocs build
docs_serve:
	mkdocs serve -a 0.0.0.0:8088

DOCKER_TAG_WINDOWS ?= ghcr.io/cubao/build-env-windows-x64:v0.0.1
DOCKER_TAG_LINUX ?= ghcr.io/cubao/build-env-manylinux2014-x64:v0.0.3
DOCKER_TAG_MACOS ?= ghcr.io/cubao/build-env-macos-arm64:v0.0.1

test_in_win:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/win:`pwd`/build -it $(DOCKER_TAG_WINDOWS) bash
test_in_mac:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/mac:`pwd`/build -it $(DOCKER_TAG_MACOS) bash
test_in_linux:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/linux:`pwd`/build -it $(DOCKER_TAG_LINUX) bash

DEV_CONTAINER_NAME ?= $(USER)_$(subst /,_,$(PROJECT_NAME)____$(PROJECT_SOURCE_DIR))
DEV_CONTAINER_IMAG ?= $(DOCKER_TAG_LINUX)
test_in_container:
test_in_dev_container:
	docker ps | grep $(DEV_CONTAINER_NAME) \
		&& docker exec -it $(DEV_CONTAINER_NAME) bash \
		|| docker run --rm --name $(DEV_CONTAINER_NAME) \
			--network host --security-opt seccomp=unconfined \
			-v `pwd`:`pwd` -w `pwd` -it $(DEV_CONTAINER_IMAG) bash

PYTHON ?= python3
build:
	$(PYTHON) -m pip install scikit_build_core pyproject_metadata pathspec pybind11
	CMAKE_BUILD_PARALLEL_LEVEL=$(NUM_JOBS) $(PYTHON) -m pip install --no-build-isolation -Ceditable.rebuild=true -Cbuild-dir=build -ve.
python_install:
	$(PYTHON) -m pip install . --verbose
python_wheel:
	$(PYTHON) -m pip wheel . -w build --verbose
python_sdist:
	$(PYTHON) -m pip sdist . --verbose
python_test: pytest
pytest:
	python3 -m pip install pytest
	pytest tests/test_basic.py
.PHONY: build

restub:
	pybind11-stubgen naive_svg._core -o stubs
	cp stubs/naive_svg/_core.pyi src/naive_svg

# conda create -y -n py38 python=3.8
# conda create -y -n py39 python=3.9
# conda create -y -n py310 python=3.10
# conda create -y -n py311 python=3.11
# conda create -y -n py312 python=3.12
# conda env list
python_build_py38:
	PYTHON=python conda run --no-capture-output -n py38 make python_build
python_build_py39:
	PYTHON=python conda run --no-capture-output -n py39 make python_build
python_build_py310:
	PYTHON=python conda run --no-capture-output -n py310 make python_build
python_build_py311:
	PYTHON=python conda run --no-capture-output -n py311 make python_build
python_build_py312:
	PYTHON=python conda run --no-capture-output -n py312 make python_build
python_build_all: python_build_py38 python_build_py39 python_build_py310 python_build_py311 python_build_py312
python_build_all_in_linux:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/linux:`pwd`/build -it $(DOCKER_TAG_LINUX) make python_build_all
	make repair_wheels && rm -rf dist/*.whl && mv wheelhouse/*.whl dist && rm -rf wheelhouse
python_build_all_in_macos: python_build_py38 python_build_py39 python_build_py310 python_build_py311 python_build_py312
python_build_all_in_windows: python_build_all

repair_wheels:
	python -m pip install auditwheel # sudo apt install patchelf
	ls dist/* | xargs -n1 auditwheel repair --plat manylinux2014_x86_64

pypi_remote ?= pypi
upload_wheels:
	python -m pip install twine
	twine upload dist/*.whl -r $(pypi_remote)

tar.gz:
	tar -cvz --exclude .git -f ../polyline-ruler.tar.gz .
	ls -alh ../polyline-ruler.tar.gz

SYNC_OUTPUT_DIR ?= headers/include/cubao
sync_headers:
	mkdir -p $(SYNC_OUTPUT_DIR)
	cp src/cheap_ruler.hpp $(SYNC_OUTPUT_DIR)
	cp src/crs_transform.hpp $(SYNC_OUTPUT_DIR)
	cp src/cubao_inline.hpp $(SYNC_OUTPUT_DIR)
	cp src/eigen_helpers.hpp $(SYNC_OUTPUT_DIR)
	cp src/polyline_ruler.hpp $(SYNC_OUTPUT_DIR)
	cp src/pybind11_cheap_ruler.hpp $(SYNC_OUTPUT_DIR)
	cp src/pybind11_crs_transform.hpp $(SYNC_OUTPUT_DIR)
	cp src/pybind11_polyline_ruler.hpp $(SYNC_OUTPUT_DIR)

# https://stackoverflow.com/a/25817631
echo-%  : ; @echo -n $($*)
Echo-%  : ; @echo $($*)
ECHO-%  : ; @echo $* = $($*)
echo-Tab: ; @echo -n '    '
