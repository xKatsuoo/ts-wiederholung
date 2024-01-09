from flask import Flask, request, make_response
import subprocess
import json
import logging

# logging
logger = logging.getLogger('server_logger')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('/home/ubuntu/myproject/server.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route("/healthz", methods=['GET'])
def healthz():
    logger.info('ip=%s method=%s scheme=%s path=%s', request.remote_addr, request.method, request.scheme, request.full_path)
    resp = make_response('OK')
    return resp

@app.route("/service/latency_check", methods=['GET'])
def latency_check_status():
    logger.info('ip=%s method=%s scheme=%s path=%s', request.remote_addr, request.method, request.scheme, request.full_path)
    result = subprocess.run(["/usr/bin/systemctl", "status", "--user", "latency_check.service"], capture_output=True)
    logger.info("returncode="+str(result.returncode))
    if result.returncode != 0 and result.returncode != 3: # rc=3 => unit not active 
        obj = { "success": False, "message": result.stderr.decode("utf-8", "ignore") }
    else: 
        obj = { "success": True, "message": result.stdout.decode("utf-8", "ignore") }
    logger.debug("message="+obj["message"])
    resp = make_response(json.dumps(obj, indent=4))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/service/latency_check/start", methods=['GET'])
def latency_check_start():
    logger.info('ip=%s method=%s scheme=%s path=%s', request.remote_addr, request.method, request.scheme, request.full_path)
    result = subprocess.run(["/usr/bin/systemctl", "start", "--user", "latency_check.service"], capture_output=True)
    logger.info("returncode="+str(result.returncode))
    if result.returncode != 0:
        obj = { "success": False, "message": result.stderr.decode("utf-8", "ignore") }
    else: 
        obj = { "success": True, "message": result.stdout.decode("utf-8", "ignore") }
    
    if obj["message"] != "":
        logger.debug("message="+obj["message"])

    resp = make_response(json.dumps(obj, indent=4))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/service/latency_check/stop", methods=['GET'])
def latency_check_stop():
    logger.info('ip=%s method=%s scheme=%s path=%s', request.remote_addr, request.method, request.scheme, request.full_path)
    result = subprocess.run(["/usr/bin/systemctl", "stop", "--user", "latency_check.service"], capture_output=True)
    logger.info("returncode="+str(result.returncode))
    if result.returncode != 0:
        obj = { "success": False, "message": result.stderr.decode("utf-8", "ignore") }
    else: 
        obj = { "success": True, "message": result.stdout.decode("utf-8", "ignore") }
    
    if obj["message"] != "":
        logger.debug("message="+obj["message"])

    resp = make_response(json.dumps(obj, indent=4))
    resp.headers['Content-Type'] = 'application/json'
    return resp
