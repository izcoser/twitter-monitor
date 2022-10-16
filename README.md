# Requirements

```sh
python -m pip install twitter wget
```

# Usage

To download all media ever posted by an account and keep watching:

```sh
python twitter-monitor.py username
```

Optionally, also log the tweets to a file ```username-tweets```.

```sh
python twitter-monitor.py username --log
```
