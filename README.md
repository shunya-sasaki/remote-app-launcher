# Remote app launcher

## Setup

```sh
python -m pip install git+https://github.com/shunya-sasaki/remote-app-launcher.git
```

## Usage

### Start server

Run API server with the following command.

```sh
run-start
```

### APIs

| Method | URL            | Description                                      |
| ------ | -------------- | ------------------------------------------------ |
| GET    | /os/           | Get OS name                                      |
| GET    | /disk-usage/   | Retrieve detailed disk usage metrics             |
| POST   | /run-command/  | Initiate a command as a background process       |
| POST   | /kill-process/ | Terminate a process by specifying its process ID |

## Author

- Shunya Sasaki
  - Mail: [shunya.sasaki1120@gmail.com](mailto:shunya.sasaki1120@gmail.com)
  - X: [@ShunyaSasaki](https://x.com/ShunyaSasaki)

## License

[MIT](./LICENSE)
