# Onkyo Remote Interactive (Raspberry Pi Python interface)

It's possible to control Onkyo devices via the Remote Interactive (RI) port. This port is normally used for direct communication between two Onkyo devices, but it can be repurposed for a more custom interface.

[![License](https://img.shields.io/github/license/edfincham/onkyo-remote-interactive)](https://github.com/edfincham/onkyo-remote-interactive)
[![Stars](https://img.shields.io/github/stars/edfincham/onkyo-remote-interactive)](https://github.com/edfincham/onkyo-remote-interactive)

## Indebted Work
This work is based on the original [Arduino implementation](https://github.com/docbender/Onkyo-RI) by docbender and the [Raspberry Pi version](https://github.com/sinaxin/Onkyo-Pi) by sinaxin

## Protocol
The protocol description can be found [here](https://lirc.sourceforge.net/remotes/onkyo/Remote_Interactive).

A graphical representation can be found [here](http://fredboboss.free.fr/articles/onkyo_ri.php).

The protocol is fairly straightforward: each message consists of a header, a 12-bit code, and a footer.

## Connection
The RI port expects a 3.5mm mono jack. The tip is the data signal; the sleeve is ground (GND). A stereo jack can be used, in which case the tip is the data signal; the sleeve and ring are GND.

The GPIO pin numbering varies between [Board and BCM](https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering) schemas. In this case, I used the UART TX pin (Board: 8, BCM: 14) which provides 3.3V. However, I suspect any output pin would work.

The UART TX pin was chosen as it is the serial port (mentioned in both docbender's and siaxin's implementations). However, I found that communication worked without enabling the serial port hardware (via `raspi-config`). Go figure.

## Remote Interactive Codes

These are in hexadecimal but plain old decimal works just fine.

**A-9010**
| Action         | Command | Notes                            |
| -------------- | ------- | -------------------------------- | 
| Vol Up         | 0x2     | Volume Up                        |
| Vol Down       | 0x3     | Volume Down                      |
| Power Toggle   | 0x4     | Power Toggle                     |
| Mute Toggle    | 0x5     | Mute Toggle                      |
| Input 1        | 0x20    | Switch to input channel 1        |
| Next Input     | 0xD5    | Switch to next input channel     |
| Previous Input | 0xD6    | Switch to previous input channel |
| Mute           | 0xD7    | Mute                             |
| Power OFF      | 0xDA    | Power OFF                        |
| Power ON       | 0xD9    | Power ON                         |
| Input 3        | 0xE0    | Switch to input channel 3        |
| Input 2        | 0x170   | Switch to input channel 2        |

These vary from device to device. To find the relevant codes, loop through the 12-bit code range (`0x0` to `0xFFF`).

For a more extensive list of devices and their remote interactive codes, check out docbenders' [list](https://github.com/docbender/Onkyo-RI?tab=readme-ov-file#ri-codes)

## Example

It's not hard:

```python
conn = OnkyoRI(pin=8)
conn.send(0x4)
```

# Raspberry Pi Docker Image

The `Dockerfile` defines a container which runs a simple Python [FastAPI](https://fastapi.tiangolo.com/) app which acts as an async queue for executing commands sent to the Onkyo RI port. The app expects `POST` requests with the following structure:

```shell
curl -X POST http://localhost:8080/message \
    -H "Content-Type: application/json" \
    -d '{"action": "0xD9"}'
```

## K3s
If the Raspberry Pi running the container is part of a K3s cluster, the manifest in `k3s` can applied to deploy the container with all the required environment variables and volume mounts.

However, to ensure the pod is deployed to the correct node in the cluster, a label and a taint should be added first. Assuming the node connected to the Onkyo device is called `rpi-x`, run:
```shell
kubectl label node rpi-x device=hifi
kubectl taint nodes rpi-x device=hifi:NoSchedule
kubectl apply -f k3s/onkyo.yaml
```

Unfortunately, the manifest does specify `privileged: true`. There may be a way to avoid this via volume mounts, but I haven't been able to get that working. 
