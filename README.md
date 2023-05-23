# CosmosExplorerBot
An explorer for humans.ai (or any Cosmos-based network, for that matter!) that works in Telegram.

Using Python and an API server, the bot gets all the info needed about **chain ID**, current **block height**, and an **active set** of validators.
If you want to see the details of a specific validators, **valoper address**, **commission rates**, **descriptions** & **websites** are all displayed.

While interacting with bot's menu, all the info is updated in **real time**.

#

At first, you need to configure the bot: in **main.py** in the *main()* method enter your Telegram Bot Token, and in *data_fetcher.py* enter the IP & port of your API server.

Then, make sure you have these packages installed via ***pip***: *requests*, *python-telegram-bot==13.12*

Finally, launch the bot!
***python3 main.py***

#

When interacting with the bot, it processes 2 commands: */start* & */menu*. The 1st one shows the details about what it can do, and the 2nd command is displaying the active set & clickable buttons to see the information about a specific validator.

#

There's a working bot for humans.ai project already!
https://t.me/cosm_mon_bot
