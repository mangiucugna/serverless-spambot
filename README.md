# Spam Bot

A slack bot running on Cloud Functions that you can use to escalate emergencies like production incidents to a number of channels

To invoke the bot in slack you will use `/[slash command] [optional reason]` this will spam all the channels configured in the code

## How to deploy

### Gitlab

The project is already provided with a .gitlab-ci.yml that takes care of deploying after each push to master via Cloud Deploy using the official Cloud SDK docker image and read the secrets from the variables

## Manually

Use deploy.sh to manually deploy the function, but don't forget to fill env.yml with the right content


## How to setup the projects

In the unlikely event that all production setup is lost, this is a guide to setup the projects in order to make this code work again.

### Google Cloud

- Create or edit a new project and enable the following APIs: `Cloud Functions`, `Cloud Build`. If you are not familiar with it you can look at this [tutorial](https://cloud.google.com/functions/docs/tutorials/slack#before-you-begin)
- Add the Google `project_id` to the Gitlab env variable `PROJECT_ID` or make sure that your local google cloud sdk is set to the right project id before deploying

*If you are using Gitlab CI*
- Create a service account with the following permissions: `Service Account User`, `Cloud Functions Developer`, `Cloud Build Service Account` and generate a JSON key
- Store the content of the JSON key in the Gitlab env variable `SERVICE_ACCOUNT`

### Slack App

Create a new app in Slack, the name doesn't matter what matters is that you set it up as follows:
- Copy the signing secret to a gitlab env variable called `SLACK_SIGNING_SECRET` or in `env.yml`
- Add the following scope permissions: `chat:write`, `chat:write.public`
- Create a slash command and add the Cloud Function endpoint url to it
- Add the application to your workspace
- Copy the OAUTH token to the Gitlab env variable `SLACK_BOT_OAUTH_TOKEN` or in `env.yml`

## License

Licensed under MIT License, read the `LICENSE` file for more information