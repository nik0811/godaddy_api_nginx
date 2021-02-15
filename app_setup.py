#!/usr/bin/env python3 
import sys, getopt
from jinja2 import Template
import requests

def customer_setup(argv):
      #<customer_domain>will be your default subdomain always, Which should be given as an Arguments.
      #<point_to> IP to point to your subdomain.
      customer_domain="13.127.43.247"
      ssl="true"

      #GoDaddy Variable
      godaddy={"key": "revanth.unnam", "secrets": "ODE0MjAwOTJAQ2MK", "domain": "apptmart.com", "match_type": "A", "ttl": 3600, "point_to": "13.127.43.247"}
      for key, value in godaddy.items():
          if len(str(value))==0:
              print("Pass the correct Value in godaddy dictionary variable in the script (key: XXXXX, secrets: XXXXXX, etc...!!!).")
              print("*********** Run Script With Proper Arguments *****************")
              print('./app_setup.py -d <customer_domain> -s <ssl==true/false>')
              sys.exit()
      
      #To list all the records visit the below urls
      #https://api.godaddy.com/v1/domains/{{domain}}/records/
      godady_api="https://api.godaddy.com/v1/domains/%s/records/"%(godaddy["domain"])
      headers={'content-type': 'application/json', "Accept": "application/json",'Authorization': 'sso-key %s:%s'%(godaddy["key"], godaddy["secrets"])}
      try:
          if len(sys.argv)<2:
              print('app_setup.py -d <customer_domain> -s <ssl==true/false>')
              sys.exit()
          opts, args = getopt.getopt(argv, "d:s:h",["dns=customer_domain.apptmart.com", "ssl=true"])
      except getopt.GetoptError:
          print('app_setup.py -d <customer_domain> -s <ssl==true/false>')
          sys.exit(2)
      for opt, arg in opts:
          if opt == "-h":
              print('app_setup.py -d <customer_domain> -s <ssl==true/false>')
              sys.exit()
          elif opt in ("-d", "--dns"):
               customer_domain = arg
          elif opt in ("-s", "--ssl"):
               ssl = arg
          else:
              print('app_setup.py -d <customer_domain> -s <ssl==true/false>')
              sys.exit()

      #Creating Nginx configuration for Register User
      with open('default.conf') as conf:
          nginx_conf_parse = Template(conf.read())
      with open("%s.conf"%(customer_domain), "w") as nginx_conf:
          nginx_main_conf = nginx_conf_parse.render(customer_domain=customer_domain, ssl=ssl)
          nginx_conf.write(nginx_main_conf)

      #GoDaddy Subdomain Creation
      data=[{"type": godaddy["match_type"], "ttl": godaddy["ttl"],"name": customer_domain, "data": godaddy["point_to"]}]
      requests.patch(godady_api, headers=headers, json=data)
      print("Customer Subdomain Created: %s.%s"%(customer_domain,godaddy["domain"]))
if __name__ == "__main__":
    customer_setup(sys.argv[1:])
