import sys
import pdb
from time import sleep
from logging import INFO

from vnpy.event import EventEngine
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine

from vnpy.gateway.huobif import HuobifGateway
from vnpy.app.cta_strategy import CtaStrategyApp
from vnpy.app.cta_strategy.base import EVENT_CTA_LOG
from vnpy.trader.object import SubscribeRequest
from vnpy.trader.constant import Exchange

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True

default_setting = {
    "API Key": "2be6e594-12edb3eb-rfhfg2mkl3-74a68",
    "Secret Key": "f3084214-4652d4fd-882f8eb2-b0256",
    "会话数": 3,
    "代理地址": "",
    "代理端口": "",
}

ExchangeName = 'HUOBIF'


def run():
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    # sub = SubscribeRequest('FIL210625', Exchange.HUOBI)

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(HuobifGateway)
    cta_engine = main_engine.add_app(CtaStrategyApp)
    main_engine.write_log("主引擎创建成功")

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")

    main_engine.connect(default_setting, ExchangeName)
    main_engine.write_log("连接接口")

    sleep(10)
    # main_engine.subscribe(sub, "HUOBIF")
    policy = 'test'
    cta_engine.init_engine()
    main_engine.write_log("策略初始化完成")
    # test_strategy
    cta_engine.init_all_strategies()
    sleep(10)   # Leave enough time to complete strategy initialization
    main_engine.write_log("策略全部初始化")

    # pdb.set_trace()
    cta_engine.start_strategy(policy)
    main_engine.write_log("策略全部启动")

    while True:
        sleep(10)
        print("进程存活")


if __name__ == "__main__":
    run()
