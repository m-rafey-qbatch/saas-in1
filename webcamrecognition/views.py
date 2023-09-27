from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WebcamSessionForm
from .models import WebcamSession
from users.models import UserFaceEncoding
from django.http import HttpResponseForbidden
import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import cv2

@login_required
def webcam_recognition_view(request):
    print("[INFO] Entered webcam_recognition_view")

    # Ensure only superusers access this
    if not request.user.is_superuser:
        return HttpResponseForbidden("Forbidden")

    # Handle POST requests
    if request.method == 'POST':
        form = WebcamSessionForm(request.POST)
        print("[INFO] Handling POST request")
        if form.is_valid():
            print("[INFO] Form is valid")
            
            # Create a new webcam session with a start timestamp
            session = WebcamSession.objects.create(user=request.user, name=form.cleaned_data['name'])

            all_known_encodings = []
            all_known_names = []

            for encoding_record in UserFaceEncoding.objects.all():
                user_encoding = np.frombuffer(encoding_record.face_encoding, dtype=np.float64)
                all_known_encodings.append(user_encoding)
                all_known_names.append(encoding_record.user.username)  # Assuming user is a ForeignKey to User model



            base64_img = request.POST.get('base64Image')
            if not base64_img:
                print("[ERROR] No base64 image received") 
                messages.error(request, "No image data received. Please capture an image before submitting.")
                return render(request, 'webcamrecognition/attendance.html', {'form': form})
            base64_img = base64_img.split('base64,')[1]

            img_data = base64.b64decode(base64_img)
            frame = Image.open(BytesIO(img_data))
            
            # Convert to RGB and to numpy array
            frame_rgb = np.array(frame.convert('RGB'))

            # Resize frame for faster face recognition processing (to 1/4)
            small_frame = cv2.resize(frame_rgb, (0, 0), fx=0.25, fy=0.25)
            face_encodings = face_recognition.face_encodings(small_frame)

            recognized_faces = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(all_known_encodings, face_encoding)
                best_match_index = np.argmin(face_recognition.face_distance(all_known_encodings, face_encoding))
                if matches[best_match_index]:
                    recognized_faces.append(all_known_names[best_match_index])

            if recognized_faces:
                session.recognized = True
                session.save()
                messages.success(request, f"Faces recognized: {', '.join(recognized_faces)}!")
                return redirect('recognition_log_view')
            else:
                messages.info(request, "No faces recognized.")
        else:
            print("[ERROR] Invalid form submission:", form.errors)
            messages.error(request, "Invalid form submission.")
    else:
        form = WebcamSessionForm()

    return render(request, 'webcamrecognition/attendance.html', {'form': form})



def recognition_log_view(request):
    sessions = WebcamSession.objects.all().order_by('-start_timestamp')  # This orders by newest sessions first based on their start time.
    return render(request, 'webcamrecognition/recognition_log.html', {'sessions': sessions})