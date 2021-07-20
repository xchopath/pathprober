# pathprober
Probe and discover HTTP pathname using brute-force methodology and filtered by specific word or 2 words at once.

![version](https://img.shields.io/badge/version-0.3+dev-blue)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


![pathprober-sample](https://raw.githubusercontent.com/xchopath/pathprober/master/sample.jpg)

#### Purpose
Brute-forcing website directories or HTTP pathname and validate using HTTP response code is not relevant anymore. This tool will help you to perform a penetration test, because it could validate the directories using specific-word or 2 words at once and the results will more accurate.

#### It will help you to find:
- Web administrator/login panel
- Credential in some paths
- Third-party token
- Etc


## Installation
```
git clone https://github.com/xchopath/pathprober
cd pathprober/
```

#### Requirements
```
pip3 install -r requirements.txt
```


## Support
- Multiple URL targets (in a file separated by newline) or single URL target
- Multiple paths (in a file separated by newline) or single path
- 1 word or 2 words (filter)
- Save valid results to another file
- Multi-threading


## Sample usage
Multiple target, multiple path, and multiple words:
```
python3 pathprober.py -T target.txt -P path.txt -w "APP_NAME" -w2 "DB_PASSWORD"
```

Single target, multiple path, and single word:
```
python3 pathprober.py -t https://redacted.com/ -P path.txt -w "APP_NAME"
```

Multiple target, single path, multiple words, and save output to file:
```
python3 pathprober.py -T target.txt -p /.env -w "APP_NAME" -w2 "TWILIO" -o output.txt
```


## Need more help?
```
bash:~/pathprober$ python3 pathprober.py --help

 ___  ____ ___ _  _ ___  ____ ____ ___  ____ ____
 |__] |__|  |  |__| |__] |__/ |  | |__] |___ |__/
 |    |  |  |  |  | |    |  \ |__| |__] |___ |  \
       Probe HTTP pathname filtered by words

usage: pathprober.py [-h] [-t https://example.com] [-p pathname] [-T target.txt] [-P path.txt] [-w Word] [-w2 Word] [-o output.txt]

PathProber - Probe and discover HTTP pathname using brute-force methodology and filtered by specific word or 2 words at once

optional arguments:
  -h, --help            show this help message and exit
  -t https://example.com
                        Single website target
  -p pathname           Single pathname
  -T target.txt         Multiple target separated by newline
  -P path.txt           Multiple pathname separated by newline
  -w Word               A word that you want to find in a path
  -w2 Word              A second word that you want to find in a path
  -o output.txt         Save the results to file
```


## Contributors
- [@xchopath](https://github.com/xchopath) (from [@zerobyte-id](https://github.com/zerobyte-id))
