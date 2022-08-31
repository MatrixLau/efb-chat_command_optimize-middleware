from doctest import master
from multiprocessing.connection import wait
from typing import Optional

from ehforwarderbot import Middleware, Message, coordinator
from ehforwarderbot.message import MsgType
from ehforwarderbot.types import ModuleID, InstanceID


class MatrixLauMiddleware(Middleware):

    """
    EFB Middleware - Chat Command Optimize Middleware
    """

    middleware_id: ModuleID = ModuleID(
        "chatCommandOptimize.MatrixLauMiddleware")
    middleware_name: str = "Chat Command Optimize Middleware"
    __version__: str = '1.0.0'

    def __init__(self, instance_id: Optional[InstanceID] = None):
        global chat_command_optimize_flag
        chat_command_optimize_flag = False

        super().__init__(instance_id)

    def process_message(self, message: Message) -> Optional[Message]:
        global chat_command_optimize_flag
        chat_command = '/chat_o'
        chat_cancel_command = '/chat_cancel'

        if message.text.startswith(chat_command):
            if message.vendor_specific.get('chat_command_optimize',0) == 1:
                return message
            name = message.text.replace(chat_command, '')
            name = name.replace(' ', '')
            if name == '':
                self.channel = coordinator.master
                coordinator.master.bot_manager.send_message(self.channel.config['admins'][0], '🔍请输入名字进行搜索\n输入__/chat_cancel__取消检索')
                chat_command_optimize_flag = True
            return None

        if message.text.startswith(chat_cancel_command):
            if chat_command_optimize_flag:
                chat_command_optimize_flag = False
                # message_alert = Message(
                #     deliver_to=coordinator.master,
                #     text='⚠已取消检索！'
                # )
                # coordinator.send_message(message_alert)
                self.channel = coordinator.master
                coordinator.master.bot_manager.send_message(self.channel.config['admins'][0], '⚠已取消检索！')
            else:
                # message_alert = Message(
                #     deliver_to=coordinator.master,
                #     text='⚠未开启检索\n请输入__/chat__开启检索'
                # )
                # coordinator.send_message(message_alert)
                self.channel = coordinator.master
                coordinator.master.bot_manager.send_message(self.channel.config['admins'][0], '⚠未开启检索\n请输入__/chat__开启检索')
            return None

        if chat_command_optimize_flag:
            if type(message.author).__name__ != 'SelfChatMember':
                return message
            name = message.text
            if name == '`':
                message.text = '/chat'
                message.vendor_specific['chat_command_optimize'] = 1
            else:
                message.text = '/chat ' + name
                chat_command_optimize_flag = False
            return message

