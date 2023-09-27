import os
import secrets
import tempfile
import imghdr
import ipfshttpclient
import pilgram
import PIL.Image
import base64
import io
import w3storage
import face_recognition
from cv2 import *
import segno
import geoip2.database
import json
import requests
import numpy as np



from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, get_backends, authenticate
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core.files.images import ImageFile
from django.http import JsonResponse

from .forms import RegisterForm, LoginForm, UpdateUserForm, PersonalProfileForm, NFTMintForm

from PIL import Image, ImageDraw

from dotenv import load_dotenv
from .models import NFT, Wallet, PersonalProfile, WebCamUser, QRScanEvent, UserFaceEncoding

from thirdweb import ThirdwebSDK
from thirdweb.types import SDKOptions, GasSettings, GasSpeed
from eth_account import Account
from thirdweb.types.nft import NFTMetadataInput
from thirdweb.types import SDKOptions

from users.forms import NFTMintForm
from web3 import Web3

from django.core.files.uploadedfile import SimpleUploadedFile
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from urllib3.exceptions import ProtocolError

from html2image import Html2Image
from django.contrib.auth.decorators import login_required, user_passes_test





def home(request):
    return render(request, 'users/home.html')

def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully Created for {username}!')

            # Specify the authentication backend
            user.backend = get_backends()[0].__class__.__module__ + '.' + get_backends()[0].__class__.__name__
            
            # Log in the user
            login(request, user)
            
            # Redirect the user to the create_profile page
            return redirect('mint_nft_view')

        return render(request, self.template_name, {'form': form})
    

# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)




def face_login(request):
    if request.method == 'POST':
        # Decode the Base64 image from webcam or other source
        base64_img = request.POST.get('base64Image').split('base64,')[1]
        img_data = base64.b64decode(base64_img)
        uploaded_image = ImageFile(BytesIO(img_data), name="captured_image.png")

        # Don't save the image right away
        # photo = WebCamUser(user=request.user, webcam_image=image)
        # photo.save()

        try:
            user = User.objects.get(email=request.POST.get('email'))  # Get the user by email
            verified_photo = user.nft.image
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return render(request, 'users/face_login.html')
        except NFT.DoesNotExist:
            messages.error(request, "No NFT image found for comparison. Please contact support.")
            return render(request, 'users/face_login.html')

        try:
            uploaded_image_data = face_recognition.load_image_file(uploaded_image)
            uploaded_encodings = face_recognition.face_encodings(uploaded_image_data)

            if not uploaded_encodings:
                messages.error(request, "No face detected in the uploaded image.")
                return render(request, 'users/face_login.html')

            # Load the saved image for the user and get its encoding
            user_image_data = face_recognition.load_image_file(verified_photo.path)
            user_encodings = face_recognition.face_encodings(user_image_data)

            # Compare the encodings
            results = face_recognition.compare_faces(user_encodings, uploaded_encodings[0])
            if results and results[0]:
                login(request, user)
                return redirect('profile_home')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'users/face_login.html')

        # If the face doesn't match
        messages.error(request, "Face did not match. Please try again.")

    return render(request, 'users/face_login.html')



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')




import logging
logger = logging.getLogger(__name__)

import json

@login_required
def apply_filter_and_preview(request):
    logger.info("Received AJAX request")
    logger.info("Form Data: %s", request.POST)
    logger.info("CSRF Token: %s", request.headers.get('X-CSRFToken'))

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        image_nft = request.FILES.get('image', None)
        selected_filter = request.POST.get('image_filter', None)

        logger.info("Image NFT: %s", image_nft)
        logger.info("Selected Filter: %s", selected_filter)

        if image_nft and selected_filter:
            # Load the image using PIL
            image = Image.open(image_nft)

            # Apply the selected filter using pilgram
            if hasattr(pilgram, selected_filter):
                filter_function = getattr(pilgram, selected_filter)
                filtered_image = filter_function(image)
            else:
                # If the selected filter is not available, use a default filter (e.g., grayscale)
                filtered_image = image

            # Save the filtered image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_file_path = temp_file.name
                filtered_image.save(temp_file_path, format='JPEG')

            # Encode the filtered image as a base64 data URL
            with open(temp_file_path, "rb") as f:
                image_data = f.read()
            filtered_image_base64 = "data:image/jpeg;base64," + base64.b64encode(image_data).decode()

            # Clean up the temporary file
            os.remove(temp_file_path)

    # Ensure that the variable is defined before using it in JsonResponse
    if filtered_image_base64 is not None:
        return JsonResponse({'filtered_image': filtered_image_base64})
    else:
        return JsonResponse({'error': 'Invalid image or filter selected.'}, status=400)


