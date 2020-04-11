import numpy as np
import cv2
import socket
import pyautogui

speed=5

low=np.array([101,105,84])
high=np.array([120,255,255])

class VideoStreamingTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.bind(('', port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            prev_x=0
            prev_y=0
            prev_area=0
            pyautogui.FAILSAFE = False
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #image=cv2.flip(image,0)

                    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
                    mask=cv2.inRange(hsv,low,high)
                    blur=cv2.GaussianBlur(mask,(15,15),0)
                    _,contours,_=cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

                    for contour in contours:                       
                        area=cv2.contourArea(contour)
                        if area>1000:                            
                            x,y,w,h = cv2.boundingRect(contour)
                            d_x=x-prev_x
                            d_y=y-prev_y
                            if(abs(d_x)<10):
                                d_x=0
                            if(abs(d_y)<10):
                                d_y=0
                            prev_x=x
                            prev_y=y
                            if(area<=3000 and prev_area>=3000):
                                print("leftclick")
                                pyautogui.click()
                            else:    
                                pyautogui.moveRel(speed*d_x,speed*d_y)
                            prev_area=area                            
                            cv2.drawContours(image,contour,-1,(255,0,0),3)
                    cv2.imshow('frame',image) #display image
    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = "192.168.1.100", 8000
    VideoStreamingTest(h, p)

cv2.destroyAllWindows()



