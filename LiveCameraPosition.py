import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO

#Avg line width = 151 pixels

#downsample
#gaussian blur
#Hough Lines vs. HoughlinesP
#Links

height = 480
width = 640
servoPIN = 18
time.sleep(.1)
horiz_slope_thresh = 1
y = 300
h = 200
x = 200
w = 300

target = width/2
line_center = target

KP = .005  #1/encoder ticks per sample to start
KD = 0.0025
KI = 0

i_error = 0

min_steering = 7
max_steering = 8


def main():

    camera = PiCamera()
    resolution = (width, height)
    camera.resolution = resolution
    rawCapture = PiRGBArray(camera, size=resolution)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    servo = GPIO.PWM(servoPIN, 50)
    servo.start(6.5)

    y_t = 7.5
    error = 0
    i_error = 0
    now = time.time()
    prev_error = error
    last_time = now
    center = target

    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            start = time.time()
            img = frame.array
            now = time.time()
            processed_img = img_pre_proccess(img)
            after_image_process = time.time()
            edges = canny(processed_img)
            after_canny = time.time()
            all_lines = hough(edges)
            after_hough = time.time()

            if all_lines is not None:
                print("--------" + str(len(all_lines)) + " lines found!!--------")
                x_intercepts = filter_lines(all_lines)
                center = kmeans_clustering(x_intercepts)
                after_kmeans = time.time()
                img = draw_lines(all_lines, img)
                if center is not None:
                    img = draw_center(center, height, img)
                    prev_error = error
                    error = target - center
            else:
                print("----------No Lines Found!------------")
                after_kmeans = time.time()

            rawCapture.truncate(0)

            dt = now - last_time
            y_t = pid_control(error, prev_error, i_error, dt, y_t)
            adjust_steering(servo, y_t)
            last_time = now

            total_time = after_kmeans - start
            img_read_time = after_image_process - start
            Hough_time = after_hough - after_image_process
            Kmeans_time = after_kmeans - after_hough
            
            print(error)


            #print("Total time: " + str(round(total_time,5)))
            #print("\nImage Read time: " + str(round(img_read_time, 5)))
            #print("Hough time: " + str(round(Hough_time, 5)))
            #print("K-Means time: " + str(round(Kmeans_time, 5)))
            #print("\n\n")
        
            #plt.imshow(img, cmap="gray")
            #plt.show()

    except KeyboardInterrupt:
        rawCapture.truncate(0)
        servo.stop()
        GPIO.cleanup()


def pid_control(error, prev_error, i_error, dt, y_t):

    p_error = error
    i_error += error * dt
    d_error = (error - prev_error) / dt

    p_out = error*KP
    i_out = i_error*KI
    d_out = d_error*KD

    y_t += p_out + i_out + d_out
    y_t = max(min(max_steering, y_t), min_steering)
    return(y_t)


def img_pre_proccess(img):

    crop_img = img[y:y+h, x:x+w]    #Crop to only look at the bottom center
    hls = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HLS) #Convert to HLS
    Lchannel = hls[:,:,1]   #Look at only L channel
    mask = cv2.inRange(Lchannel, 180, 255)      #Get rid of pixels with L<180
    return(mask)


def canny(mask):

    edges = cv2.Canny(mask, 100, 200)       #Canny Edge detection
    return(edges)


def hough(edges):

    rho = 1
    angle = np.pi/180
    min_thresh = 50
    lines = cv2.HoughLinesP(edges,rho,angle,min_thresh,minLineLength=8,maxLineGap=20)
    return(lines)


def filter_lines(lines):

    i = 0
    X = np.array([])
    while i < len(lines):   #For all the lines found
        for x1,y1,x2,y2 in lines[i]:
            m = ((y2+y)-(y1+y))/((x2+x)-(x1+x))     #Compute Slope
            if m == float("inf") or m == float("-inf"):     #Check for inf slope
                x_intercept = (x1+x2)/2 + x
            else:   
                b = (y2+y)-m*(x2+x)
                x_intercept = (height-b)/m 
            if abs(m) > horiz_slope_thresh: # if line is close to vertical
                X = np.append(X, [x_intercept])
        i+=1
    return(X)


def kmeans_clustering(X):

    if (X.size > 1):            #Kmeans Clustering
        X = X.reshape(-1, 1)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        clusters = kmeans.cluster_centers_
        diff = abs(clusters[0] - clusters[1])
        if clusters[0] > clusters[1]:
            line_center = clusters[0] - diff/2
        else:
            line_center = clusters[0] + diff/2
        return(line_center)
    else:
        return None


def draw_lines(lines, img):

    i = 0
    while i < len(lines):   #For all the lines found
        for x1,y1,x2,y2 in lines[i]:
            m = ((y2+y)-(y1+y))/((x2+x)-(x1+x))     #Compute Slope
            if abs(m) > horiz_slope_thresh:             # if line is vertical
                cv2.line(img,(x1+x,y1+y),(x2+x,y2+y),(255,0,0),3) #Draw line
        i+=1
    return(img)
 

def draw_center(line_center, height, img):

    cv2.line(img,(line_center,height),(line_center,(height-100)),(66,21,74),6)
    return(img)


def adjust_steering(servo, duty_cycle):

    servo.ChangeDutyCycle(duty_cycle)


if __name__=="__main__":
    main()

