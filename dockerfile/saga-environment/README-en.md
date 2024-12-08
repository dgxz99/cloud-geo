# SAGA-GIS arithmetic environment

A SAGA GIS environment image, based on Ubuntu 22.04 (jammy), which is compiled with all optional features.

## How to use it

### (1) Creating a data volume

You can create a data volume and store the data in it:

```bash
docker volume create saga-data
```

### (2) Creating containers

To create a container with a data volume mounted, go to the container's ``bash`` terminal and invoke ``saga_cmd`` from the command line:

```bash
# Create the container
docker run -it --name saga-gis -v saga-data:/data swsk33/saga-gis-environment bash
# Invoke the command
saga_cmd -h
```

A subsequent call to `saga_cmd` to invoke the operator is sufficient.
