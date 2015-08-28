# Schwarzie
Schwarzie is an ellie-slack bot reading from users's input in order to learn words, sentences and, maybe one day, be able to talk autonomously. The idea is that chatbot are usually quickly boring because answers are pre-formatted, thus learning from actual people chatting may improve the quality of answers. On the other hand, it's a practical exercise on programming (text-processing) neural networks, which is a current active field of research.

# ellie-slack
Meet Ellie, Eliza's younger, hipper, psychobabble-friendly successor. She makes a great Slackbot.

## Background
Ellie's is Slack's Python-based [real-time messaging bot](https://github.com/slackhq/python-rtmbot) wrapped around  Daniel Connelly's [Python implementation](https://github.com/dhconnelly/paip-python) of Peter Norvig's *Paradigms of AI Programming* Eliza .. with updated diction. Loads has changed since 1991, and she seemed a little standoff-ish – which also led to her new, hip name.

The langauge updates rendered her internals less elegant, but I think – hope – they make Ellie more fun than Eliza ever was.

### Modding Ellie
If you'd like to dive into Ellie's innerworkings, [ellie.py](https://github.com/christinac/ellie-slack/blob/master/plugins/ellie/ellie.py) is your file. Push changes back here, in a branch, if you think others will appreicate your wit.

### Dependencies
* [websocket-client](https://pypi.python.org/pypi/websocket-client/)
* [python-slackclient](https://github.com/slackhq/python-slackclient)

### Installation
1. Download Ellie

  ````
  git clone git@github.com:christinac/ellie-slack.git
  cd ellie-slack
  ````

2. Install dependencies

  ````
  pip install -r requirements.txt
  ````

3. Configure rtmbot ([Slack instructions](https://christinac.slack.com/services/new/bot).) From the Slack console, you'll get to choose your bot's name and icon. Though we've become partial to Ellile, bot-naming is up to you.

  ````
  cp example-config/rtmbot.conf .
  vi rtmbot.conf
  SLACK_TOKEN: "xoxb-11111111111-222222222222222"
  ````

4. Run her! (You've got to keep her running so long as you'd like her to keep chattering; something like [nohup](http://linux.die.net/man/1/nohup) might be helpful.)

````
  python rtmbot.py
````

## Ellie in action
![Ellie in action](screenshot.png)