def upload_to_ipfs(file_path):
    WEB3_API = os.getenv('WEB3_API')
    w3 = w3storage.API(token=WEB3_API)
    print(f"Uploading file: {file_path}")
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_name = os.path.basename(file_path)
    cid = w3.post_upload((file_name, file_content))
    ipfs_uri = f'ipfs://{cid}'
    print(f"Uploaded file to IPFS: {ipfs_uri}")
    return ipfs_uri



@login_required
def mint_nft_view(request):
    # Load the .env file from the 'battle-website' directory
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

    # Access the environment variables
    THIRDWEB_API_KEY = os.getenv('THIRDWEB_API_KEY')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    print("Environment Variables:", os.environ)

    # Print the values for debugging
    print("THIRDWEB_API_KEY:", THIRDWEB_API_KEY)
    print("PRIVATE_KEY:", PRIVATE_KEY[:10] + "..." if PRIVATE_KEY else "None")  # Print only the first 10 characters of the private key for security


    contract_address = "0x7777A79eBBd9BF1ab4afFA4c4f6fAD95d4A68191"

    # Retrieve the first name and last name of the user from the request object
    first_name = request.user.first_name
    last_name = request.user.last_name
    username = request.user.username

    # Combine first name and last name to form the initial_full_name
    initial_full_name = f'{first_name} {last_name}' if first_name and last_name else ""


    if request.method == 'POST':
        # Check if the filtered_image_data is present in the request data
        filtered_image_data = request.POST.get('filtered_image_data', None)
        if filtered_image_data:
            # If filtered_image_data is present, create an InMemoryUploadedFile from the data
            filtered_image_data = filtered_image_data.split(",")[1]
            image_data = base64.b64decode(filtered_image_data)
            image_file = InMemoryUploadedFile(
                BytesIO(image_data),
                field_name='filtered_image',
                name='filtered_image.jpg',
                content_type='image/jpeg',
                size=len(image_data),
                charset=None,
            )
        else:
            # If filtered_image_data is not present, use the original uploaded image
            image_file = request.FILES.get('image', None)

        nft_form = NFTMintForm(request.POST or None, request.FILES or None, instance=request.user.nft)
        if nft_form.is_valid():
            name_nft = request.POST.get('name', '')
            description_nft = request.POST.get('description', '')

            prop = {}

            # Create a temporary file to save the uploaded image
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())

            # Generating a random hexadecimal string and storing it in priv variable
            priv = secrets.token_hex(32)
            # Attaching 0x prefix to our 64 character hexadecimal string stored in priv and storing the new string in variable private_key.
            private_key_user = "0x" + priv
            # Creating a new account using the private_key_user and storing it in variable acct
            wallet_account = Account.from_key(private_key_user)
            # Get the Ethereum wallet address from the Account instance
            wallet_address = wallet_account.address

            # Get the current user
            user = request.user

            # Try to retrieve the existing Wallet for the user or create a new one with default values
            wallet, created = Wallet.objects.get_or_create(user=user, defaults={'wallet_address': wallet_address, 'private_key_user': private_key_user})

            # Update the wallet_address and private_key_user regardless of whether the wallet was created or already existed
            wallet.wallet_address = wallet_address
            wallet.private_key_user = private_key_user
            wallet.save()


            # Create the gas settings with your desired values
            gas_settings = GasSettings(max_price_in_gwei=5000000000000000000000000000, speed=GasSpeed.FAST)

            print("Initializing SDK with THIRDWEB_API_KEY:", THIRDWEB_API_KEY) # Print SDK initialization
            # Create an instance of the ThirdwebSDK using the private key and gas settings
            sdk = ThirdwebSDK("goerli", options=SDKOptions(secret_key=THIRDWEB_API_KEY, gas_settings=gas_settings))
            print("SDK Instance:", sdk) # Print SDK instance
            print("SDK Configuration:", vars(sdk))
            print("Contract Address:", contract_address)

            
            # Create a valid signer using your private key
            signer = Account.from_key(PRIVATE_KEY)
            sdk.update_signer(signer)

            print("PRIVATE_KEY:", PRIVATE_KEY)
            print("private_key_user:", private_key_user)
            print("Signer:", signer)

            print("Fetching contract with address:", contract_address)
            try:
                contract = sdk.get_contract(contract_address)
            except ProtocolError:
                messages.error(request, "There was a problem connecting to the server. Please try again later.")
                return render(request, "users/mint_nft.html", {'nft_form': nft_form, 'initial_full_name': initial_full_name})
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Exception Details:", str(e))
                messages.error(request, "An unexpected error occurred. Please contact the support team.")
                return render(request, "users/mint_nft.html", {'nft_form': nft_form, 'initial_full_name': initial_full_name})


            ipfs_uri = upload_to_ipfs(temp_file.name)

            metadata = NFTMetadataInput.from_json({
                "name": name_nft,
                "description": description_nft,
                "image": ipfs_uri,
            })

            # Call the mint_nft function with the metadata and SDK instance
            tx = contract.erc721.mint_to(wallet_address, metadata)
            receipt = tx.receipt
            token_id = tx.id
            nft = tx.data()

            # After the transaction, delete the temporary file
            os.remove(temp_file.name)

            # Remove the "ipfs://" prefix from the image IPFS URI
            image_url_without_prefix = ipfs_uri.replace("ipfs://", "")

            last_updated_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            nft = nft_form.save(commit=False)
            nft.user = request.user
            nft.image_ipfs_uri = image_url_without_prefix
            nft.contract_address = contract_address
            nft.token_id = token_id
            nft.last_updated_timestamp = last_updated_timestamp
            nft.save()

            messages.success(request, f'WEB3 ID NFT Successfully Minted for {username}!')

            if tx is not None:
                # NFT minted successfully, store relevant data in the session
                

                request.session['name_nft'] = name_nft
                request.session['description_nft'] = description_nft
                request.session['image_ipfs_uri'] = ipfs_uri
                request.session['created_by_address'] = wallet_address
                request.session['contract_address'] = contract_address
                request.session['token_id'] = token_id
                request.session['last_updated_timestamp'] = last_updated_timestamp
                request.session['token_standard'] = "ERC-721"
                request.session['network'] = "goerli"
                request.session['etherscan_link'] = f"https://goerli.etherscan.io/token/{contract_address}?a={token_id}"
                request.session['opensea_link'] = f"https://testnets.opensea.io/assets/goerli/{contract_address}/{token_id}"

                return redirect("mint-success")
        else:
            print("Form is not valid.")
            print("Form errors:", nft_form.errors)
    
    else:
        # Retrieve the first name and last name of the user from the request object
        first_name = request.user.first_name
        last_name = request.user.last_name

        # Combine first name and last name to form the initial_full_name
        initial_full_name = f'{first_name} {last_name}' if first_name and last_name else ""

        nft_form = NFTMintForm(instance=request.user.nft, initial={'name': initial_full_name})


    context = {
        'nft_form': nft_form,
        'initial_full_name': initial_full_name,
    }

    return render(request, "users/mint_nft.html", context,)


