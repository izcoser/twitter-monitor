# twitter-monitor

```twitter-monitor``` is a short Python script used to watch all Twitter posts from a given user, logging the tweet text as well as saving the media. 

## Requirements

Twitter developer credentials are necessary for this to run. You can get them at [developer.twitter.com](developer.twitter.com).

Edit the credentials file accordingly and place save at the user home, ```~/credentials``` on Linux or ```C:\\Users\user\credentials``` on Windows.
And install the dependencies.
```sh
python -m pip install twitter wget
```

## Usage

To download all media ever posted by an account and keep watching:

```sh
python twitter-monitor.py username
```

Optionally, also log the tweets to a file ```username-tweets```.

```sh
python twitter-monitor.py username --log
```
