import requests
import xml.dom.minidom
import json

# Disable warnings on SSL
requests.packages.urllib3.disable_warnings()

# Define JSON parameters
encoded_body = json.dumps({
    "aaaUser" : {
        "attributes" : {
            "name" : "admin",
            "pwd" : "!v3G@!4@Y"
        }
    }
})

# Call requests with aaaUser
r = requests.post("https://sandboxapicdc.cisco.com/api/aaaLogin.json", data=encoded_body, verify=False)

# Parse response
header = {"Cookie" : "APIC-cookie=" + r.cookies["APIC-cookie"]}

# Grab tenant information with cookie

tenants = requests.get("https://sandboxapicdc.cisco.com/api/node/class/fvTenant.xml?rsp-subtree-include=health,faults", headers=header, verify=False)

# Parse tenants output to XML
dom = xml.dom.minidom.parseString(tenants.text)
xml = dom.toprettyxml()
tenant_list = dom.getElementsByTagName('fvTenant')
for tenants in tenant_list:
    tenant_name = tenants.getAttribute('name')
    tenant_dn = tenants.getAttribute('dn')
    health_score = tenants.firstChild.getAttribute('cur')
    output = "Tenant: " + tenant_name + "\t Health Score: " + health_score + "\n DN: " + tenant_dn
    print(output.expandtabs(40))