@login_required
def mint_success_view(request):
    name = request.session.get('name_nft')
    description = request.session.get('description_nft')
    ipfs_uri = request.session.get('image_ipfs_uri')
    created_by_address = request.session.get('created_by_address')
    contract_address = request.session.get('contract_address')
    token_id = request.session['token_id']
    token_standard = request.session.get('token_standard')
    network = request.session.get('network')
    etherscan_link = request.session.get('etherscan_link')
    opensea_link = request.session.get('opensea_link')
    last_updated_timestamp = request.session.get('last_updated_timestamp')


    # Remove the "ipfs://" prefix from the image IPFS URI
    image_url_without_prefix = ipfs_uri.replace("ipfs://", "")

    context = {
        'name': name,
        'description': description,
        'image_ipfs_hash': image_url_without_prefix,
        'created_by_address': created_by_address,
        'contract_address': contract_address,
        'token_id': token_id,
        'token_standard': token_standard,
        'network': network,
        'etherscan_link': etherscan_link,
        'opensea_link': opensea_link,
        'last_updated_timestamp': last_updated_timestamp,
        # Add more variables to the context as needed
    }
    return render(request, "users/mint_success.html", context)


@login_required
def verify_view(request):
    if request.method == 'POST':
        print("Processing POST request.")  # Log the request method

        # Decoding the Base64 image
        base64_img = request.POST.get('base64Image').split('base64,')[1]
        img_data = base64.b64decode(base64_img)
        image = ImageFile(BytesIO(img_data), name="captured_image.png")

        photo = WebCamUser(user=request.user, webcam_image=image)
        photo.save()

        print("Saved webcam image for user:", request.user.username)  # Log the saved image

        # Try to get the NFT image for this user
        try:
            verified_photo = request.user.nft.image
            print("Using verified photo from NFT for user:", request.user.username)  # Log the NFT photo used
        except NFT.DoesNotExist:
            messages.error(request, "No NFT image found for comparison. Please contact support.")
            return render(request, 'users/verify.html')


        results = []

        try:
            uploaded_image = face_recognition.load_image_file(photo.webcam_image.path)
            uploaded_encodings = face_recognition.face_encodings(uploaded_image)

            print("Number of faces detected in uploaded image:", len(uploaded_encodings))  # Log the number of detected faces

            verified_image = face_recognition.load_image_file(verified_photo.path)
            verified_encodings = face_recognition.face_encodings(verified_image)

            print("Number of faces detected in verified image:", len(verified_encodings))  # Log the number of detected faces

            # Ensure that faces were detected in both images
            if not uploaded_encodings or not verified_encodings:
                raise ValueError("No face detected in one or both images.")

            # Compute the face distance
            face_distances = face_recognition.face_distance([verified_encodings[0]], uploaded_encodings[0])
            print("Face Distance:", face_distances[0])

            # Load images with PIL
            uploaded_pil_image = Image.open(photo.webcam_image.path)
            verified_pil_image = Image.open(verified_photo.path)

            # Draw on the images
            draw_uploaded = ImageDraw.Draw(uploaded_pil_image)
            draw_verified = ImageDraw.Draw(verified_pil_image)

            # Get face landmarks
            uploaded_landmarks = face_recognition.face_landmarks(uploaded_image)[0]
            verified_landmarks = face_recognition.face_landmarks(verified_image)[0]

            # Draw landmarks on uploaded image
            for feature, points in uploaded_landmarks.items():
                draw_uploaded.line(points, fill="red", width=2)

            # Draw landmarks on verified image
            for feature, points in verified_landmarks.items():
                draw_verified.line(points, fill="blue", width=2)

            # Save the images with landmarks
            uploaded_with_landmarks_path = photo.webcam_image.path.replace(".png", "_landmarks.png")
            verified_with_landmarks_path = verified_photo.path.replace(".png", "_landmarks.png")

            uploaded_with_landmarks_relative_path = os.path.join(settings.MEDIA_URL, 'webcam_images', os.path.basename(uploaded_with_landmarks_path))
            verified_with_landmarks_relative_path = os.path.join(settings.MEDIA_URL, 'nft_images', os.path.basename(verified_with_landmarks_path))


            uploaded_pil_image.save(uploaded_with_landmarks_path)
            verified_pil_image.save(verified_with_landmarks_path)


            # Save the image paths in the session
            request.session['uploaded_with_landmarks_path'] = uploaded_with_landmarks_relative_path
            request.session['verified_with_landmarks_path'] = verified_with_landmarks_relative_path
            request.session['partial_face_encodings'] = str(uploaded_encodings[0][:5])  # Or wherever this line is in your verify_view
            
            # After computing the verified_encodings
            face_encoding_data = np.array(uploaded_encodings[0]).tobytes()  # Convert numpy array to bytes
            UserFaceEncoding.objects.create(user=request.user, face_encoding=face_encoding_data)


            # Set up the context for rendering
            context = {
                'uploaded_image_url': uploaded_with_landmarks_path,
                'verified_nft_image_url': verified_with_landmarks_path,
            }

            results = face_recognition.compare_faces([verified_encodings[0]], uploaded_encodings[0])

            request.session['compare_faces_result'] = bool(results[0])

            
        except ValueError as ve:
            # Handle specific error where no face is detected
            messages.error(request, str(ve))
            context = {
                'uploaded_image_url': uploaded_with_landmarks_path,
                'verified_nft_image_url': verified_with_landmarks_path,
            }
            return render(request, 'users/verify.html', context)

        except Exception as e:
            # Handle general errors
            messages.error(request, "An error occurred during face recognition. Please try again.")
            context = {
                'uploaded_image_url': uploaded_with_landmarks_path,
                'verified_nft_image_url': verified_with_landmarks_path,
            }
            return render(request, 'users/verify.html', context)

        if results and results[0]:
            photo.verified = True
            photo.save()
            return redirect('verify-success')
        else:
            # Handle case where the faces don't match
            messages.error(request, "Faces don't match. Please try again.")
            context = {
                'uploaded_image_url': uploaded_with_landmarks_path,
                'verified_nft_image_url': verified_with_landmarks_path,
            }

            print(messages.get_messages(request))


            return render(request, 'users/verify.html', context)
        
    return render(request, 'users/verify.html')

        



