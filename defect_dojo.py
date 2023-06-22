import logging
import requests
import subprocess

# token is for a localhost DD deployment, so it's fine to commit
headers = {'content-type': 'application/json', 'Authorization': 'Token 5c3f5c0b517a7847f57ae03ca50f8dcfedfce3cd'}
server = "http://localhost:8081/api/v2"
def check_product_exists(product_name):
    result = requests.get('http://localhost:8081/api/v2/products/?name=' + product_name, verify=False, headers=headers)
    if result.status_code == 200:
        return True
    return False

def create_product(name, description):
    data = {
            'name': name,
            'description': description,
            'prod_type': 1,
        'lifecycle': None
        }

    logging.debug(requests.post(server + '/products/', data=data, headers=headers, verify=False))

def upload_report(product_name, report):
    result = subprocess.run([
        "curl", "-X", 'POST', 'http://localhost:8081/api/v2/import-scan/',
        "-H", 'accept: application/json', "-H", 'Content-Type: multipart/form-data',
        "-H", 'Authorization: Token 5c3f5c0b517a7847f57ae03ca50f8dcfedfce3cd',
        "-H", 'X-CSRFTOKEN: UjuCuq4MLJVrRJY3BQ64hlC0CABBSAixFXpLwxTMN5h4BlS0lzRjvCcdkir7S9yj',
        "-F", 'active=true', "-F", 'verified=true', "-F", 'close_old_findings=true',
        "-F", 'engagement_name=Demo', "-F", 'deduplication_on_engagement=true',
        "-F", 'minimum_severity=Info', "-F", 'create_finding_groups_for_all_findings=true',
        "-F", 'product_name=centos7', "-F", 'file=@result.json;type=application/json',
        "-F", 'auto_create_context=true', "-F", 'scan_type=Anchore Grype'], stdout=subprocess.PIPE)
    logging.info("Successfully uploaded to defect dojo")
