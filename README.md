
# EFSCRA.py

This repo contains a small script that gets info from the ef portal into a csv file.

To use just run it as:

``` bash
    ./ef.py --username "YOURUSERNAME" --password "YOURPASSWORD"
```

If you are using a python virtual environment you can run it by just by prepending Python - if you get errors with PhantomJS I recommend you to try this.

If you prefer to use the Chrome webdriver, you can specify the path to your driver with the --chrome flag.

Finally if your internet is quite slow, you can modify the waiting time with --waiting.