def verify_success(request):
    uploaded_with_landmarks_url = request.session.get('uploaded_with_landmarks_path')
    verified_with_landmarks_url = request.session.get('verified_with_landmarks_path')
    partial_face_encodings = request.session.get('partial_face_encodings')
    compare_faces_result = request.session.get('compare_faces_result')

    context = {
        'uploaded_with_landmarks_url': uploaded_with_landmarks_url,
        'verified_with_landmarks_url': verified_with_landmarks_url,
        'partial_face_encodings': partial_face_encodings,
        'compare_faces_result': compare_faces_result
    }

    if 'uploaded_with_landmarks_path' in request.session:
        del request.session['uploaded_with_landmarks_path']
    if 'verified_with_landmarks_path' in request.session:
        del request.session['verified_with_landmarks_path']
    if 'partial_face_encodings' in request.session:
        del request.session['partial_face_encodings']
    if 'compare_faces_result' in request.session:
        del request.session['compare_faces_result']

    return render(request, 'users/verify-success.html', context)




def save_color(request):
    if request.method == "POST":
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        color = data.get('color')

        # Log the received color
        print("Saving color:", color)

        # Save the color in the session
        request.session['p_color'] = color

        return JsonResponse({'status': 'success'})
    
def save_color_header(request):
    if request.method == "POST":
        # Parse the JSON data from the request body
        data_head = json.loads(request.body.decode('utf-8'))
        colorHeader = data_head.get('colorHeader')

        # Log the received color
        print("Saving font header color:", colorHeader)

        # Save the color in the session
        request.session['p_color_header'] = colorHeader

        return JsonResponse({'status': 'success'})


