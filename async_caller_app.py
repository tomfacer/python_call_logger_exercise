from call_log import CallLog
from flask import Flask
from http import HTTPStatus
from timer import Timer
import uuid
import worker


APP_PORT = 8095
DEBUG = False
ROUTE = '/route'

app = Flask(__name__)
call_log = CallLog()


@app.route(ROUTE)
def endpoint():

    call_id = uuid.uuid4()
    make_call = make_call_check()

    timer = Timer()  # start timer

    if make_call:
        worker.work(call_log.sleep)
        call_log.increment_success_call_count()
        res = 'Processed {}'.format(call_id)
    else:
        call_log.increment_rejected_call_count()
        res = 'Skipping call {}'.format(call_id)

    timetaken = timer.get_elapsed_in_millis()
    call_log.add_to_queue(timetaken)

    print('Call serviced for {} in {} millis :: stats :: {}'.format(call_id, timetaken, call_log))

    if make_call:
        return res
    return res, HTTPStatus.TOO_MANY_REQUESTS



def make_call_check():
    return call_log.avg_call_duration < 2000


if __name__ == '__main__':
    app.run(debug=DEBUG, port=APP_PORT)