import requests
import json
import shutil
from datetime import datetime,timedelta
import subprocess
import sys

start=datetime.now()

class app():
    def __init__(self,name:str,start_time:datetime,end_time:datetime) -> None:
        self.name=name
        self.iso_start=datetime.fromisoformat(start_time)+timedelta(hours=3)
        self.unix_start=str(int(self.iso_start.timestamp()))+'000000'
        self.iso_end=datetime.fromisoformat(end_time)+timedelta(hours=3)
        self.unix_end=str(int(self.iso_end.timestamp()))+'000000'
        self.start_time=self.unix_start
        self.end_time=self.unix_end
        
    def find_guid(self):
        
        urls=['127.0.0.1'] #URL регистраторов
        postfix='objects/?password=' #Пароль
        prefix='https://'
        
        for elements in urls:

            full_adr=prefix+elements+postfix
            adr=prefix+elements

            response=requests.get(full_adr,verify=False)
            into_json=json.dumps(response.json())
            info=json.loads(into_json)

            for elements in info:
                if self.name==elements['name']:

                    self.guid=(elements['guid'])
                    self.currentadr=adr
                    print(self.guid)

                    break
                    
                     
    def export_video(self):
        try:
            sid_url="{adr}login?password=".format(adr=self.currentadr) #Пароль
            sid_response=requests.post(sid_url,verify=False)
            self.sid=json.loads(sid_response.text)["sid"]
        except:
            print(f'ERROR: камера не найдена {sys.exc_info()}')
            print(sid_response.text)
        try:
            create_task_url="{adr}jit-export-create-task?sid={sid}".format(adr=self.currentadr,sid=self.sid)
            guid=f'"{self.guid}"'
            create_task_parms=str('{"resource_guid": 'f"{guid}"',"start_ts": 'f"{self.start_time}"',"end_ts": 'f"{self.end_time}"',"is_hardware": 0,"prefer_substream": 0}')
            create_task_response=requests.post(create_task_url,data=create_task_parms,verify=False)
            self.task_id=json.loads(create_task_response.text)['task_id']
        except:
            print(f'ERROR {sys.exc_info}')
        try:

            export_download_url=f'{self.currentadr}jit-export-download?sid={self.sid}&task_id={self.task_id}'
            start=str(self.iso_start.strftime('%H.%M.%S'))
            end=str(self.iso_end.strftime('%H.%M.%S'))
            filename=f'{str(self.name)}({str(datetime.date(self.iso_start))}) {start}-{end}.mp4'

            with requests.get(export_download_url,verify=False,stream=True) as export_download:
                with open(f'C:\path\to\folder\{filename}','wb+') as file:
                    print(f'Экспорт файла {filename} ...')
                    shutil.copyfileobj(export_download.raw,file)
                    print('Экспорт успешно выполнен')
                    subprocess.Popen(r'explorer /select,"C:\path\to\folder\"')
        except:
            print(f'error {sys.exc_info()}') 
        
if __name__=='__main__':
    main=app('V3.3.13  16-17 проезд','2023-05-20 12:25:00','2023-05-20 12:50:00')
    main.find_guid()
    main.export_video()
    print(datetime.now()-start)