gcloud functions deploy spam_all \
--runtime python39 \
--trigger-http \
--env-vars-file env.yml \
--allow-unauthenticated
