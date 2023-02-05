from flask import Flask, Response
import matplotlib.pyplot as plt
import io
import base64
import os
#os.environ['FLASK_ENV'] = 'production'


app = Flask(__name__)

@app.route('/')
def index():
    op1 = 4992000
    # line 1 points
    fig = plt.figure()
    x1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    y1 = [4992000,2518000,1776000,1337000,1115000,966000,860000,780000,718000,669000,628000,595000,0,0,520000]
    for num,u in enumerate(y1):
        y = (u*x1[num]/op1)-1
        print(x1[num])
        if y < 0:
            y = None
        y1[num] = y
    print(y1)
    # plotting the line 1 points
    plt.plot(x1, y1, label = "line 1")

    op2 = 1815000
    # line 1 points
    #fig = plt.figure()
    x2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    y2 = [1815000,1071000,745000,567000,460000,378000,344000,303000,271000,246000,225000,207000,195000,184000,174000,169000,163000,156000]
    for num,u in enumerate(y2):
        y = (u*x2[num]/op2)-1
        print(x2[num])
        if y < 0:
            y = None
        y2[num] = y
    print(y2)
    # plotting the line 1 points
    plt.plot(x2, y2, label = "line 2")

    op3 = 3710000
    # line 1 points
    #fig = plt.figure()
    x3 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    y3 = [3710000,0,0,0,0,745000,0,0,0,0,0,465000,0,0,0,395000]
    for num,u in enumerate(y3):
        y = (u*x3[num]/op3)-1
        print(x3[num])
        if y < 0:
            y = 0
        y3[num] = y
    print(y3)
    # plotting the line 1 points
    plt.plot(x3, y3, label = "line 3")

    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    # giving a title to my graph
    plt.title('Two lines on same graph!')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()

    # Convert the figure to a PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_data = buf.read()

    return Response(image_data, content_type='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

