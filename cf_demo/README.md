# Kernel Gateway on Cloud Foundry

Deploys the [Python Got Scotch API](../scotch_demo/README.md) demo to Cloud Foundry using the conda buildpack.

1. Edit the app name in `manifest.yml`.
2. `cf push` to start it.
3. `cf scale <your app name> -i 2` to scale it.
4. `cf logs <your app name> --recent` to see the API end points (e.g., `/scotches`).
