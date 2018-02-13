import time
import websocket
import json

import schedule
import global_variable
import core


if __name__ == '__main__':

    if global_variable.get_slacker().rtm.connect():
        response=global_variable.get_slacker().rtm.start()
        sock_endpoint=response.body['url']
        slack_socket=websocket.create_connection(sock_endpoint)

        scheduler = schedule.get_scheduler()
        scheduler.start()
        schedule.set_scheduler(scheduler)
        schedule.get_scheduler().add_job(
            func=schedule.process_reserve,
            trigger='interval',
            seconds=30
        )

        while True:
            msg = json.loads(slack_socket.recv())

            if(len(msg)>0):
                res=core.parse_msg(msg)
                if(res is not None):
                    global_variable.get_slacker().chat.post_message(channel=msg['channel'],text=res,username="bus bot")

            time.sleep(1)

    else:
        print("connect fail")
