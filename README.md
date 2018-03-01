# Lundy

Agent used to collect data and send it to Lunni

# Usage

Configure .lunni file with uri and project_source from current dir

```
uri=mongodb://{db_host}:{password}@{ip}/{db_name}
project_source=src/
```

```
pip install lundy
```

To collect data

```
python -m lundy -c
```

To send data to Lunni

```
python -m lundy -p
```



# Tests


To test collect.

Go to Lundy/lundy dir

To install current version:

```
pip install ./.. --upgrade
```

To run:

```
python -m lundy -c
```


# To use Runner
export LUNNICONFIG="lunni.ini"


