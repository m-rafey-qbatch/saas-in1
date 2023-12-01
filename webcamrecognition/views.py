from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
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

from socialmedia.models import Unit

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

            # Add this line to print the first 100 characters of base64_img
            print("[DEBUG] base64_img (before):", base64_img[:100])

            # Split the base64 image data
            base64_img = base64_img.split(',')[1]

            # Add this line to print the first 100 characters of base64_img (after splitting)
            print("[DEBUG] base64_img (after):", base64_img[:100])

            img_data = base64.b64decode(base64_img)
            frame = Image.open(BytesIO(img_data))
            
            # Convert to RGB and to a numpy array
            frame_rgb = np.array(frame.convert('RGB'))

            # Resize frame for faster face recognition processing (to 1/4)
            small_frame = cv2.resize(frame_rgb, (0, 0), fx=0.25, fy=0.25)
            face_encodings = face_recognition.face_encodings(small_frame)

            recognized_faces = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(all_known_encodings, face_encoding)
                best_match_index = np.argmin(face_recognition.face_distance(all_known_encodings, face_encoding))
                if matches[best_match_index]:
                    recognized_user = User.objects.get(username=all_known_names[best_match_index])
                    session.recognized_user = recognized_user
                    session.recognized = True
                    session.face_recognized = True
                    session.save()
                    recognized_faces.append(recognized_user.username)

            if recognized_faces:
                messages.success(request, f"Faces recognized: {', '.join(recognized_faces)}!")
            else:
                messages.info(request, "No faces recognized.")

            return redirect('recognition_log_view')
        else:
            print("[ERROR] Invalid form submission:", form.errors)
            messages.error(request, "Invalid form submission.")
    else:
        form = WebcamSessionForm()

    return render(request, 'webcamrecognition/attendance.html', {'form': form})


def recognition_log_view(request):
    # Fetch the most recent recognized session initiated by the super admin
    session = WebcamSession.objects.select_related('user').filter(user=request.user, face_recognized=True).order_by('-start_timestamp').first()

    unit_choices = dict(Unit.UNIT_CHOICES)  # Create a dictionary from choices for quick look-up

    if session:
        session.display_name = unit_choices.get(session.name, session.name)
    else:
        session = None

    return render(request, 'webcamrecognition/recognition_log.html', {'session': session})
