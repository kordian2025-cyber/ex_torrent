# EX-Torrenty Plugin

**Plugin Version:** 3.3  
**Documentation Version:** 1.01  
**Author:** KordianJ (5c0rp10n) kordian2025@gmail.com  
**Co-Author:** powerzasty  
**Acknowledgments:** ex-torrenty.com  
**License:** GPLv3+  
**Last Modified:** 15.10.2025

---

## Overview

`ex_torrenty.py` is a Python plugin that allows searching and downloading torrents from [EX-Torrenty](https://ex-torrenty.org/) through their API.  
The plugin retrieves torrent metadata and supports downloading `.torrent` files using session cookies for authentication.

The plugin is built on **`novaprinter`**, following the **qBittorrent plugin documentation**.

---

## Included Files

The plugin uses the following helper modules originally provided by **qBittorrent**:

* `helpers.py`  
* `nova2.py`  
* `nova2dl.py`  
* `novaprinter.py`  
* `socks.py`  

> ⚠️ It is recommended to check if newer versions of these files are available before use.

Additionally, an `install` directory is included, containing a Python script for generating cookies.

---

## Official Documentation

Official documentation for creating search plugins is available on GitHub:

[qBittorrent Plugin Documentation](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin)

---

## Requirements

No additional Python packages are required if the plugin is used in its basic form.  
Installation can be done according to the official qBittorrent documentation.  
A `requirements.txt` file is included for convenience.

---

## Configuration – Session Cookies

⚠️ **Important:** To use this plugin, you must provide **session cookies from your EX-Torrenty account**.

1. Log in to [EX-Torrenty](https://ex-torrenty.org/) using your browser.  
2. Retrieve the following session cookies:

   * `uid`  
   * `pass`  
   * `hashv`  
   * `PHPSESSID`  

3. Replace the values in the `COOKIES` dictionary in `ex_torrenty.py` with your own session cookies. Example:

```python
COOKIES = {
    "uid": "xxxxxx",
    "pass": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "hashv": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "PHPSESSID": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

> The plugin will not work without valid session cookies.

---

### Automatic Cookie Generator

In the `install/` directory, you will find a helper script that generates a JSON file with the required session cookies:

* `instalator.py`

Required Python packages to run this script:

* `beautifulsoup4>=4.12.0`  
* `selenium>=4.21.0`

---

## Usage Outside qBittorrent

The plugin can also be tested directly in the terminal.  
The first search result will be downloaded automatically.

---

## License

The plugin is released under the **GPLv3+ license**.  
You may use, modify, and distribute it freely.  
Use it at your own risk.

> ⚠️ Users are responsible for ensuring the legality of downloading content in their country.
