# Copyright 2010 James Tatum
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import objc
from Foundation import *
from AppKit import *

speaking = False
speaknick = False
synthesizer = None

def voices():
   '''return a list of available voices'''
   voices = NSSpeechSynthesizer.availableVoices()
   voices = [x.split('.')[-1] for x in voices]
   return voices

def setvoice(voice):
   '''set the synthesizer voice to the specified voice

      Return True/False on success/failure
   '''
   global synthesizer
   if voice in voices():
      voice = 'com.apple.speech.synthesis.voice.' + voice
      synthesizer.setVoice_(voice)
      return True
   return False

def say(txt):
   '''say the specified text'''
   synthesizer.startSpeakingString_(txt)

def load( scriptFilePath ):
   '''colloquy calls this function on plugin load

      setup the synthesizer object
   '''
   global synthesizer
   voice = NSSpeechSynthesizer.defaultVoice()
   synthesizer = NSSpeechSynthesizer.alloc().initWithVoice_(voice)

def processUserCommand( command, arguments, connection, view ):
   '''handle commands entered by the user'''
   global speaking
   global speaknick
   # Remap this very long objective C function to something shorter
   message = view.addEventMessageToDisplay_withName_andAttributes_
   args = arguments.mutableString()
   if (command=='speech'):
      if (args in ['enable', 'on']):
         speaking = True
         message('Speech enabled', 'speechEnabled', None)
         return True
      elif (args in ['disable', 'off']):
         speaking = False
         message('Speech disabled', 'speechDisabled', None)
         return True
      elif (args == 'voices'):
         voice_list = ', '.join(voices())
         message('Voices: ' + voice_list, 'voiceList', None)
         return True
      elif (args.startswith('voice ')):
         requested_voice = args[6:].lstrip()
         if setvoice(requested_voice.capitalize()):
            message('Set voice to ' + requested_voice, 'voiceSet', None)
         else:
            message('%s is an invalid voice' % requested_voice, 'voiceSet',
                  None)
         return True
      elif (args == 'nick on'):
         speaknick = True
         message('Will speak nicknames.', 'nickSpeakSet', None)
         return True
      elif (args == 'nick off'):
         speaknick = False
         message('Will not speak nicknames.', 'nickSpeakSet', None)
         return True
      elif (args in ['help', '?']):
         help_text = [
               'Speech plugin:',
               '----',
               '/speech on - Enable speech',
               '/speech off - Disable speech',
               '/speech voices - List available voices.',
               '/speech voice VOICE - Set speaking voice',
               '/speech nick on - Speak the nick as well',
               '/speech nick off - Don\'t speak the nick',
               '/speech help - Display this help'
               ]
         for line in help_text:
            message(line, 'speechHelp', None)
         return True
      else:
         message('Invalid command. For help, use /speech help',
               'speechInvalid', None)
         return True
   return False

# called for each incoming message, the message is mutable
def processIncomingMessage( message, view ):
   global speaking
   global speaknick
   msg = message.bodyAsPlainText()
   source = view.identifier()
   if speaking and source.startswith('Chat Room'):
      if speaknick:
         say(message.senderNickname() + ': ' + msg)
      else:
         say(msg)


# Unused functions below:

# called on unload and relead
def unload():
   pass

# return an array of NSMenuItems that should be dispalyed for 'item' associated with 'view'
def contextualMenuItems( item, view ):
   pass

# return an array of toolbar item identifier strings that can be associated with 'view'
def toolbarItemIdentifiers( view ):
   pass

# return an NSToolbarItem for 'identifier' associated with 'view'
def toolbarItem( identifier, view, willBeInserted ):
   pass

# perform the action associated with 'toolbarItem' for 'view'
def handleClickedToolbarItem( toolbarItem, view ):
   pass

# handle a ctcp request and return true if you handle it or False to pass on to another plugin
def processSubcodeRequest( command, arguments, user ):
   # return true if the command was handled or to prevent other plugins or Colloquy from handling it
  return False

# handle a ctcp reply and return true if you handle it or False to pass on to another plugin
def processSubcodeReply( command, arguments, user ):
   # return true if the command was handled or to prevent other plugins or Colloquy from handling it
  return False

# called when 'connection' connects
def connected( connection ):
   pass

# called when 'connection' is disconnecting
def disconnecting( connection ):
   pass

# perform a notification
def performNotification( identifier, context, preferences ):
   pass

# called when an unhandled URL scheme is clicked in 'view'
def handleClickedLink( url, view ):
   # return true if the link was handled or to prevent other plugins or Colloquy from handling it
  return False

# called for each outgoing message, the message is mutable
def processOutgoingMessage( message, view ):
   pass

# called when a member joins 'room'
def memberJoined( member, room ):
   pass

# called when a member parts 'room'
def memberParted( member, room, reason ):
   pass

# called when a member is kicked from 'room' for 'reason'
def memberKicked( member, room, by, reason ):
   pass

# called when the local user joins 'room'
def joinedRoom( room ):
   pass

# called when the local user is parting 'room'
def partingFromRoom( room ):
   pass

# called when the local user is kicked from 'room' for 'reason'
def kickedFromRoom( room, by, reason ):
   pass

# called when the topic changes in 'room' by 'user'
def topicChanged( topic, room, user ):
   pass