@login_required
def create_personal_profile(request):
    try:
        # Check if the user already has a personal profile
        personal_profile = PersonalProfile.objects.get(user=request.user)
        personal_profile_form = PersonalProfileForm(request.POST or None, request.FILES or None, instance=personal_profile)
    except PersonalProfile.DoesNotExist:
        # If not, create a new one
        personal_profile_form = PersonalProfileForm(request.POST or None, request.FILES or None, initial={'full_name': request.user.nft.name})

    personal_profile = PersonalProfile.objects.filter(user=request.user).first()
    selected_color = request.session.get('p_color', '#f8f9fa')
    selected_color_header = request.session.get('p_color_header', '#000000')

    # Retrieve the first name and last name of the user from the request object
    first_name = request.user.first_name
    last_name = request.user.last_name
    initial_full_name = f'{first_name} {last_name}' if first_name and last_name else ""

    username = request.user.username

    # Instantiate the form based on the request method
    if request.method == 'POST':
        personal_profile_form = PersonalProfileForm(request.POST, instance=personal_profile, initial={'full_name': initial_full_name})
        if personal_profile_form.is_valid():
            personal_profile = personal_profile_form.save(commit=False)
            personal_profile.p_color = selected_color
            personal_profile.p_color_header = selected_color_header
            personal_profile.user = request.user
            personal_profile.save()

            request.session['grade_level'] = personal_profile.grade_level
            request.session['school'] = personal_profile.school
            request.session['hometown'] = personal_profile.hometown
            request.session['mobile'] = personal_profile.mobile
            request.session['personal_linkedin'] = personal_profile.personal_linkedin

            
            messages.success(request, f'Personal Profile Successfully Created for {username}!')
            return redirect('profile_home')  # Redirect to Profile Home
    else:
        personal_profile_form = PersonalProfileForm(instance=personal_profile, initial={'full_name': initial_full_name})
    
    context = {
        'personal_profile_form': personal_profile_form,
        'selected_color': selected_color,
        'selected_color_header': selected_color_header,
    }

    return render(request, 'users/create_personal_profile.html', context)



@login_required
def update_personal_profile(request):
    user_profile = get_object_or_404(PersonalProfile, user=request.user)
    
    if request.method == 'POST':
        form = PersonalProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile_personal'))


    else:
        form = PersonalProfileForm(instance=user_profile)

    selected_color = user_profile.p_color or '#f8f9fa'
    selected_color_header = user_profile.p_color_header or '#000000'

    # Define the context
    context = {
        'personal_profile_form': form,
        'personal_profile': user_profile,
        'selected_color': selected_color,
        'selected_color_header': selected_color_header,
    }

    return render(request, 'users/update_personal_profile.html', context)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




def get_location_from_ip(ip_address):
    # Path to the database file
    db_path = settings.GEOIP_PATH + '/GeoLite2-City.mmdb'
    
    with geoip2.database.Reader(db_path) as reader:
        try:
            response = reader.city(ip_address)
            country = response.country.name
            city = response.city.name
            return city, country
        except geoip2.errors.AddressNotFoundError:
            # IP not found in the database
            return None, None


def display_qr_code(request):
    track_url = f"https://2260-96-232-102-204.ngrok-free.app/track_vcard?user_id={request.user.id}"
    
    qr = segno.make(track_url)
    buffer = io.BytesIO()
    qr.save(buffer, kind='PNG', scale=5)
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')



