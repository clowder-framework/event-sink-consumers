# How to test

### 1. Set Environment Variables
Set the following env variables filling in the necessary values:
- export GOOGLE_API_SECRET="<secret_value>"
- export GOOGLE_MEASUREMENT_ID="G-XXXXX"
- export GOOGLE_CLIENT_ID="12345678901"

To create an api secret for your project, on your Google Analytics dashboard go to:
- Admin > Data Streams > choose your stream > Measurement Protocol > Create

To find you measurement id on your google analytics dashboard go to:
- Admin > Data Streams > choose your stream > Measurement ID

The client_id is a unique id.

### 2. Build Docker image locally

In a terminal: ./build.sh

### 3. Start up one or more Google Analytics consumer and send a test message:

- Terminal A: ./recv.sh
- Terminal B: ./send.sh

### 4. Confirm event in Google Analytics
1. Log into your Google Analytics dashboard and click on the appropriate project.
3. Navigate to the Realtime tab.
- Scroll down to event count by event_name panel. You should see the event "test_event" if step 3 completed successfully
4. Click on the event named "test_event."
- The event parameters should now be displayed in the same panel.
5. Click on the "message" parameter.
- You should be able to see "Hello World!" as the value for the message parameter.
