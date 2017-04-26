<img src="http://i.imgur.com/aMo4RaH.png" alt="" height="40" style="max-width:100%;">

Live @: http://178.62.41.17

<img src="http://i.imgur.com/VgxvuF9.png" alt="" height="40" style="max-width:100%;">
Ticketr is a ticket sales platform for any type of event, it allows Event Owners to start selling their tickets, while it let's Event Goers re-sell their tickets safely on the Ticketr website. All payments are handled through PayPal, and when a user purchases a ticket a pdf and qrcode are generated for the user, that will be scanned upon arriving to the event to check the validity of the ticket. When reselling a ticket, a user can only ask for the price they paid (ticket face value), or less. Ticketr is written using Python on the Django framework, and is accompanied by its own Android app for Event Owners to scan tickets at the doors of their events, and also a REST API, which can be used to create future applications for event listings, and also handles authentication and ticket checking in/validating with the Android App.


<img src="http://i.imgur.com/lDkJPBz.png" alt="" height="40" style="max-width:100%;">
<ul>
<li><strong>User Registration and Logging In</strong>: Authentication of the user upon login. When user logs in a session is set which is used throughout the website to check and see if the user is authenticated.</li>

<li><strong>User registration and logging in</strong>: Authentication of the user upon login. When user logs in a session is set which is used throughout the website to check and see if the user is authenticated.</li>

<li><strong>Organiser Profiles</strong>: Allow users to make an organiser profile which allows them to list their event on the site. The event has many fields like a time and date, description and image. Event owner can create tickets to their event, choose a price, its name, and also the total quantity of these tickets available.</li>

<li><strong>Event Visibility</strong>: Allow the event to be public, private or invite only. Events that are public, allow anyone to buy a ticket, and are listed on the Ticketr site. Private events are the same however they are not listed on the site. You must have the URL to access that event. Finally, an invite only event is listed but a user can only buy ticket(s) if they have a preset invite code set by the event organiser.</li>

<li><strong>Ticket Purchasing (PayPal)</strong>: Users can purchase tickets for events, with all payments being handled through PayPal. When being bought, Ticketr will POST to PayPal, when the payment goes through, PayPal will send a response in the form of a HTTP POST (Instant Payment Notification), which is caught by my IPN listener which takes it and generates a new order for the user. The order includes a QR code and some other transaction information.</li>

<li><strong>QR Code Generation</strong>: Everytime an order is is processed, a qrcode is generated using a unique ID. This is used with the Android app to checkin users at the event (at the door etc).</li>

<li><strong>PDF Generation</strong>: When an order is processed, the user has the option to download their ticket as a PDF, or view the QR code online. If they click Download Ticket, the PDF is generated using a a4 graphic that I created using GIMP. The details are then put onto this PDF using a Python PDF library called Report Lab.</li>

<li><strong>Resell Ticket Security</strong>: When a user resells his/her ticket, it is listed under the event as a ticket being sold by a reseller. Once a user purchases this ticket, a new QR code and order is generated for that user whilst the original users QR code / order is removed. By doing this, it stops users selling their tickets but still having a copy of the soft ticket. If the original user went to the door of an event and it was scanned, the app would say Invalid ticket.</li>

<li><strong>Searching Event</strong>: Allows the user to search for events by a query or by location.</li>

<li><strong>Event Dashboard</strong>: The event dashboard is the main hub for event organisers. It gives statistics on tickets sold. It shows orders, tickets, and also gives the organiser the ability to edit their event and change their settings regarding Event Visibility and resell settings.</li>

<li><strong>Discount Codes</strong>: Discount codes can be set by the event organiser which give the user discount at the checkout page. This is a percentage of the total that is preset by the organiser.</li>

<li><strong>Invite Codes</strong>: These are also set by the event organiser and allows them to let only some people buy tickets that have this invite code. Anyone that doesn't have it cannot buy tickets.</li>

<img src="http://i.imgur.com/R73gx5m.png" alt="" height="40" style="max-width:100%;">
[![Video](https://img.youtube.com/vi/F5iHWranhSM/0.jpg)](https://youtu.be/F5iHWranhSM)
Video still uploading, will be here in a couple of minutes.

<img src="http://i.imgur.com/k7XIEES.png" alt="" height="40" style="max-width:100%;">
Ticketr was created using Python on the Django framework. The frontend is created using Bootstrap. There is some JavaScript and AJAX in it to handle the timer and to remove the ticket once the timer has expired. The application is deployed on a Digital Ocean Ubuntu server that is running Django. The android application is created in Android Studio, using Java, and the Volley library to handle HTTP requests.

I used the above languages and platforms because I wanted to learn something new. I wanted to take this oppurtunity to broaden my knowledge and to learn a new language.

<img src="http://i.imgur.com/clM1Nld.png" alt="" height="40" style="max-width:100%;">
The API was written with Python in the Django project too. It provides multiple end points for outside applications to connect to. The android application connects to these endpoints and posts the username and password to it, using Volley. The API then takes the posted data and checks it with the database. It then returns a response.

<strong>Ticket Validation</strong>
The app sends the scanned code (from the qr code) and the event owners username (that was obtained upon login), to the API. It checks it all. If it is correct then it responds with a relevant message and marks the ticket as used. There is security implemented, to prevent anybody scanning the qrcode. The event owners username and password must be passed (i.e logged in), in order for the qrcode to be scanned.

<strong>User Login</strong>
The app sends the username and password to the API. If it is a valid user, it checks the password. If successful, it will send a reply back that the app will make sense of. If it is a positive response the user logs in and can scan tickets. If not it won't let the user log in.

<img src="http://i.imgur.com/XwhwIaC.png" alt="" height="40" style="max-width:100%;">
I really enjoyed making Ticketr. It gave me a chance to learn a brand new language on my own, and also allowed me to become more familiar with how REST api's work. How HTTP requests are sent and recieved, and ultimately it has helped my understanding of OOP. I'm happy I choose this because it let me mix two different applications (web app and android app) together, even though they are written in different languages. It allowed me to find out how applications like this commnunicate with eachother and how information is sent around the web.
