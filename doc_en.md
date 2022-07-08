# Documentation
This application provides a tool to get an article text from an URl.

## Installation
Git clone this repo and enter ```ArticleParser``` directory

To install dependencies run:
```commandline
pip install -r requirements.txt
```

## Usage
To use the application use command:
```commandline
ArticleParser.py --url=https://yoursite/
```

Also you can configure the format of output file by ```settings.txt``` file.
In this file you can check parameters as "yes" if you want to print them in output file, or enter a number
in ```Line length limit``` parameter.

As article proceeded the output dir will be created automatically in the current dir.

