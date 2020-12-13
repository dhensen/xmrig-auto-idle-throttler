# xmrig auto throttler

This program automatically throttles xmrig when you start using your computer and stops throttling when you become idle again. It does so by defining two profiles, which are two config.json's, one for the minimum load situation, one for the maximum load situation.

## Installation

### Arch Linux (or other arch-derivatives like Manjaro, etc...)

```shell
sudo pacman -S xprintidle
pip3 install xmrig-auto-throttler
```

### Ubuntu (or other Debian based distros)

```shell
sudo apt-get install xprintidle
pip3 install xmrig-auto-throttler
```

### Windows

> Coming soon

## Usage

This script only works when the XMRIG api is enabled, so first enable this by editing your config.json:

```
{
    ...
    "http": {
        "enabled": true,
        "host": "127.0.0.1",
        "port": 8000,
        "access-token": "MySuperSecretToken",
        "restricted": false
    },
    ...
}
```

Make a two copies of you config.json, one for the maximum profile, one for the minimum profile:

```
cd xmrig-6.6.2
cp config.json maximum-config.json
cp config.json minimum-config.json
```

Now edit the `minimum-config.json` and `maximum-config.json` to be let the minimum profile be a throttler version of the maximum profile.

I for example use this as minimum-config.json:

```json
{
    ...
    "cpu": {
        ...,
        "rx": [0, 1, 2, 3],
        ...
    },
    ...
}
```

And double the amount of threads for maximum-config.json:

```json
{
    ...
    "cpu": {
        ...,
        "rx": [0, 1, 2, 3, 4, 5, 6, 7],
        ...
    },
    ...
}
```

Now from the folder where the configs are created:

```
xmrig-auto-throttler
```

## CLI Settings

- `--interval`
  - default: 5
  - unit: seconds
  - This defines the polling interval. By default this checks your idle status every 5 seconds and switches profile accordingly
- `--max-profile-timeout`
  - default: 60
  - unit: seconds
  - This defined the time that you have to be idle for the maximum profile to kick in.
- `--min-profile-timeout`
  - default: 10
  - unit: seconds
  - This defined the maximum time that you have to be non-idle for the minimum profile to kick in.
- `--xmrig-api-url`
  - default: http://127.0.0.1:8000
  - The xmrig api url, may contain a port.
- `--xmrig-api-token`
  - default: empty

### Example

```
xmrig-auto-throttler --interval 1 --max-profile-timeout 300 --min-profile-timeout 5 --xmrig-api-url http://127.0.0.1:8000 --xmrig-api-token MySuperSecretToken
```

> interval needs to be smaller than min-profile-timeout else the switch to min profile wont be made

Above command will poll idle status each second. When maximum profile is active, profile will be switched to minimum when you go from idle to not-idle. When minimum profile is active, it will switch to maximum profile when you are idle for 5 minutes (300sec).

## Donate

Please consider a donation if you find this program useful.

- XMR: 4AeP7Piu23yDrYS3dmDMbc3jVzLKbP8QVcBPi9NW5ywKQwgH47ekGr6fjPzGS6WwGQaYTeXC72pSuiVvoXqfrcMH8qKe174
