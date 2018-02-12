from apscheduler.schedulers.background import BackgroundScheduler

import global_variable

_scheduler = None

def set_scheduler(sched):
    global _scheduler
    _scheduler = sched


def get_scheduler():
    global _scheduler

    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        set_scheduler(_scheduler)
    return _scheduler


def process_reserve():
    print("예약 목록 : ", global_variable.get_reserve_list())
    for reserve in global_variable.get_reserve_list():
        remain_min = reserve.check()
        if remain_min:
            reserve.alert_to_user(remain_min)
            global_variable.get_reserve_list().remove(reserve)

