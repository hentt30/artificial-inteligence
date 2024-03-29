from keras.models import load_model
import cv2
import numpy as np
from utils import sigmoid


class YoloDetector:
    """
    Represents an object detector for robot soccer based on the YOLO algorithm.
    """
    def __init__(self, model_name, anchor_box_ball=(5, 5), anchor_box_post=(2, 5)):
        """
        Constructs an object detector for robot soccer based on the YOLO algorithm.

        :param model_name: name of the neural network model which will be loaded.
        :type model_name: str.
        :param anchor_box_ball: dimensions of the anchor box used for the ball.
        :type anchor_box_ball: bidimensional tuple.
        :param anchor_box_post: dimensions of the anchor box used for the goal post.
        :type anchor_box_post: bidimensional tuple.
        """
        self.network = load_model(model_name + '.hdf5')
        self.network.summary()  # prints the neural network summary
        self.anchor_box_ball = anchor_box_ball
        self.anchor_box_post = anchor_box_post

    def detect(self, image):
        """
        Detects robot soccer's objects given the robot's camera image.

        :param image: image from the robot camera in 640x480 resolution and RGB color space.
        :type image: OpenCV's image.
        :return: (ball_detection, post1_detection, post2_detection), where each detection is given
                by a 5-dimensional tuple: (probability, x, y, width, height).
        :rtype: 3-dimensional tuple of 5-dimensional tuples.
        """
        # Todo: implement object detection logic
        ball_detection = (0.0, 0.0, 0.0, 0.0, 0.0)  # Todo: remove this line
        post1_detection = (0.0, 0.0, 0.0, 0.0, 0.0)  # Todo: remove this line
        post2_detection = (0.0, 0.0, 0.0, 0.0, 0.0)  # Todo: remove this line
        image_array = self.preprocess_image(image)
        output = self.network.predict(image_array)
        ball_detection,post1_detection,post2_detection = self.process_yolo_output(output)
        return ball_detection, post1_detection, post2_detection

    def preprocess_image(self, image):
        """
        Preprocesses the camera image to adapt it to the neural network.

        :param image: image from the robot camera in 640x480 resolution and RGB color space.
        :type image: OpenCV's image.
        :return: image suitable for use in the neural network.
        :rtype: NumPy 4-dimensional array with dimensions (1, 120, 160, 3).
        """
        # Todo: implement image preprocessing logic
        image = cv2.resize(image,(160,120),interpolation = cv2.INTER_AREA)
        image = np.array(image)
        image = image/255
        image = np.reshape(image,(1,120,160,3))
        return image

    def process_yolo_output(self, output):
        """
        Processes the neural network's output to yield the detections.

        :param output: neural network's output.
        :type output: NumPy 4-dimensional array with dimensions (1, 15, 20, 10).
        :return: (ball_detection, post1_detection, post2_detection), where each detection is given
                by a 5-dimensional tuple: (probability, x, y, width, height).
        :rtype: 3-dimensional tuple of 5-dimensional tuples.
        """
        coord_scale = 4 * 8  # coordinate scale used for computing the x and y coordinates of the BB's center
        bb_scale = 640  # bounding box scale used for computing width and height
        output = np.reshape(output, (15, 20, 10))  # reshaping to remove the first dimension
        # Todo: implement YOLO logic
   
        ball_prob = 0
        post1_prob = 0
        post2_prob = 0 
        cord_ball = np.array([0,0]) 
        cord_post1 = np.array([0,0]) 
        cord_post2 = np.array([0,0])


        for i in range(15):
            for j in range(20):
               
                prob_ball = sigmoid(output[i][j][0])
                prob_post = sigmoid(output[i][j][5])
                if prob_ball >ball_prob:
                    ball_prob = prob_ball
                    cord_ball[0] = i
                    cord_ball[1] = j
               
                if prob_post > min(post1_prob,post2_prob):
                    if  post1_prob > post2_prob:
                        if prob_post > post1_prob:
                            post2_prob = post1_prob
                            post1_prob = prob_post
                            cord_post2[0] = cord_post1[0]
                            cord_post2[1] = cord_post1[1]
                            cord_post1[0] = i
                            cord_post1[1] = j
                           
                        else:
                           post2_prob = prob_post
                           cord_post2[0] = i
                           cord_post2[1] = j
                         
                    else:
                        if prob_post > post2_prob:
                            post1_prob = post2_prob
                            post2_prob = prob_post
                            cord_post1[0] = cord_post2[0]
                            cord_post1[1] = cord_post2[1]
                            cord_post2[0] = i
                            cord_post2[1] = j
                           
                        else:
                           post1_prob = prob_post
                           cord_post1[0] = i
                           cord_post1[1] = j
                           

        x_ball = (cord_ball[1]+ sigmoid(output[cord_ball[0]][cord_ball[1]][1]))*coord_scale
        y_ball = (cord_ball[0]+ sigmoid(output[cord_ball[0]][cord_ball[1]][2]))*coord_scale
        w_ball = bb_scale*5*np.exp(output[cord_ball[0]][cord_ball[1]][3])
        h_ball = bb_scale*5*np.exp(output[cord_ball[0]][cord_ball[1]][4])
        ball_detection = (ball_prob, x_ball, y_ball, w_ball, h_ball)
        x_post = (cord_post1[1]+ sigmoid(output[cord_post1[0]][cord_post1[1]][6]))*coord_scale
        y_post = (cord_post1[0]+ sigmoid(output[cord_post1[0]][cord_post1[1]][7]))*coord_scale
        w_post = bb_scale*2*np.exp(output[cord_post1[0]][cord_post1[1]][8])
        h_post = bb_scale*5*np.exp(output[cord_post1[0]][cord_post1[1]][9])  
        post1_detection = (post1_prob, x_post, y_post, w_post, h_post)  
        x_post2 = (cord_post2[1]+ sigmoid(output[cord_post2[0]][cord_post2[1]][6]))*coord_scale
        y_post2 = (cord_post2[0]+ sigmoid(output[cord_post2[0]][cord_post2[1]][7]))*coord_scale
        w_post2 = bb_scale*2*np.exp(output[cord_post2[0]][cord_post2[1]][8])
        h_post2 = bb_scale*5*np.exp(output[cord_post2[0]][cord_post2[1]][9])  
        post2_detection = (post2_prob, x_post2, y_post2, w_post2, h_post2)
        

        return ball_detection, post1_detection, post2_detection
