# Weather Analysis

Simple Flask App to display smart home device readings from your devices.

Note: currently Nest is returning client inactive messages, most likely as a result
of the message " Thank you for your interest in the Works with Nest program. We're upgrading our systems and will not accept new client reviews during this time. Please check back in a few weeks. If you have an urgent issue, please message us through the developer console."


For now only working with Netatmo data.

##Setuup

Run in a Python 3.7 venv (virtualenv), then:
`pip install -r requirements.txt`

Obtain a fresh netatmo token:
``

Run tests
`make weathertests`

Start flask app:
`python ShowKruegerHomeData.py`

Visit information page in your browser (locally or where deployed e.g. AWS lambda):

`http://127.0.0.1:5001/showall/KruegerHome`



 
