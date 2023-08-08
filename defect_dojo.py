import json
import logging
import requests
import subprocess

# token is for a localhost DD deployment, so it's fine to commit
headers = {'content-type': 'application/json', 'Authorization': 'Token 5c3f5c0b517a7847f57ae03ca50f8dcfedfce3cd', 'X-CSRFTOKEN': 'UjuCuq4MLJVrRJY3BQ64hlC0CABBSAixFXpLwxTMN5h4BlS0lzRjvCcdkir7S9yj'}
server = "http://localhost:8081/api/v2/"
def check_product_exists(product_name):
    result = requests.get(server + 'products/?name=' + product_name, verify=False, headers=headers)
    r = json.loads(result.content)
    if r['count'] > 0:
        return False
    else:
        return True

def create_product(name, description):
    result = subprocess.run(["curl", "-X", 'POST', server + 'products/',
        "-H", 'accept: application/json', "-H", 'Content-Type: multipart/form-data',
        "-H", 'Authorization: Token 5c3f5c0b517a7847f57ae03ca50f8dcfedfce3cd',
        "-H", 'X-CSRFTOKEN: UjuCuq4MLJVrRJY3BQ64hlC0CABBSAixFXpLwxTMN5h4BlS0lzRjvCcdkir7S9yj',
        "-F", 'name='+name, "-F", "description="+description, "-F", "prod_type=1"], stdout=subprocess.PIPE)

def upload_report(product_name, report):
    result = subprocess.run([
        "curl", "-X", 'POST', server + 'import-scan/',
        "-H", 'accept: application/json', "-H", 'Content-Type: multipart/form-data',
        "-H", 'Authorization: Token 5c3f5c0b517a7847f57ae03ca50f8dcfedfce3cd',
        "-H", 'X-CSRFTOKEN: UjuCuq4MLJVrRJY3BQ64hlC0CABBSAixFXpLwxTMN5h4BlS0lzRjvCcdkir7S9yj',
        "-F", 'active=true', "-F", 'verified=true', "-F", 'close_old_findings=true',
        "-F", 'engagement_name=' + product_name + '_August', "-F", 'deduplication_on_engagement=true',
        "-F", 'minimum_severity=Info', "-F", 'create_finding_groups_for_all_findings=true',
        "-F", 'product_name=' + product_name, "-F", 'file=@result.json;type=application/json',
        "-F", 'auto_create_context=true', "-F", 'scan_type=Anchore Grype'], stdout=subprocess.PIPE)
    logging.info("Successfully uploaded to defect dojo")