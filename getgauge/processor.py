import os
import sys
import time
import traceback

from connection import read_message, send_message
from messages.messages_pb2 import Message, StepValidateResponse
from messages.spec_pb2 import ProtoExecutionResult

from getgauge.registry import registry

PROJECT_ROOT_ENV = 'GAUGE_PROJECT_ROOT'
STEP_IMPL_DIR = "step_impl"
project_root = os.environ[PROJECT_ROOT_ENV]
impl_dir = os.path.join(project_root, STEP_IMPL_DIR)


def _current_time(): return int(round(time.time() * 1000))


def _validate_step(req, res, socket):
    res.messageType = Message.StepValidateResponse
    res.stepValidateResponse.isValid = registry.is_step_implemented(req.stepValidateRequest.stepText)
    if res.stepValidateResponse.isValid is False:
        res.stepValidateResponse.errorType = StepValidateResponse.STEP_IMPLEMENTATION_NOT_FOUND


def _execute_step(req, res, socket):
    params = []
    for param in req.executeStepRequest.parameters:
        params.append(param.value)
    set_response_values(req, res)
    execute_method(params, registry.get_info(req.executeStepRequest.parsedStepText).impl, res)


def set_response_values(request, response, s=None):
    response.messageType = Message.ExecutionStatusResponse
    response.executionStatusResponse.executionResult.failed = False
    response.executionStatusResponse.executionResult.executionTime = 0


def execute_method(params, func, response):
    start = _current_time()
    try:
        func(*params)
    except Exception as e:
        _add_exception(e, response)
    response.executionStatusResponse.executionResult.executionTime = _current_time() - start


def _add_exception(e, response):
    response.executionStatusResponse.executionResult.failed = True
    response.executionStatusResponse.executionResult.errorMessage = e.__str__()
    response.executionStatusResponse.executionResult.stackTrace = traceback.format_exc()
    response.executionStatusResponse.executionResult.errorType = ProtoExecutionResult.ASSERTION


def _kill_runner(req, res, socket):
    socket.close()
    sys.exit()


processors = {Message.ExecutionStarting: set_response_values,
              Message.ExecutionEnding: set_response_values,
              Message.SpecExecutionStarting: set_response_values,
              Message.SpecExecutionEnding: set_response_values,
              Message.ScenarioExecutionStarting: set_response_values,
              Message.ScenarioExecutionEnding: set_response_values,
              Message.StepExecutionStarting: set_response_values,
              Message.StepExecutionEnding: set_response_values,
              Message.ExecuteStep: _execute_step,
              Message.StepValidateRequest: _validate_step,
              Message.StepNamesRequest: set_response_values,
              Message.ScenarioDataStoreInit: set_response_values,
              Message.SpecDataStoreInit: set_response_values,
              Message.SuiteDataStoreInit: set_response_values,
              Message.StepNameRequest: set_response_values,
              Message.RefactorRequest: set_response_values,
              Message.KillProcessRequest: _kill_runner,
              }


def dispatch_messages(socket):
    sys.path.append(impl_dir)
    map(__import__, ['step_impl'])
    while True:
        request = read_message(socket)
        response = Message()
        processors[request.messageType](request, response, socket)
        send_message(response, request, socket)