def send_token_to_user(user_eth_address):
    
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

    # Your server's Ethereum account
    sender_address = '0xB7a978C09f74bFCC872FCAdb98FFC8579BDC109E'
    private_key = os.getenv('PRIVATE_KEY')

    # Print statements for debugging
    print(f"Private Key: {private_key}")  # Ensure it prints a valid key
    print(f"Recipient: {user_eth_address}")  # Ensure the recipient address is correct
    print(f"Sender Address: {sender_address}")  # Check sender address too

    # Token details
    token_address = '0xF62D94eF1C18cB71F5D9C5cb7675c1462AD80F54'
    print(f"Contract Address: {token_address}")  # Ensure the token address is correct

    with open("token_abi.json", "r") as f:
        token_abi = json.load(f)

    # Connect to the token contract
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)

    # Specify token amount to send (for example, 1 token here, but you need to consider decimals in real scenarios)
    amount = 1

    # Build a transaction
    tx = token_contract.functions.transfer(user_eth_address, amount).buildTransaction({
        'chainId': 5,
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(sender_address),
    })

    print(f"Transaction: {tx}")  # Printing out the entire transaction to check its values

    # Sign the transaction
    signed_tx = w3.eth.account.signTransaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return tx_hash.hex()





def track_vcard(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)

    # Constructing the vCard for the user
    full_name = user.personal_profile.full_name
    title = user.personal_profile.title
    email = user.email
    mobile = user.personal_profile.mobile
    photo_link = f'https://gateway.ipfs.io/ipfs/{user.nft.image_ipfs_uri}'


    # Get location data from IP
    client_ip = get_client_ip(request)
    city, country = get_location_from_ip(client_ip)
    
    # Record the scan event
    ip_address = get_client_ip(request)  # Use the function we provided earlier to get the IP
    
    print(f"Timestamp: {datetime.now(tz=timezone.utc)}")
    print(f"IP Address: {get_client_ip(request)}")  
    print(f"Scan from IP: {client_ip}, Location: {city}, {country}")  # Logs the IP and location to the console

    # After recording the scan event
    user_wallet_address = user.wallet.wallet_address  # Assuming the user has a related 'wallet' attribute with an 'wallet_address' field

    try:
        # Send tokens to the user
        tx_hash = send_token_to_user(user_wallet_address)
        print(f"Token sent! Transaction hash: {tx_hash}")
    except Exception as e:
        print(f"Error sending token: {e}")

    scan_event = QRScanEvent(
        user=user, 
        scan_timestamp=timezone.now(), 
        ip_address=ip_address, 
        city=city, 
        country=country,
        tx_hash=tx_hash
    )
    
    scan_event.save()

    vcard = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{full_name}\n"
        f"TITLE:{title}\n"
        f"EMAIL:{email}\n"
        f"TEL:{mobile}\n"
        f"PHOTO;VALUE=URI:{photo_link}\n"
        "END:VCARD"
    )
    


    return HttpResponse(vcard, content_type='text/vcard')



def get_wallet_details(user_wallet_address):

    # If user_wallet_address is empty, return an empty dictionary
    if not user_wallet_address:
        return {}

    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

    # Load the NFT ABI data from the file
    with open("nft_abi.json", "r") as f:
        nft_abi = json.load(f)

    # Load the Token ABI data from the file
    with open("token_abi.json", "r") as f:
        token_abi = json.load(f)

    # Fetch Ether balance
    balance_wei = w3.eth.getBalance(user_wallet_address)
    balance_eth = w3.fromWei(balance_wei, 'ether')

    # Fetch current block number
    block_number = w3.eth.blockNumber

    # Fetch ERC-20 token balance
    erc20_contract = w3.eth.contract(address='0xF62D94eF1C18cB71F5D9C5cb7675c1462AD80F54', abi=token_abi)
    token_name = erc20_contract.functions.name().call()
    token_symbol = erc20_contract.functions.symbol().call()
    print(token_name)
    print(token_symbol)

    user_balance = erc20_contract.functions.balanceOf(user_wallet_address).call()

    # Fetch NFT details
    erc721_contract = w3.eth.contract(address='0x7777A79eBBd9BF1ab4afFA4c4f6fAD95d4A68191', abi=nft_abi)
    user_token_count = erc721_contract.functions.balanceOf(user_wallet_address).call()
    user_nfts = [erc721_contract.functions.tokenOfOwnerByIndex(user_wallet_address, i).call() for i in range(user_token_count)]
    
    nft_details = []
    for nft_id in user_nfts:
        
        nft_name = erc721_contract.functions.name().call()
        nft_uri = erc721_contract.functions.tokenURI(nft_id).call()

        if nft_uri.startswith("ipfs://"):
            nft_uri = nft_uri.replace("ipfs://", "https://ipfs.io/ipfs/")
        
        response = requests.get(nft_uri)
        
        nft_metadata = response.json()
        nft_description = nft_metadata.get('description', '')
        nft_details.append({
            'id': nft_id,
            'name': nft_name,
            'description': nft_description
        })

    return {
        'wallet_address': user_wallet_address,
        'balance_eth': balance_eth,
        'block_number': block_number,
        'token_balance': user_balance,
        'token_name': token_name,
        'token_symbol': token_symbol,
        'nfts': nft_details
    }


