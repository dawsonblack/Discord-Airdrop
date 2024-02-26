# Cross-platform Airdrop copycat using Discord's API
### Send any combination of text and files to your designated airdrop discord channel and run this program on the desired recipient
#### All text is automatically saved to a txt file, with photos and other files being stored in a folder called "Airdrop Files"
#### If only one bit of text is detected, it's automatically copied to your clipboard

# Steps for use
1. Open discord on your browser and log in
2. Create a new server. This will be your own private server where all data will be sent and received
3. Once this is done, go to the general channel and inspect element, then click on network at the top (this is why you need to be in the browser)
4. Type anything into the chat and send it. you should see several network events pop up, click on the one that says messages. It should be a POST request type
5. Copy the request URL at the top and paste that into the 'my_airdrop_server' variable in the python file
6. Scroll down to requerst headers and copy the Authorization ID. This will be pasted into the auth value in the python file

#### The program should be ready for use now, set it to open with python or terminal so that you can simply double click to accept airdrop. Remember that if you typed a message into your server to grab the request info, you will need to either delete it or send the stop key. I recommend saving the file to your desktop, wherever you save it is where any downloaded files will be saved by default.
