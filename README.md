# SolaxCloud integration for Home Assistant.

Solax Clound integration based on the (now publicly accssible) SolaxCloud API.
This component is basically a rewrite of [thomascys/solaxcloud](https://github.com/thomascys/solaxcloud).
You need:

- The API Key which is accessible in the Service menu of your SolaxCloud.
- The Inverter Serial Number (SN) is the 10 character Registration No. of the
  specific inverter (see the Inverters menu in SolaxCloud)

## Installation

- Place this directory in `/config/cusotm_components`. If `cusotm_components`
  does not exist, you have to create it.
- Add the sensor to your configuration.yaml:
  ```
  sensor:
  - platform: solaxcloud
    name: Inverter 1
    api_key: YOUR_API_KEY
    sn: YOUR_INVERTER_SN
  ```
- Verify that the custom entities are available in home assistant (Total Yield,
  Daily Yield and AC Power).

## Multiple Inverters

You might have multiple inverters in your PV installation. By simply adding the
same configuration again, but changing the inverter SN, you can add more
inverters to home assistant.

```

```
