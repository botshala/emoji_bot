#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

PAGE_ACCESS_TOKEN = 'EAAYgQ8PcnXcBAMoZC2E1QWAem7VOc7VLvUsTNNHCNx2seOF5CFoMYkodiPk7jgW98ALPIkx8Q8h46joQh93A4EEIs5dmvQXvERRUIMKZCbbna73yGvvusB9tryP5B17TKXXgaajBTDVgZB8r1a4M2qAuaJ9NqkkuHA3ZCHDtZCQZDZD'
VERIFY_TOKEN = '8447789934m'

emoji_arr = [["\ud83d\ude04", "Smiling Face with Open Mouth and Smiling Eyes"], ["\ud83d\ude03", "Smiling Face with Open Mouth"], ["\ud83d\ude00", "Grinning Face"], ["\ud83d\ude0a", "Smiling Face with Smiling Eyes"], ["\u263a\ufe0f", "White Smiling Face"], ["\ud83d\ude09", "Winking Face"], ["\ud83d\ude0d", "Smiling Face with Heart-Shaped Eyes"], ["\ud83d\ude18", "Face Throwing a Kiss"], ["\ud83d\ude1a", "Kissing Face with Closed Eyes"], ["\ud83d\ude17", "Kissing Face"], ["\ud83d\ude19", "Kissing Face with Smiling Eyes"], ["\ud83d\ude1c", "Face with Stuck-Out Tongue and Winking Eye"], ["\ud83d\ude1d", "Face with Stuck-Out Tongue and Tightly-Closed Eyes"], ["\ud83d\ude1b", "Face with Stuck-Out Tongue"], ["\ud83d\ude33", "Flushed Face"], ["\ud83d\ude01", "Grinning Face with Smiling Eyes"], ["\ud83d\ude14", "Pensive Face"], ["\ud83d\ude0c", "Relieved Face"], ["\ud83d\ude12", "Unamused Face"], ["\ud83d\ude1e", "Disappointed Face"], ["\ud83d\ude23", "Persevering Face"], ["\ud83d\ude22", "Crying Face"], ["\ud83d\ude02", "Face with Tears of Joy"], ["\ud83d\ude2d", "Loudly Crying Face"], ["\ud83d\ude2a", "Sleepy Face"], ["\ud83d\ude25", "Disappointed but Relieved Face"], ["\ud83d\ude30", "Face with Open Mouth and Cold Sweat"], ["\ud83d\ude05", "Smiling Face with Open Mouth and Cold Sweat"], ["\ud83d\ude13", "Face with Cold Sweat"], ["\ud83d\ude29", "Weary Face"], ["\ud83d\ude2b", "Tired Face"], ["\ud83d\ude28", "Fearful Face"], ["\ud83d\ude31", "Face Screaming in Fear"], ["\ud83d\ude20", "Angry Face"], ["\ud83d\ude21", "Pouting Face"], ["\ud83d\ude24", "Face with Look of Triumph"], ["\ud83d\ude16", "Confounded Face"], ["\ud83d\ude06", "Smiling Face with Open Mouth and Tightly-Closed Eyes"], ["\ud83d\ude0b", "Face Savouring Delicious Food"], ["\ud83d\ude37", "Face with Medical Mask"], ["\ud83d\ude0e", "Smiling Face with Sunglasses"], ["\ud83d\ude34", "Sleeping Face"], ["\ud83d\ude35", "Dizzy Face"], ["\ud83d\ude32", "Astonished Face"], ["\ud83c\udfe0", "House Building"], ["\ud83c\udfe1", "House with Garden"], ["\ud83c\udfeb", "School"], ["\ud83c\udfe2", "Office Building"], ["\ud83c\udfe3", "Japanese Post Office"], ["\ud83c\udfe5", "Hospital"], ["\ud83c\udfe6", "Bank"], ["\ud83c\udfea", "Convenience Store"], ["\ud83c\udfe9", "Love Hotel"], ["\ud83c\udfe8", "Hotel"], ["\ud83d\udc92", "Wedding"], ["\u26ea\ufe0f", "Church"], ["\ud83c\udfec", "Department Store"], ["\ud83c\udfe4", "European Post Office"], ["\ud83c\udf07", "Sunset over Buildings"], ["\ud83c\udf06", "Cityscape at Dusk"], ["\ud83c\udfef", "Japanese Castle"], ["\ud83c\udff0", "European Castle"], ["\u26fa\ufe0f", "Tent"], ["\ud83c\udfed", "Factory"], ["\ud83d\uddfc", "Tokyo Tower"], ["\ud83d\uddfe", "Silhouette of Japan"], ["\ud83d\uddfb", "Mount Fuji"], ["\ud83c\udf04", "Sunrise over Mountains"], ["\ud83c\udf05", "Sunrise"], ["\ud83c\udf03", "Night with Stars"], ["\ud83d\uddfd", "Statue of Liberty"], ["\ud83c\udf09", "Bridge at Night"], ["\ud83c\udfa0", "Carousel Horse"], ["\ud83c\udfa1", "Ferris Wheel"], ["\u26f2\ufe0f", "Fountain"], ["\ud83c\udfa2", "Roller Coaster"], ["\ud83d\udea2", "Ship"], ["\u26f5\ufe0f", "Sailboat"], ["\ud83d\udea4", "Speedboat"], ["\ud83d\udea3", "Rowboat"], ["\u2693\ufe0f", "Anchor"], ["\ud83d\ude80", "Rocket"], ["\u2708\ufe0f", "Airplane"], ["\ud83d\udcba", "Seat"], ["\ud83d\ude81", "Helicopter"], ["\ud83d\ude82", "Steam Locomotive"], ["\ud83d\ude8a", "Tram"], ["\ud83d\ude89", "Station"], ["\ud83d\udc36", "Dog Face"], ["\ud83d\udc3a", "Wolf Face"], ["\ud83d\udc31", "Cat Face"], ["\ud83d\udc2d", "Mouse Face"], ["\ud83d\udc39", "Hamster Face"], ["\ud83d\udc30", "Rabbit Face"], ["\ud83d\udc38", "Frog Face"], ["\ud83d\udc2f", "Tiger Face"], ["\ud83d\udc28", "Koala"], ["\ud83d\udc3b", "Bear Face"], ["\ud83d\udc37", "Pig Face"], ["\ud83d\udc3d", "Pig Nose"], ["\ud83d\udc2e", "Cow Face"], ["\ud83d\udc17", "Boar"], ["\ud83d\udc35", "Monkey Face"], ["\ud83d\udc12", "Monkey"], ["\ud83d\udc34", "Horse Face"], ["\ud83d\udc11", "Sheep"], ["\ud83d\udc18", "Elephant"], ["\ud83d\udc3c", "Panda Face"], ["\ud83d\udc27", "Penguin"], ["\ud83d\udc26", "Bird"], ["\ud83d\udc24", "Baby Chick"], ["\ud83d\udc25", "Front-Facing Baby Chick"], ["\ud83d\udc23", "Hatching Chick"], ["\ud83d\udc14", "Chicken"], ["\ud83d\udc0d", "Snake"], ["\ud83d\udc22", "Turtle"], ["\ud83d\udc1b", "Bug"], ["\ud83d\udc1d", "Honeybee"], ["\ud83d\udc1c", "Ant"], ["\ud83d\udc1e", "Lady Beetle"], ["\ud83d\udc0c", "Snail"], ["\ud83d\udc19", "Octopus"], ["\ud83d\udc1a", "Spiral Shell"], ["\ud83d\udc20", "Tropical Fish"], ["\ud83d\udc1f", "Fish"], ["\ud83d\udc2c", "Dolphin"], ["\ud83d\udc33", "Spouting Whale"], ["\ud83d\udc0b", "Whale"], ["\ud83d\udc04", "Cow"], ["\ud83d\udc0f", "Ram"], ["\ud83d\udc00", "Rat"], ["\ud83d\udc03", "Water Buffalo"], ["\ud83c\udf8d", "Pine Decoration"], ["\ud83d\udc9d", "Heart with Ribbon"], ["\ud83c\udf8e", "Japanese Dolls"], ["\ud83c\udf92", "School Satchel"], ["\ud83c\udf93", "Graduation Cap"], ["\ud83c\udf8f", "Carp Streamer"], ["\ud83c\udf86", "Fireworks"], ["\ud83c\udf87", "Firework Sparkler"], ["\ud83c\udf90", "Wind Chime"], ["\ud83c\udf91", "Moon Viewing Ceremony"], ["\ud83c\udf83", "Jack-o-lantern"], ["\ud83d\udc7b", "Ghost"], ["\ud83c\udf85", "Father Christmas"], ["\ud83c\udf84", "Christmas Tree"], ["\ud83c\udf81", "Wrapped Present"], ["\ud83c\udf8b", "Tanabata Tree"], ["\ud83c\udf89", "Party Popper"], ["\ud83c\udf8a", "Confetti Ball"], ["\ud83c\udf88", "Balloon"], ["\ud83c\udf8c", "Crossed Flags"], ["\ud83d\udd2e", "Crystal Ball"], ["\ud83c\udfa5", "Movie Camera"], ["\ud83d\udcf7", "Camera"], ["\ud83d\udcf9", "Video Camera"], ["\ud83d\udcfc", "Videocassette"], ["\ud83d\udcbf", "Optical Disc"], ["\ud83d\udcc0", "DVD"], ["\ud83d\udcbd", "Minidisc"], ["\ud83d\udcbe", "Floppy Disk"], ["\ud83d\udcbb", "Personal Computer"], ["\ud83d\udcf1", "Mobile Phone"], ["\u260e\ufe0f", "Black Telephone"], ["\ud83d\udcde", "Telephone Receiver"], ["\ud83d\udcdf", "Pager"], ["\ud83d\udce0", "Fax Machine"], ["\ud83d\udce1", "Satellite Antenna"], ["\ud83d\udcfa", "Television"], ["\ud83d\udcfb", "Radio"], ["\ud83d\udd0a", "Speaker with Three Sound Waves"], ["\ud83d\udd09", "Speaker with One Sound Wave"], ["\ud83d\udd08", "Speaker"], ["\ud83d\udd07", "Speaker with Cancellation Stroke"], ["\ud83d\udd14", "Bell"], ["\ud83d\udd15", "Bell with Cancellation Stroke"], ["1\u20e3", "Keycap 1"], ["2\u20e3", "Keycap 2"], ["3\u20e3", "Keycap 3"], ["4\u20e3", "Keycap 4"], ["5\u20e3", "Keycap 5"], ["6\u20e3", "Keycap 6"], ["7\u20e3", "Keycap 7"], ["8\u20e3", "Keycap 8"], ["9\u20e3", "Keycap 9"], ["0\u20e3", "Keycap 0"], ["\ud83d\udd1f", "Keycap Ten"], ["\ud83d\udd22", "Input Symbol for Numbers"], ["#\u20e3", "Hash Key"], ["\ud83d\udd23", "Input Symbol for Symbols"], ["\u2b06\ufe0f", "Upwards Black Arrow"], ["\u2b07\ufe0f", "Downwards Black Arrow"], ["\u2b05\ufe0f", "Leftwards Black Arrow"], ["\u27a1\ufe0f", "Black Rightwards Arrow"], ["\ud83d\udd20", "Input Symbol for Latin Capital Letters"], ["\ud83d\udd21", "Input Symbol for Latin Small Letters"], ["\ud83d\udd24", "Input Symbol for Latin Letters"], ["\u2197\ufe0f", "North East Arrow"], ["\u2196\ufe0f", "North West Arrow"], ["\u2198\ufe0f", "South East Arrow"], ["\u2199\ufe0f", "South West Arrow"], ["\u2194\ufe0f", "Left Right Arrow"], ["\u2195\ufe0f", "Up Down Arrow"], ["\ud83d\udd04", "Anticlockwise Downwards and Upwards Open Circle Arrows"], ["\u25c0\ufe0f", "Black Left-Pointing Triangle"], ["\u25b6\ufe0f", "Black Right-Pointing Triangle"], ["\ud83d\udd3c", "Up-Pointing Small Red Triangle"], ["\ud83d\udd3d", "Down-Pointing Small Red Triangle"], ["\u21a9\ufe0f", "Leftwards Arrow with Hook"], ["\u21aa\ufe0f", "Rightwards Arrow with Hook"], ["\u2139\ufe0f", "Information Source"], ["\u23ea", "Black Left-Pointing Double Triangle"], ["\u23e9", "Black Right-Pointing Double Triangle"], ["\u23eb", "Black Up-Pointing Double Triangle"], ["\u23ec", "Black Down-Pointing Double Triangle"], ["\u2935\ufe0f", "Arrow Pointing Rightwards Then Curving Downwards "], ["\u2934\ufe0f", "Arrow Pointing Rightwards Then Curving Upwards"], ["\ud83c\udd97", "Squared OK"], ["\ud83d\udd00", "Twisted Rightwards Arrows"], ["\ud83d\udd01", "Clockwise Rightwards and Leftwards Open Circle Arrows"], ["\ud83c\udf21", "Thermometer"], ["\ud83c\udf22", "Black Droplet"], ["\ud83c\udf23", "White Sun"], ["\ud83c\udf24", "White Sun with Small Cloud"], ["\ud83c\udf25", "White Sun Behind Cloud"], ["\ud83c\udf26", "White Sun Behind Cloud with Rain"], ["\ud83c\udf27", "Cloud with Rain"], ["\ud83c\udf28", "Cloud with Snow"], ["\ud83c\udf29", "Cloud with Lightning"], ["\ud83c\udf2a", "Cloud with Tornado"], ["\ud83c\udf2b", "Fog"], ["\ud83c\udf2c", "Wind Blowing Face"], ["\ud83c\udf36", "Hot Pepper"], ["\ud83c\udf7d", "Fork and Knife with Plate"], ["\ud83c\udf94", "Heart with Tip on The Left"], ["\ud83c\udf95", "Bouquet of Flowers"], ["\ud83c\udf96", "Military Medal"], ["\ud83c\udf97", "Reminder Ribbon"], ["\ud83c\udf98", "Musical Keyboard with Jacks"], ["\ud83c\udf99", "Studio Microphone"], ["\ud83c\udf9a", "Level Slider"], ["\ud83c\udf9b", "Control Knobs"], ["\ud83c\udf9c", "Beamed Ascending Musical Notes"], ["\ud83c\udf9d", "Beamed Descending Musical Notes"], ["\ud83c\udf9e", "Film Frames"], ["\ud83c\udf9f", "Admission Tickets"], ["\ud83c\udfc5", "Sports Medal"], ["\ud83c\udfcb", "Weight Lifter"], ["\ud83c\udfcc", "Golfer"], ["\ud83c\udfcd", "Racing Motorcycle"], ["\ud83c\udfce", "Racing Car"], ["\ud83c\udfd4", "Snow Capped Mountain"], ["\ud83c\udfd5", "Camping"], ["\ud83c\udfd6", "Beach with Umbrella"], ["\ud83c\udfd7", "Building Construction"], ["\ud83c\udfd8", "House Buildings"], ["\ud83c\udfd9", "Cityscape"], ["\ud83c\udfda", "Derelict House Building"], ["\ud83c\udfdb", "Classical Building"], ["\ud83c\udfdc", "Desert"], ["\ud83c\udfdd", "Desert Island"], ["\ud83c\udfde", "National Park"], ["\ud83c\udfdf", "Stadium"], ["\ud83c\udff1", "White Pennant"], ["\u261d\ud83c\udffb", "White White Up Pointing Index"], ["\u261d\ud83c\udffc", "Light Brown White Up Pointing Index"], ["\u261d\ud83c\udffd", "Olive Toned White Up Pointing Index"], ["\u261d\ud83c\udffe", "Deeper Brown White Up Pointing Index"], ["\u261d\ud83c\udfff", "Black White Up Pointing Index"], ["\u270a\ud83c\udffb", "White Raised Fist"], ["\u270a\ud83c\udffc", "Light Brown Raised Fist"], ["\u270a\ud83c\udffd", "Olive Toned Raised Fist"], ["\u270a\ud83c\udffe", "Deeper Brown Raised Fist"], ["\u270a\ud83c\udfff", "Black Raised Fist"], ["\u270b\ud83c\udffb", "White Raised Hand"], ["\u270b\ud83c\udffc", "Light Brown Raised Hand"], ["\u270b\ud83c\udffd", "Olive Toned Raised Hand"], ["\u270b\ud83c\udffe", "Deeper Brown Raised Hand"], ["\u270b\ud83c\udfff", "Black Raised Hand"], ["\u270c\ud83c\udffb", "White Victory Hand"], ["\u270c\ud83c\udffc", "Light Brown Victory Hand"], ["\u270c\ud83c\udffd", "Olive Toned Victory Hand"], ["\u270c\ud83c\udffe", "Deeper Brown Victory Hand"], ["\u270c\ud83c\udfff", "Black Victory Hand"], ["\ud83c\udf85\ud83c\udffb", "White Father Christmas"], ["\ud83c\udf85\ud83c\udffc", "Light Brown Father Christmas"], ["\ud83c\udf85\ud83c\udffd", "Olive Toned Father Christmas"], ["\ud83c\udf85\ud83c\udffe", "Deeper Brown Father Christmas"], ["\ud83c\udf85\ud83c\udfff", "Black Father Christmas"], ["\ud83c\udfc3\ud83c\udffb", "White Runner"], ["\ud83c\udfc3\ud83c\udffc", "Light Brown Runner"], ["\ud83c\udfc3\ud83c\udffd", "Olive Toned Runner"], ["\ud83c\udfc3\ud83c\udffe", "Deeper Brown Runner"], ["\ud83c\udfc3\ud83c\udfff", "Black Runner"], ["\ud83c\udfc4\ud83c\udffb", "White Surfer"], ["\ud83c\udfc4\ud83c\udffc", "Light Brown Surfer"], ["\ud83c\udfc4\ud83c\udffd", "Olive Toned Surfer"], ["\ud83c\udfc4\ud83c\udffe", "Deeper Brown Surfer"], ["\ud83c\udfc4\ud83c\udfff", "Black Surfer"], ["\ud83c\udfc7\ud83c\udffb", "White Horse Racing"], ["\ud83c\udfc7\ud83c\udffc", "Light Brown Horse Racing"], ["\ud83c\udfc7\ud83c\udffd", "Olive Toned Horse Racing"], ["\ud83c\udfc7\ud83c\udffe", "Deeper Brown Horse Racing"], ["\ud83c\udfc7\ud83c\udfff", "Black Horse Racing"], ["\ud83c\udfca\ud83c\udffb", "White Swimmer"], ["\ud83c\udfca\ud83c\udffc", "Light Brown Swimmer"], ["\ud83c\udfca\ud83c\udffd", "Olive Toned Swimmer"], ["\ud83c\udfca\ud83c\udffe", "Deeper Brown Swimmer"]]

def emoji_search(search_string):
    #tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message)
    for emoji,emoji_text in emoji_arr:
        if search_string.lower() in emoji_text:
            return emoji

    return 'Emoji not found :('


def post_facebook_message(fbid, recevied_message):
    response_text = recevied_message + ' :)'
    response_text = emoji_search(recevied_message.lower())

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])

        return HttpResponse()    



def index(request):
    print test()
    return HttpResponse("Hello World")

def test():
    post_facebook_message('abhishek.sukumar.1','test message')



