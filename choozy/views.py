import os
import json
import requests
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dotenv import load_dotenv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Room, Player, Submission, Result
from .serializers import RoomSerializer

load_dotenv()

SUPPORTED_COUNTRIES = ['ar', 'au', 'at', 'be', 'br', 'ca', 'cl', 'cz', 'dk', 'fi', 'fr', 'de', 'ie', 'it', 'jp', 'my', 'mx', 'nl', 'nz', 'no', 'ph', 'pl', 'pt', 'sg', 'es', 'se', 'ch', 'tw', 'tr', 'gb', 'us']

# Render homepage
def index(request):
    return render(request, 'choozy/index.html')


# Register (get: render form) (post: register user)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if not username or not email or not password or not confirmation:
            return render(request, 'choozy/register.html', {'error': 'Please fill out entire form!'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'choozy/register.html', {'error': 'Username taken!'})

        if password != confirmation:
            return render(request, 'choozy/register.html', {'error': 'Passwords do not match!'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
        except Exception:
            return render(request, 'choozy/register.html', {'error': 'Could not create account'})
    else:
        return render(request, 'choozy/register.html', {'error': None})


# Login (get: render form) (post: login user
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('rooms'))
        else:
            return render(request, 'choozy/login.html', {
                'error': 'Invalid username or password'
            })
    else:
        return render(request, 'choozy/login.html', {'error': None})


# Logout (get: render form) (post: login user)
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def rooms(request):
    username = request.user.username
    rooms = Room.objects.filter(creator=request.user).order_by('-date_created')
    return render(request, 'choozy/rooms.html', {
        'username': username,
        'rooms': rooms
    })


# Create room (get: render form with location) (post: create room and redirect to room template)
@login_required
def create_room(request):
    if request.method == 'POST':
        # Check if the latitude and longitude was retrieved
        if request.POST.get('current_location'):
            # Get lattitude and longitude
            latitude =  request.POST['latitude']
            longitude = request.POST['longitude']

            # Make a API request to geocoder
            url = f"https://us1.locationiq.com/v1/reverse?lat={latitude}&lon={longitude}&format=json&zoom=10&key={os.getenv('GEOCODER_KEY')}"
            response = requests.get(url, headers={"accept": "application/json"}).json()

            # Get city and country code from geocoder API
            city = response['address']['city']
            country_code = response['address']['country_code']

            # Check if the selected country is supporteed by the YELP API
            if country_code in SUPPORTED_COUNTRIES:
                try:
                    # Create a room object in database
                    room = Room(creator=request.user, latitude=latitude, longitude=longitude, city=city, country_code=country_code)
                    room.save()
                    room_id = room.id
                except Exception:
                    # Render error message
                    return render(request, 'choozy/create.html', {
                        'errormessage': 'Error creating room'
                    })
                
                # Make the creator the first player of the room and save player info in the session
                player = Player(username=request.user.username)
                player.save()
                player.room.add(room)
                request.session['player'] = {'id': player.id, 'room_id': room_id, 'name': player.username}

                return HttpResponseRedirect(reverse('room_admin', args=(room_id,)))
            else:
                return render(request, 'choozy/create.html', {
                    'errormessage': 'Your current location is not yet supported! Please enter location manually'
                })
        else:
            # Get the country and city
            city = request.POST['city']
            country_code = request.POST['country']

            # Check if the selected country is supporteed by the YELP API
            if country_code in SUPPORTED_COUNTRIES:
                try:
                    # Create a room object in database without coordinates
                    room = Room(creator=request.user, city=city, country_code=country_code)
                    room.save()
                    room_id = room.id
                except Exception:
                    # Render error message
                    return render(request, 'choozy/create.html', {
                        'errormessage': 'Error creating room'
                    })
                
                # Set the creator as the first player and save player info in session
                player = Player(username=request.user.username)
                player.save()
                player.room.add(room)
                request.session['player'] = {'id': player.id, 'room_id': room_id, 'name': player.username}

                return HttpResponseRedirect(reverse('room_admin', args=(room_id,)))
            else:
                return render(request, 'choozy/create.html', {
                    'errormessage': 'Location is not yet supported! Please enter location manually'
                })
    else:
        # Check if the user already has a active room 
        try:
            # Render the room admin page of the active room
            active_room = Room.objects.get(creator=request.user, active=True)
            return HttpResponseRedirect(reverse('room_admin', args=(active_room.id,)))
        except Room.DoesNotExist:
            return render(request, 'choozy/create.html')


# Render the room admin page
@login_required
def room_admin(request, room_id):
    room = Room.objects.get(id=room_id)

    # Check if the user is the room's creator
    if request.user == room.creator:
        # Render results page if the room is closed
        if not room.active: 
            HttpResponseRedirect(reverse('results', args=(room_id, )))

        # Get the room creator's status and render the admin dashboard
        try:
            player = Player.objects.get(id=request.session['player']['id'])
            status = player.status
        except Player.DoesNotExist:
            status = False
        return render(request, 'choozy/room_admin.html', {
            'id': room.id,
            'completed': status
        })


# Room Viewset by CS50 duck debugger (for API that returns list of players)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


# Lets a player join the room
def join(request, room_id):
    room = Room.objects.get(id=room_id)
    
    # Redirect creator to the room admin panel
    if request.user.is_authenticated and request.user == room.creator:
        return HttpResponseRedirect(reverse('room_admin', args=(room_id,)))
    else:
        # Check if the username is taken and try to create a player object in database
        if request.method == 'POST':
            name = request.POST['name']
            if name != '' and not Player.objects.filter(room=room, username=name) and name != room.creator.username:
                player = Player(username=name)
                player.save()
                player.room.add(room)
                request.session['player'] = {'id': player.id, 'room_id': room_id, 'name': name}
                return HttpResponseRedirect(reverse('room', args=(room_id,)))
            else:
                # Render error
                return render(request, 'choozy/join.html', {
                    'room': room,
                    'error': 'Name already taken!'
                })
        return render(request, 'choozy/join.html', {
            'room': room
        })


# Renders the Choozy form and adds response to the database
def room(request, room_id):
    # Check if the player has joined the room
    if request.session['player'] and room_id == request.session['player']['room_id']:
        playerobj = request.session['player']
        player = Player.objects.get(id=playerobj['id'])
        room = Room.objects.get(id=room_id)

        # Check if player hasn't already completed the form
        if not player.status:
            if request.method == 'POST':

                # Get player's choices
                category_list = request.POST.getlist('category')
                price = int(request.POST.get('price'))
                parking = True if request.POST.get('parking') == 'on' else False
                outdoor = True if request.POST.get('outdoor') == 'on' else False

                if not category_list:
                    return render(request, 'choozy/room.html', {'room': room, 'player': playerobj, 'error': 'Select at least one cusine or type!'})

                # Make the category list info a comma-seperated string
                categories = ", ".join(category_list)

                # Save the response
                response = Submission(room=room, player=player, categories=categories, price=price, parking=parking, outdoor=outdoor)
                response.save()

                player.status = True
                player.save()

                # Redirect to results page
                return HttpResponseRedirect(reverse('results', args=(room_id,))) 
            else:
                # Render Choozy form
                return render(request, 'choozy/room.html', {
                    'room': room,
                    'player': playerobj
                })
        else:
            # Redirect done user to results page
            return HttpResponseRedirect(reverse('results', args=(room_id,)))
    else:
        # Redirect to join page if user is not joined
        return HttpResponseRedirect(reverse('join', args=(room_id,))) 
    

@login_required
def close_room(request, room_id):
    room = Room.objects.get(id=room_id)

    # Get the responses of the players and make an API call
    if request.user == room.creator:
        submissions = Submission.objects.filter(room=room)

        # Create a dictionary with the categories and their frequencies
        categoey_freq = {}
        for submission in submissions:
            category_list = submission.categories.split(', ')
            for category in category_list:
                if category in categoey_freq:
                    categoey_freq[category] += 1
                else:
                    categoey_freq[category] = 1

        # Sort the catogories into a list  
        sorted_categories = sorted(categoey_freq.items(), key=lambda item: item[1])
        sorted_categories.reverse()

        # Find categories that have been chosen by more than one person
        overlaping = [category for category, freq in categoey_freq.items() if freq > 1]

        # Define the categories list
        if overlaping:
            categories = ','.join(overlaping)
        else:
            categories = ','.join([category for category, freq in categoey_freq.items()])


        # Make a list of the prices (ensuring they appear only once)
        prices = ','.join(list(set([str(submission.price) for submission in submissions])))

        # Get the atributes (parking and outdoor seating)
        attribute_list = []

        # If there is someone who needs parking, set it to true, otherwise false
        for submission in submissions:
            if submission.parking:
                attribute_list.append('parking')
                break

        # Use voting to determine if outdoor seating is prefered
        out = [submission.outdoor for submission in submissions]
        if out.count(True) > out.count(False) or out.count(True) == out.count(False):
            attribute_list.append('outdoor_seating')

        # Join attrubutes for API call
        attributes = ','.join(attribute_list) 

        # Create corresponding url
        if room.latitude and room.longitude:
            url = f"https://api.yelp.com/v3/businesses/search?latitude={room.latitude}&longitude={room.longitude}&radius=5000&term=food&categories={categories}&price={prices}&open_now=true&attributes={attributes}&sort_by=best_match&limit=12"
        else:
            url = f"https://api.yelp.com/v3/businesses/search?location={f"{room.city}, {room.country_code.upper()}"}&term=food&categories={categories}&price={prices}&open_now=true&attributes={attributes}&sort_by=best_match&limit=12"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('YELP_KEY')}"
        }

        # Make the API call and turn it into json form
        response = requests.get(url, headers=headers)
        json_data = response.json()

        # Enter the data into database
        try:
            for data in  json_data['businesses']:
                categories = ', '.join([category['title'] for category in data['categories']])
                result = Result(
                    room=room, 
                    restraunt_name=data['name'], 
                    image_url=data['image_url'], 
                    menu_url=data['attributes']['menu_url'], 
                    yelp_url=data['url'], 
                    phone=data['phone'], 
                    display_phone=data['display_phone'],
                    rating=data['rating'],
                    price=data['price'],
                    categories=categories
                    )
                result.save()
        except Exception as e:
            return HttpResponseRedirect(reverse('room_admin', args=(room_id,))) 

        # Set room acive status to false
        room.active = False
        room.save()
        return HttpResponseRedirect(reverse('results', args=(room_id,)))
    else:
        return HttpResponseRedirect(reverse('index'))
    

