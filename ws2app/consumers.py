from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import *
from channels.db import database_sync_to_async

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
  
        print("Websocket Connected...", event)
        self.group_name = (self.scope['url_route']['kwargs']['group_name'])
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        
        self.send({
            'type' : 'websocket.accept'
        })

   

    def websocket_receive(self,event):

        print("Websocket Recieve...", event)
        data = json.loads(event['text'])
        print(data)
        user= self.scope['user']
        data['user'] = user.username
        gr_name = Group.objects.get(name = self.group_name)

        if user.is_authenticated:

            ch_name = Chat(content = data['msg'], room = gr_name, is_online = True)
            ch_name.save()
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type' : 'chat.messege',
                'messege' : json.dumps(data),
            })

        else:

            self.send({
                'type' : "websocket.send",
                'text' : json.dumps({
                    "msg" : "Login Required",
                })
            })


    def chat_messege(self, event):
        print(event)
        self.send({
            'type' : 'websocket.send',
            'text' : event['messege']
        })


    def websocket_disconnect(self,event):
        print("Websocket DisConnected...", event)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        
        raise StopConsumer()
    

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print("Websocket Connected...", event)
        self.group_name = (self.scope['url_route']['kwargs']['group_name'])
        # self.user_name = (self.scope['url_route']['kwargs']['username'])
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # await self.channel_layer.group_send(self.group_name,{
        #     'type' : 'user.status',
        #     'status' : 'online',
        # })
        await self.send({
            'type' : 'websocket.accept'
        })
        
    # async def user_status(self, event):
    #     await self.send({
    #         'type' : 'websocket.send',
    #         'msgg' : event['status'],
    #     })

    async def websocket_receive(self,event):
        print("Websocket Recieve...", event)
        self.data = json.loads(event['text'])
        print(self.data)
        user= self.scope['url_route']['kwargs']['username']
        self.data['user'] = user
        self.data['status'] = 'online'
        gr_name = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        
        ch_name = Chat(content = self.
        data['msg'], room = gr_name, sender = user)
        await database_sync_to_async(ch_name.save)()
        await self.channel_layer.group_send(self.group_name, {
                'type' : 'chat.messege',
                'messege' : json.dumps(self.
                data),
        })

    async def chat_messege(self, event):
        print(event)
        await self.send({
            'type' : 'websocket.send',
            'text' : event['messege']
        })

    async def websocket_disconnect(self,event):
        print("Websocket DisConnected...", event)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()
    