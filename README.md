# RaidMap
Pokemon GO Scanner for Raids

# How does it work?
It uses a database of gyms obtained from Monocle / RocketMap, and then occasionally scans them [using a light-weight web server.](https://github.com/ibuckshot5/RaidEngine) Once a raid is spotted, it will not scan that gym until the raid egg hatches, at which point it will scan it again to find out what it hatched into. Once the raid is over, RaidMap will go back to scanning it as usual.

# How do I use it?
You will need to provide an `accounts.csv` file. **RaidMap DOES NOT NEED non-shadowbanned accounts. IIRC Shadowbanned accounts can still see gyms.**

Once you're done that, head over to `config.json` and fill it out with your settings.
