# Master Game List EarnKeeper.io Plugin

## Requirements

- Python 3

## Run locally

Install dependencies with:

```
pip3 install -r requirements.txt
```

Run the plugin locally with:

```
python3 main_sync.py
```

## Deploying

The repository is already set up for deploy to kubernetes.

From a fresh install, add a new file to the root of the project:

```
clear-values.yaml
```

(Copy clear-values.yaml.example to get a head start)

Configure this file with your secret settings.

Run the following to generate a secret key and encrypt your settings.

```
werf helm secret generate-secret-key | tr -d '\n' >  .werf_secret_key
werf helm secret values encrypt clear-values.yaml -o .helm/secret-values.yaml
werf helm secret file encrypt secret/credentials.json -o .helm/secret/credentials.json
werf helm secret file encrypt secret/ca.pem -o .helm/secret/ca.pem
werf helm secret file encrypt secret/mongodb.pem -o .helm/secret/mongodb.pem
werf helm secret file encrypt secret/ca_bsc.pem -o .helm/secret/ca_bsc.pem
werf helm secret file encrypt secret/mongodb_bsc.pem -o .helm/secret/mongodb_bsc.pem
```

Set the following two secrets on your github repo:

| Secret Name             | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| WERF_SECRET_KEY         | The contents of .werf_secret_key in the root of your project |
| KUBE_CONFIG_BASE64_DATA | Your k8s config file including your access keys              |

If you have the Github and Digital Ocean CLIs installed you can do this as follows:

```
gh secret set WERF_SECRET_KEY --repos=\"$(git remote get-url origin)\" < .werf_secret_key
gh secret set KUBE_CONFIG_BASE64_DATA --repos=\"$(git remote get-url origin)\" -b$(doctl kubernetes cluster kubeconfig show ekp | base64)
```

Commit your changes and push to `main` branch. The github action in this repo will perform the deploy with werf.
