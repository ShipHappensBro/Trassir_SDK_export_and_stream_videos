import requests
import json
from datetime import datetime
import webbrowser
import sys
start=datetime.now()
class app():
    def __init__(self,name:str,start_time:datetime,end_time:datetime) -> None:
        self.name=name
        self.start_time=start_time
        self.end_time=end_time

    def find_guid(self):
        
        urls=['127.0.0.1']
        
        postfix=':8080/objects/?password=' #Пароль
        port=':8080/'
        prefix='https://'

        prefix_stream='http://'
        port_stream=':555/'

        try:
            for elements in urls:
                full_adr=prefix+elements+postfix
                adr=prefix+elements+port
                streamadr=prefix_stream+elements+port_stream

                response=requests.get(full_adr,verify=False)
                into_json=json.dumps(response.json())
                info=json.loads(into_json)

                for elements in info:
                    if self.name==elements['name']:
                        self.guid=(elements['guid'])
                        self.currentadr=adr
                        self.streamadr=streamadr
                        break
        except:
            print(f'Error: Camera doesnt found{sys.exc_info()}')

    def export_video(self):
        try:

            if self.currentadr !='https://127.0.0.1:8080/' and 'https://127.0.0.2:8080/': # Используйте условие,если на некоторых регистраторах другой пароль
                sid_url="{adr}login?username=Admin&password=".format(adr=self.currentadr) #Пароль
                sid_response=requests.post(sid_url,verify=False)
                self.sid=json.loads(sid_response.text)["sid"]

            else:
                sid_url="{adr}login?username=Admin&password=".format(adr=self.currentadr) #Пароль
                sid_response=requests.post(sid_url,verify=False)
                self.sid=json.loads(sid_response.text)["sid"]

        except:
            print(f'Error: sid wasnt created{sys.exc_info()}')

        try:
            token_url=f'{self.currentadr}get_video?channel={self.guid}&container=mjpeg&stream=archive_main&sid={self.sid}'

            token_response=requests.get(token_url,verify=False)
            self.token=json.loads(token_response.text)["token"]
            get_stream_url=f'{self.streamadr}{self.token}'

            requests.get(get_stream_url,verify=False,stream=True)
            stream_url=f"{self.currentadr}archive_command?command=play&start={self.start_time}&stop={self.end_time}&speed=1&sid={self.sid}&token={self.token}"

        except:
            print(f'Token wasnt created {sys.exc_info()}')
        
        try:
            stream_response=requests.get(stream_url,verify=False,stream=True)
            first_frame=json.loads(stream_response.text)["first_frame_ts"]

            stream_url=f"{self.currentadr}archive_command?command=play&start={first_frame}&stop={self.end_time}&speed=1&sid={self.sid}&token={self.token}"
            stream_response=requests.get(stream_url,verify=False,stream=True)

            webbrowser.open(get_stream_url,new=0)

        except:
            print(f'Error: No frames {sys.exc_info()}')

if __name__=='__main__':
    main=app('КАМЕРА','2023-05-18 09:00:16','2023-05-18 10:00:00')
    main.find_guid()
    main.export_video()
    print(datetime.now()-start)