@login_required
def qr_dashboard(request):
    # Fetch the last 10 scan events specifically for the currently logged-in user
    scan_events = QRScanEvent.objects.filter(user=request.user).order_by('-scan_timestamp')[:10]

    # Print the number of fetched scan events.
    print("Number of scan events:", len(scan_events))

    # Print each scan event's details.
    for event in scan_events:
        print(event.user, event.scan_timestamp, event.ip_address)

    # Print the executed SQL query.
    print(scan_events.query)

    # Print the user's ID.
    print("Current user's ID:", request.user.id)

    return render(request, 'users/qr_dashboard.html', {'scan_events': scan_events})


@login_required
def profile_home_view(request):
  
    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    users = User.objects.exclude(is_superuser=True)
    
    # Check if the user is a superuser
    if request.user.is_superuser:
        wallet_details = {}
    else:
        wallet = Wallet.objects.get(user=request.user)
        wallet_details = get_wallet_details(wallet.wallet_address)


         # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    web3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

    token_address = "0xF62D94eF1C18cB71F5D9C5cb7675c1462AD80F54"

    # Load the Token ABI data from the file
    with open("token_abi.json", "r") as f:
        token_abi = json.load(f)

    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    
    token_name = token_contract.functions.name().call()
    symbol = token_contract.functions.symbol().call()
    total_supply = token_contract.functions.totalSupply().call()
    transfer_filter = token_contract.events.Transfer.createFilter(fromBlock="0x0")
    transfers = transfer_filter.get_all_entries()


    leaderboard_data = []
    for user in users:
        if hasattr(user, 'wallet'):
            wallet_details = get_wallet_details(user.wallet.wallet_address)
            token_balance = wallet_details.get('token_balance', 0)
            leaderboard_data.append((user, token_balance))

    leaderboard_data.sort(key=lambda x: x[1], reverse=True)

    # Define the context
    context = {
        'nft': nft,
        'personal_profile': personal_profile, 
        'wallet': wallet,
        "token_name": token_name,
        "symbol": symbol,
        "total_supply": total_supply,
        "transfer_filter":transfer_filter,
        "transfers":transfers,
        'leaderboard': leaderboard_data,

        **wallet_details
    }

    # Only add the 'wallet' to context if the user is not a superuser
    if not request.user.is_superuser:
        context['wallet'] = wallet

    return render(request, 'users/profile_home.html', context)


@login_required
def email_sig_porfile_view(request):

    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    
    wallet_details = get_wallet_details(wallet.wallet_address)

    # Define the context
    context = {
        'nft': nft,
        'personal_profile': personal_profile, 
        'wallet': wallet,
        **wallet_details
    }

    return render(request, 'users/email_signature.html', context)


@login_required
def contact_profile_view(request):
    user_form = UpdateUserForm(instance=request.user)
    
    # Fetch additional information from the database
    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    scan_events = QRScanEvent.objects.filter(user=request.user).order_by('-scan_timestamp')[:10]
    wallet = Wallet.objects.get(user=request.user)
    
    wallet_details = get_wallet_details(wallet.wallet_address)



    # Define the context
    context = {
        'user_form': user_form,
        'nft': nft,
        'personal_profile': personal_profile, 
        'scan_events': scan_events,
        'wallet': wallet,

        **wallet_details
    }

    return render(request, 'users/contact_card.html', context)


@login_required
def resume_profile_view(request):
    user_form = UpdateUserForm(instance=request.user)
    
    # Fetch additional information from the database
    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    
    wallet_details = get_wallet_details(wallet.wallet_address)

    # Define the context
    context = {
        'user_form': user_form,
        'nft': nft,
        'personal_profile': personal_profile, 
        'wallet': wallet,
        **wallet_details
    }

    return render(request, 'users/digital_resume.html', context)


