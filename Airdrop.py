import requests
import os
import pyperclip
import re
import webbrowser

my_airdrop_server = ''                                                                          #see README step 5
auth = {
    'authorization': ''                                                                         #see README step 6
}

stopKey = '$$$$###BEGINNING_OF_NEXT_AIRDROP_SESSION(server begins here)###$$$$'                 #make this whatever you want, this lets the program know not to go further back in the discord
text_divider = '---------------NEXT_MESSAGE_CONTENT---------------'                             #make this whatever you want, this is for the downloaded txt file
text_divider += '\n\n'

#toggles
promptOpenLinks = True                                                                          #When set to True, program will ask you if you want to open a link if it detects one
keepOpen = True                                                                                 #When set to True, program will remain open at the end until you press enter



#####################################################################################################################################################################################################
def postStopKey(stopKey, channel, authorization):
  data = {'content': stopKey}
  response = requests.post(channel, data=data, headers=authorization)
  while response.status_code != 200:
    key = input("Something went wrong trying to post session break. Response code was " + str(response.status_code) + ". Press Enter to try again (enter q to quit)")
    if key == 'q' or key == 'Q':
      quit()
    response = requests.post(channel, data=data, headers=authorization)



def getRecentMessages(messages, stopKey):
  for i in range (len(messages)):
    if messages[i]['content'] == stopKey:
      return messages[:i]

  return messages



def getMessages(channel, authorization, stopKey):
  messages = requests.get(channel, headers=authorization)
  while messages.status_code != 200:
    key = input("Something went wrong trying to retrieve data. Response code was " + str(messages.status_code) + ". Press Enter to try again (enter q to quit)")
    if key == 'q' or key == 'Q':
      quit()
    messages = requests.get(channel, headers=authorization)

  return getRecentMessages(messages.json(), stopKey)



def setFileName(filename, path=os.getcwd()):
  if not os.path.exists(path + '\\' + filename):
    return filename
  dot_index = filename.rfind('.')
  name = filename[0:dot_index]
  filetype = filename[dot_index:]
  num = 2

  while os.path.exists(path + '\\' + name + '(' + str(num) + ')' + filetype):
    num += 1
  return name + '(' + str(num) + ')' + filetype



def download_files(attachments):
  save_folder = os.getcwd() + '\\Airdrop Files'
  if not os.path.exists(save_folder):
    os.makedirs(save_folder)
  
  for i, file in enumerate(attachments):
    response = requests.get(file['url'])
    key = ''

    while response.status_code != 200:
      key = input("Something went wrong trying to download file " + str(i+1) + "/" + str(len(attachments)) + " (" + file['filename']
            + "). Response code was " + str(response.status_code) + ". Press Enter to try again, s to skip, q to quit")
      if key == 's' or key == 'S':
        break
      elif key == 'q' or key == 'Q':
        quit()
      response = requests.get(file['url'])

    if key == 's' or key == 'S':
      continue
    
    filename = setFileName(file['filename'], save_folder)
    with open(save_folder + '\\' + filename, 'wb') as saveFile:
      saveFile.write(response.content)
    print(filename + " saved successfully")



def isLink(string):
  link_pattern = r'((http|ftp|https):\/\/)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
  return bool(re.search(link_pattern, string))



def handleMessageText(text, openLinks):
  pyperclip.copy(text)

  if isLink(text) and openLinks:
    user_input = input("Message may be a link (" + text + "). Type Y to open it (Enter to ignore)")
    if user_input == 'Y' or user_input == 'y':
      webbrowser.open(text)
    #postStopKey(stopKey)
    #quit()



def importMessageData(message, text_divider, openLinks):
  if len(message['attachments']) > 0:
    download_files(message['attachments'])

  if message['content'] != '':
    handleMessageText(message['content'], openLinks)
    message['content'] += "\n\n" + text_divider
  
  return message['content']



messages = getMessages(my_airdrop_server, auth, stopKey)
if len(messages) == 0:
  input("No new messages found (you may want to check if there is a stopKey blocking new messages). Press Enter to quit")
  quit()
txt = ''

for message in messages:
  txt += importMessageData(message, text_divider, promptOpenLinks)
txt = txt.rstrip(text_divider)

if text_divider in txt:
  with open(setFileName('Airdrop Text.txt'), 'w') as textFile:
    textFile.write(txt)

postStopKey(stopKey, my_airdrop_server, auth)
keepOpen and input("Downloads complete. Press Enter to quit")
