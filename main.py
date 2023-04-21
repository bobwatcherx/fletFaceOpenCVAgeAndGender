from flet import *
import base64
import dlib
import math
import cv2


# INITIALIZE CAMERA
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predirector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# AND NOW ESTIMATE YOU AGE IN FACE CAM
def estimate_age(shape):
	eye_distance = math.sqrt((shape.part(45).x - shape.part(36).x)**2 + (shape.part(45).y - shape.part(36).y)** 2)

	# AND DETECT EYE
	age = eye_distance * 0.3
	return int(age)


# AND NOW ESTIMATE GENDER
def estimate_gender(shape):
	lip_distance = math.sqrt((shape.part(62).x - shape.part(66).x)**2 + (shape.part(62).y - shape.part(66).y)** 2)


	# AND DETECT EYE
	if lip_distance > 25:
		gender = "Male"
	else:
		gender = "Female"
	return gender


# AND NOW CREATE CLASS FLET 
class YouFace(UserControl):
	"""docstring for YouFace"""
	def __init__(self):
		super().__init__()
		# AND CREATE VARIABLE AGE AND GENDER 
		# FOR SHOW IN BOTTOM WEBCAM
		self.you_gender = Text("",
			size=30,weight="bold",color="white"
			)
		self.you_age = Text("",
			size=30,weight="bold",color="white"
			)
	# AND NOW LOAD update_timer() WHEN FLET RUn
	def did_mount(self):
		self.update_timer()

	def update_timer(self):
		# DETECT REALTIME EVERY 1 SECONDS
		while True:
			_,frame = cap.read()
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			rects = detector(gray,0)

			if len(rects) > 0:
				for rect in rects:
					x,y,w,h = rect.left(),rect.top(),rect.width(),rect.height()
					cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2)
					shape = predirector(gray,rect)

					age = estimate_age(shape)
					gender = estimate_gender(shape)

					# NOW ADD TEXT TO YOU FACE CAM
					cv2.putText(frame,f"Age: {age}",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
					cv2.putText(frame,f"GENDER: {gender}",(x,y+h+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

					# AND NOW SET SELF.age AND self.gender
					self.you_age.value  = age
					self.you_gender.value  = gender
					self.page.update()
			# AND IF NO FACE FOUND IN CAMERA THEN SHOW TEXT NO FOUND FACE
			else:
				cv2.putText(frame,"no face found",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

			_,im_arr = cv2.imencode(".png",frame)
			im_b64 = base64.b64encode(im_arr)
			self.img.src_base64 = im_b64.decode("utf-8")
			self.update()

	# NOW BUILD UI TEXT AND IMAGE FROM YOU FACE 
	def build(self):
		self.img = Image(
			border_radius = border_radius.all(20)
			)

		return Column([
			self.img,
			Row([
			Text("Gender : ",size=30,weight="bold",
				color="white"
				),
			self.you_gender

				]),
			Row([
			Text("Age : ",size=30,weight="bold",
				color="white"
				),
			self.you_age

				]),

			])

# NOW BUILD CONTAINER 
section = Container(
	margin = margin.only(bottom=40),
	content= Row([
		Card(
			elevation=30,
			content=Container(
				bgcolor="blue",
				padding=10,
				border_radius = border_radius.all(20),
				content=Column([
					Text("Face Cam FLET",
						size=30,weight="bold",
						color="white"
						),
					YouFace()

					])
				)
			)
		],alignment="center")
	)











def main(page:Page):
	page.padding = 50
	page.window_left = page.window_left + 100
	page.theme_mode = "light"

	page.add(
		section
		)

if __name__ == "__main__":
	flet.app(target=main)
	cap.release()
	cv2.destroyAllWindows()



