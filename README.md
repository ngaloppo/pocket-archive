# Installation

Install the dependencies through pip:

```
mkvirtualenv pocket-archive
pip install -r requirements.txt
```

In order to use the pocket API, you have to register a new pocket app. Do this by following the relevant links in the [Pocket developer docs](http://getpocket.com/developer/docs/overview).

Using this consumer key you will get an access token for the user by running the following:

```
python auth.py --key=<consumer-key>
```

Follow the instructions and the program will finish. Check your `.creds` file in the root directory of the project to make sure that it exists and has a consumer key and access token.

# Usage

First, download your items to a json file, then run the archive script.

```
python pocket_to_json.py
```

This will output a JSON file called `<timestamp>.json` to your current directory.

Then, do a test run to observe the number of archived articles for a given number of expiration days. This will print out the number of to-be-archived days.
```
python pocket_archive.py --days <num_days> <timestamp>.json
```
Finally, effectively archive by passing the `--archive` option: 
```
python pocket_archive.py --days <num_days> <timestamp>.json
```
Note that all auto-archived items will be tagged with the _old-unread_ tag.