# API to get
@api_view(['GET'])
def players_in_room(request, room_id):
    try:
        # Authenticate player
        playerobj = request.session['player']
    except KeyError:
        return Response({'error': 'Authentication failed!'}, status=403)
    try:
        room = Room.objects.get(id=room_id)

        # If the request maker is in the room, return the data, return error if otherwise
        if playerobj['room_id'] == room_id:
            players = room.players.all()
            players_done = room.players.filter(status=True)
            return Response({'players': len(players), 'players_done': len(players_done), 'room_status': room.active}, status=200)
        else:
            return Response({'error': 'Authentication failed!'}, status=403)
    except Room.DoesNotExist:
        return Response({'error': 'Room does not exist!'}, status=404)


def results(request, room_id):
    # Get room
    room = Room.objects.get(id=room_id)

    if request.user == room.creator:
        # Send creator to admin page if it isn't closed
        if room.active:
            return HttpResponseRedirect(reverse('room_admin', args=(room_id,)))
        else:
            # Get the restraunt list
            restraunts = Result.objects.filter(room=room)

            # Split categories into a list
            for restraunt in restraunts:
                category_list = restraunt.categories.split(', ')
                restraunt.category_list = category_list

            # Render the results page
            return render(request, 'choozy/results.html', {
                'restraunts': restraunts
            })
    else:
        try:
            if request.session['player'] and room_id == request.session['player']['room_id']:
                player = Player.objects.get(id=request.session['player']['id'])

            # If player hasn't completed the form redirect them to the form
            if not player.status:
                return HttpResponseRedirect(reverse('room', args=(room_id,)))
            
            # Render waiting page if the room is not yet closed
            if room.active:
                return render(request, 'choozy/waitroom.html', {'room_id': room_id})

            else:
                # Get the restraunt list
                restraunts = Result.objects.filter(room=room)

                # Split categories into a list
                for restraunt in restraunts:
                    category_list = restraunt.categories.split(', ')
                    restraunt.category_list = category_list

                # Render the results page
                return render(request, 'choozy/results.html', {
                    'restraunts': restraunts
                })
        except KeyError:
            
            return HttpResponseRedirect(reverse('join', args=(room_id,))) 
