# slugs-discord-bot

### A.K.A.:

- **slugsnet**
- **R.O.N.**
- **dipshit**

This is a Discord bot created for the SLUGSoc Discord server by [@RaptureAwaits](https://github.com/RaptureAwaits "one of the programmers of all time").

It performs the following basic moderation tasks:

- New member challenge to keep out bots
- Audit logging for message edits/deletes
- Shared access authenticator for 2FA

## Requirements

**Python >= 3.10**

This project makes use of the pipe operator (`|`) for defining unions in typehints, 
[added in 3.10](https://docs.python.org/3/library/stdtypes.html#types-union "Python docs 🔥🔥🔥"). Anything lower 
will throw errors.

## Basic Usage

- Clone repository
- Create a virtual environment
- `pip install -r requirements.txt`
- `python main.py`
- Follow prompts for config file setup
- `python main.py`
- Enjoy

## Configuration Specifics

On first launch, **slugsnet** will (attempt to) copy some files from `config_templates/`, and create some directories 
within the project root folder. These include:
- `slugs-discord-bot/`
  - `token.yaml`
  - `server_configs/`
    - `example0.yaml`
  - `logs/`

### Setting the token

`token.yaml` must be populated with the corresponding Discord application's token. This can be obtained from the 
developer dashboard.

### Configuring a server

On startup, **slugsnet** will read each file in `server_configs/` and store the contents in memory. This config file 
contains the guild ID for the guild (server) being configured, as well as a lot of ID fields and some strings.

To create a new config for a server, copy the `config_template.yaml` file into `server_configs/`, rename it to 
something vaguely descriptive (or don't, the filename has no bearing on anything), and populate the fields within.

IDs for channels, guilds, and roles can be retrieved by right-clicking elements in the Discord client after 
[enabling developer mode](https://discord.com/developers/docs/activities/building-an-activity#step-0-enable-developer-mode).

Configs are stored in memory as a standard dictionary keyed by guild ID. This means that providing multiple config 
files for the same server will simply cause the latest one in the load order to take effect. Best not to do this.

Currently, **slugsnet** will only read config files on startup, and so must be restarted for config changes to take 
effect.