@login_required
def profile_personal_view(request):
    user_form = UpdateUserForm(instance=request.user)
    
    # Fetch additional information from the database
    nft = NFT.objects.filter(user=request.user)
    personal_profile = PersonalProfile.objects.get(user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    
    wallet_details = get_wallet_details(wallet.wallet_address)

    # Define the context
    context = {
        'user_form': user_form,
        'nft': nft,
        'personal_profile': personal_profile, 
        'wallet': wallet,
        **wallet_details
        
    }

    return render(request, 'users/profile_home.html', context)


def token_view(request):

    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    web3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

    token_address = "0xF62D94eF1C18cB71F5D9C5cb7675c1462AD80F54"

    # Load the Token ABI data from the file
    with open("token_abi.json", "r") as f:
        token_abi = json.load(f)

    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    
    name = token_contract.functions.name().call()
    symbol = token_contract.functions.symbol().call()
    total_supply = token_contract.functions.totalSupply().call()
    transfer_filter = token_contract.events.Transfer.createFilter(fromBlock="0x0")
    transfers = transfer_filter.get_all_entries()
    
    context = {
        "name": name,
        "symbol": symbol,
        "total_supply": total_supply,
        "transfer_filter":transfer_filter,
        "transfers":transfers,
    }

    return render(request, "users/token.html", context)


@login_required
def view_wallet(request):
    user_wallet_address = request.user.wallet.wallet_address
    context = get_wallet_details(user_wallet_address)
    return render(request, 'users/view_wallet.html', context)


@login_required
def update_user(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your user information has been updated successfully')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'users/update_user.html', {'user_form': user_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')




@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensures only superusers can access this view
def erc721_contract_details(request):

    nft_objects = NFT.objects.all()

    # Initialize web3 with Infura
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))
    
    # Load the NFT ABI data from the file
    with open("nft_abi.json", "r") as f:
        nft_abi = json.load(f)

    contract_address = "0x7777A79eBBd9BF1ab4afFA4c4f6fAD95d4A68191"
    contract = w3.eth.contract(address=contract_address, abi=nft_abi)

    # Get Contract Details
    contract_name = contract.functions.name().call()
    contract_symbol = contract.functions.symbol().call()
    total_supply = contract.functions.totalSupply().call()

    # Fetching details for each minted NFT
    nft_details = []
    for i in range(total_supply):
        token_id = contract.functions.tokenByIndex(i).call()
        owner = contract.functions.ownerOf(token_id).call()
        metadata_uri = contract.functions.tokenURI(token_id).call()
        # Additional metadata fetching and parsing can be added here

        nft_details.append({
            'token_id': token_id,
            'owner': owner,
            'metadata_uri': metadata_uri
        })

    # Note: Fetching every transfer event can be a bit data-intensive. 
    # Use this wisely and consider potential solutions for paginating or filtering results.
    transfer_events = contract.events.Transfer.getLogs(fromBlock=0, toBlock='latest')

    transfers = [{
        'from': event['args']['from'],
        'to': event['args']['to'],
        'token_id': event['args']['tokenId']
    } for event in transfer_events]

    context = {
        'contract_name': contract_name,
        'contract_symbol': contract_symbol,
        'nft_details': nft_details,
        'transfers': transfers,
        'nft_objects': nft_objects,
    }

    return render(request, 'users/nft_smart_contract.html', context)




def get_contract_instance(infura_endpoint, contract_address, token_abi_path):
    w3 = Web3(Web3.HTTPProvider(infura_endpoint))
    with open(token_abi_path, "r") as f:
        token_abi = json.load(f)
    contract = w3.eth.contract(address=contract_address, abi=token_abi)
    return contract

def get_contract_details(contract):
    return {
        'name': contract.functions.name().call(),
        'symbol': contract.functions.symbol().call(),
        'total_supply': contract.functions.totalSupply().call(),
        'decimals': contract.functions.decimals().call(),
    }

def get_transfer_events(contract):
    transfer_events = contract.events.Transfer.getLogs(fromBlock=0, toBlock='latest')
    decimals = contract.functions.decimals().call()
    return [{
        'from': event['args']['from'],
        'to': event['args']['to'],
        'value': event['args']['value'] / (10 ** decimals)  # adjust by decimals for readability
    } for event in transfer_events]


@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensures only superusers can access this view
def erc20_contract_details(request):
    INFURA_ENDPOINT = os.getenv('INFURA_ENDPOINT')
    CONTRACT_ADDRESS = "0xF62D94eF1C18cB71F5D9C5cb7675c1462AD80F54"
    TOKEN_ABI_PATH = "token_abi.json"
    
    contract = get_contract_instance(INFURA_ENDPOINT, CONTRACT_ADDRESS, TOKEN_ABI_PATH)
    details = get_contract_details(contract)
    
    readable_total_supply = details['total_supply'] / (10 ** details['decimals'])

    transfers = get_transfer_events(contract)
    
    context = {
        'contract_name': details['name'],
        'contract_symbol': details['symbol'],
        'transfers': transfers,
        'total_supply': readable_total_supply,
        'decimals': details['decimals'],
    }

    return render(request, 'users/token_contract.html', context)
