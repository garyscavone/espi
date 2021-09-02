from pypylon import pylon
from pypylon import genicam
import cv2
import tkinter as tk

# code from/based off: https://github.com/drscotthawley/image-capture-opencv/blob/master/capture.py


camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# camera needs to be opened to asjust the settings
camera.Open()

# must be smaller than or equal 0.999969
camera.BslBrightness.SetValue(0)
camera.BslContrast.SetValue(0)

# hue and saturation automatic values
camera.BslSaturation.SetValue(1)
camera.BslHue.SetValue(0)


# Set the upper limit of the camera's frame rate
camera.AcquisitionFrameRateEnable.SetValue(True)
# fps will not go past 20, there are many factors that limit the value
camera.AcquisitionFrameRate.SetValue(20)

# variables for consecutive differencing, black and white, and live view. set to false to begin
c_sub=False
bw=False
l_view=False

# basic setters to change the settings
def changeBrightness(newB):
    camera.BslBrightness.SetValue(newB)

def changeContrast (newC):
    camera.BslContrast.SetValue(newC)

def changeFPS(newF):
    camera.AcquisitionFrameRate.SetValue(newF)

# newE is in microseconds
def changeExposure(newE):
    camera.ExposureTime.SetValue(newE)

def changeHue(newH):
    camera.BslHue.SetValue(newH)

def changeSaturation(newS):
    camera.BslSaturation.SetValue(newS)





# creating tkinter tab
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

# function that is called if the user selects consecutive differencing in color
def startC():
    global c_sub
    c_sub=True
    global l_view
    l_view=True
    root.destroy()

# function that is called if the user selects consecutive differencing in black and white
def startC2():
    global c_sub
    c_sub=True
    global bw
    bw=True
    global l_view
    l_view=True
    root.destroy()



# creates buttons

button1 = tk.Button(frame, 
                   text="Start consecutive differencing (in color)", fg="blue",command=startC)
button1.pack(side=tk.RIGHT)

button2 = tk.Button(frame, 
                   text="Start consecutive differencing (in black and white)", fg="blue",command=startC2)
button2.pack(side=tk.RIGHT)


root.mainloop()


# converts image to pixel format, either BGR or Mono16
converter = pylon.ImageFormatConverter()
if(bw):
    converter.OutputPixelFormat = pylon.PixelType_Mono16
else:
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


# creates tkinter tab and sliders for brightness, contrast, hue, saturation, exposure, and frame rate
usercontrols=tk.Tk()
b=tk.Scale(usercontrols, from_=0, to=99, label="brightness")
b.pack(side='right')
c=tk.Scale(usercontrols, from_=0, to=99, label="contrast")
c.pack(side='right')

h=tk.Scale(usercontrols, from_=-180, to=180, label="hue")
h.pack(side='right')
saturation=tk.DoubleVar()
saturation.set(1)
s=tk.Scale(usercontrols, from_=0, to=2, label="saturation", variable=saturation)
s.pack(side='right')

exposure=tk.DoubleVar()
exposure.set(0.1)
e=tk.Scale(usercontrols, from_=0.012, to=0.999, digits=4, resolution=0.001, label="exposure (seconds)", variable=exposure)
e.pack(side='right')

framerate=tk.DoubleVar()
framerate.set(2)
f=tk.Scale(usercontrols, from_=1, to=20, label="frame rate (fps)", variable=framerate)
f.pack(side='right')

# tkinter entry/button that gives user the ability to enter a value for the exposure
tk.Label(usercontrols, text="Exposure (in seconds)").pack()
e1=tk.Entry(usercontrols)
e1.pack()

def setE():
    exposure.set(float(e1.get()))

tk.Button(usercontrols, text="set", command=setE).pack()






# function from https://github.com/basler/pypylon/blob/master/samples/opencv.py
def get_img():
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    # once the image has successfully been taken
    if grabResult.GrabSucceeded():
        # convert the image to the correct format and save its data to a variable img1
        image = converter.Convert(grabResult)
        img1 = image.GetArray()

    # tell the camera to stop grabbing frames
    camera.StopGrabbing()

    # return the image
    return img1


# grabs the current image and sets the var prev to it
prev=get_img()


# main loop that continues to run after user chooses which consecutive differencing they want
while True:
    

    img=get_img()

    # updating the tkinter tab
    usercontrols.update()

    # if l_view is true then displays the live view in a tab labeled "live view"
    if(l_view):
        cv2.namedWindow('Live View', cv2.WINDOW_NORMAL)
        cv2.imshow('Live View', img)
        cv2.resizeWindow("Live View", 1000,1000)
        k = cv2.waitKey(1)
        if k == 27:
            break

    # if c_sub (var for consecutive differencing) is true then displays the consecutive differencing in a tab labeled "consecutive differencing"
    if(c_sub):
        current=img
        cv2.namedWindow('Consecutive Differencing', cv2.WINDOW_NORMAL)
        cv2.imshow('Consecutive Differencing', cv2.absdiff(current, prev))
        cv2.resizeWindow('Consecutive Differencing', 1000,1000)
        prev=current
        k = cv2.waitKey(1)
        if k == 27:
            break

    # updating parameters based off of slider values
    changeBrightness((b.get()*.01))
    changeContrast((c.get()*.01))
    changeHue(h.get())
    changeSaturation(s.get())
    changeFPS(f.get())
    changeExposure(e.get()*1000000)

    

# when the loop is broken (i.e. the user clicks the esc key) the camer is closed, windows are closed, and program is exited
camera.Close()
cv2.destroyAllWindows()
exit()
